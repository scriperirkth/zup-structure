#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Full rebuild of the _ai layer using build_ai_index.py as a library.

Requires Python 3.13 and tools/build_ai_index.py.
Builds into a temporary directory first.
Preserves the previous _ai directory outside the repository.
Does not commit, push, or modify configuration source files.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import os
from pathlib import Path
import re
import subprocess
import sys
import uuid


VERSION = "rebuild_ai 2.0"
BUILD_PREFIX = ".ai-build-"


def fail(message):
    raise RuntimeError(message)


def git(repo, *args):
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        fail(
            "Git failed: "
            + ascii(result.stderr.decode("utf-8", errors="replace"))
        )
    return result.stdout


def source_status(repo, stage_name):
    return git(
        repo,
        "status",
        "--porcelain",
        "--untracked-files=all",
        "--",
        ".",
        ":(top,exclude)_ai",
        ":(top,exclude)" + stage_name,
    )


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_generator(path):
    if not path.is_file():
        fail("Base generator was not found: " + str(path))

    spec = importlib.util.spec_from_file_location(
        "zup_base_generator",
        path,
    )
    module = importlib.util.module_from_spec(spec)

    # Do not create an untracked __pycache__ in tools.
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous

    required = (
        "TAG_TO_FOLDER",
        "FOLDER_TO_TAG",
        "DEFAULT_CARD_FOLDERS",
        "read_registry",
        "build_card",
        "parse_bsl",
        "module_title",
        "cell",
        "rel",
        "write_text",
        "main",
    )

    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        fail("Unsupported base generator: " + ", ".join(missing))

    return module


def install_overrides(g, repo, stage, card_errors):
    g.GENERATOR = VERSION
    g.TAG_TO_FOLDER["PaletteColor"] = "PaletteColors"
    g.FOLDER_TO_TAG["PaletteColors"] = "PaletteColor"

    if "PaletteColors" not in g.DEFAULT_CARD_FOLDERS:
        g.DEFAULT_CARD_FOLDERS.append("PaletteColors")

    original_registry = g.read_registry
    original_card = g.build_card
    allowed_keys = set()

    def strict_registry(root):
        registry, unknown, info = original_registry(root)

        if unknown:
            fail(
                "Unknown configuration object types: "
                + ascii(unknown)
            )

        if not registry or not sum(len(items) for items in registry.values()):
            fail("The configuration object registry is empty.")

        allowed_keys.clear()

        for folder, items in registry.items():
            names = set()

            for tag, name in items:
                if (
                    not name
                    or name in (".", "..")
                    or any(char in name for char in ("/", "\\", ":"))
                ):
                    fail("Invalid metadata object name: " + ascii(name))

                if name.casefold() in names:
                    fail("Duplicate metadata object name: " + ascii(name))

                names.add(name.casefold())

                source = Path(root) / folder / (name + ".xml")

                if not source.is_file():
                    fail("Metadata XML was not found: " + str(source))

                allowed_keys.add((folder, name))

        return registry, unknown, info

    def restricted_scan(root, outname):
        result = {}

        roots = sorted(set(g.TAG_TO_FOLDER.values()) | {"Ext"})

        for folder in roots:
            base = Path(root) / folder
            if not base.is_dir():
                continue

            for directory, dirs, filenames in os.walk(
                base,
                followlinks=False,
            ):
                for child in dirs + filenames:
                    candidate = Path(directory) / child

                    if candidate.is_symlink() or (
                        hasattr(candidate, "is_junction")
                        and candidate.is_junction()
                    ):
                        fail("Link in source tree: " + str(candidate))

                for filename in filenames:
                    if not filename.lower().endswith(".bsl"):
                        continue

                    full = Path(directory) / filename
                    parts = full.relative_to(root).parts

                    if folder == "Ext":
                        key = ("Ext", "Ext")
                    elif len(parts) >= 3:
                        key = (parts[0], parts[1])
                    else:
                        fail("Unexpected BSL location: " + str(full))

                    if key != ("Ext", "Ext") and key not in allowed_keys:
                        fail(
                            "BSL belongs to an object outside the registry: "
                            + str(full)
                        )

                    result.setdefault(key, []).append(str(full))

        for paths in result.values():
            paths.sort()

        return result

    def strict_card(root, folder, tag, name, commit, bsl_files):
        try:
            text = original_card(
                root,
                folder,
                tag,
                name,
                commit,
                bsl_files,
            )

            source = Path(root) / folder / (name + ".xml")

            text = text.replace(
                "| Обязательно |",
                "| FillChecking=ShowError |",
            )

            text += (
                "\n"
                "- Source XML SHA-256: " + sha(source) + "\n"
                "- This is a generated summary, not the complete XML.\n"
                "- FillChecking=ShowError is an XML setting; "
                "runtime validation requires BSL analysis.\n"
            )

            return text

        except Exception as error:
            card_errors.append(
                folder + "/" + name + ": " + str(error)
            )
            raise

    def safe_chunked(path, header, rows, max_bytes):
        # The target directory is new for every full rebuild.
        # No old part files can survive.
        header_text = "\n".join(header) + "\n"
        chunks = []
        current = []
        size = len(header_text.encode("utf-8")) + 256

        for row in rows:
            row_size = len((row + "\n").encode("utf-8"))

            if len(header_text.encode("utf-8")) + row_size + 256 > max_bytes:
                fail(
                    "One output row exceeds the size limit: "
                    + str(path)
                    + ". Increase --max-kb."
                )

            if current and size + row_size > max_bytes:
                chunks.append(current)
                current = []
                size = len(header_text.encode("utf-8")) + 256

            current.append(row)
            size += row_size

        if current or not chunks:
            chunks.append(current)

        base, extension = os.path.splitext(path)
        written = []

        for number, chunk in enumerate(chunks, 1):
            target = (
                path if number == 1
                else base + ".part" + str(number) + extension
            )

            note = ""
            if len(chunks) > 1:
                note = (
                    "\nPart " + str(number)
                    + " of " + str(len(chunks))
                    + ". Read all parts when searching the complete index.\n\n"
                )

            content = header_text + note + "\n".join(chunk) + "\n"

            if len(content.encode("utf-8")) > max_bytes:
                fail("Output exceeds size limit: " + str(target))

            g.write_text(target, content)
            written.append(target)

        return written

    def module_index(root, folder, name, files, commit, max_bytes, out_dir):
        rows = []
        method_count = 0
        export_count = 0

        for path in files:
            # Refuse silent replacement of undecodable bytes.
            Path(path).read_bytes().decode("utf-8-sig")

            line_count, byte_count, methods = g.parse_bsl(path)

            method_count += len(methods)
            export_count += sum(1 for method in methods if method[4])

            rows.extend([
                "",
                "## " + g.rel(path, root),
                "",
                "- Module: " + g.module_title(root, path),
                "- Lines: " + str(line_count),
                "- Bytes: " + str(byte_count),
                "- Source SHA-256: " + sha(path),
                "",
                "| Line | Kind | Name | Parameters | Export | Directives |",
                "|---|---|---|---|---|---|",
            ])

            for line, kind, method, params, exported, directives in methods:
                rows.append(
                    "| %s | %s | %s | %s | %s | %s |"
                    % (
                        line,
                        g.cell(kind),
                        g.cell(method),
                        g.cell(params),
                        "Yes" if exported else "",
                        g.cell(" ".join(directives)),
                    )
                )

        header = [
            "# BSL index: " + folder + "/" + name,
            "",
            "Generator: " + VERSION,
            "Source snapshot commit: " + commit,
            "Navigation only: read the source method body before "
            "describing behavior.",
            "Header recognition is heuristic, not a complete BSL parser.",
            "An absent index entry does not prove an absent method.",
        ]

        output = Path(out_dir) / "modules" / folder / (name + ".md")
        safe_chunked(str(output), header, rows, max_bytes)

        return method_count, export_count

    g.read_registry = strict_registry
    g.scan_bsl = restricted_scan
    g.build_card = strict_card
    g.write_chunked = safe_chunked
    g.build_module_index = module_index

    # This value is set only after the wrapper checks the source tree.
    g.git_dirty = lambda root, outname: "чистое, кроме производного _ai"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument(
        "--max-kb",
        type=int,
        default=24,
        help="Maximum index/table part size in KiB; default 24.",
    )
    args = parser.parse_args()

    if args.max_kb < 8 or args.max_kb > 700:
        fail("--max-kb must be between 8 and 700.")

    repo = Path(args.repo).resolve()
    target = repo / "_ai"

    if not (repo / "Configuration.xml").is_file():
        fail("Configuration.xml was not found.")

    if target.is_symlink() or (
        hasattr(target, "is_junction") and target.is_junction()
    ):
        fail("_ai must not be a symlink or junction.")

    if target.exists() and not target.is_dir():
        fail("_ai exists but is not a directory.")

    stage_name = BUILD_PREFIX + uuid.uuid4().hex
    stage = repo / stage_name

    if source_status(repo, stage_name).strip():
        fail(
            "Commit source/tool/document changes first. "
            "Only _ai changes are allowed during generation."
        )

    head = git(repo, "rev-parse", "HEAD").decode("ascii").strip()

    print("Generator:", VERSION, flush=True)
    print("Source snapshot commit:", head, flush=True)
    print("Temporary output:", stage, flush=True)

    g = load_generator(repo / "tools" / "build_ai_index.py")
    card_errors = []

    install_overrides(g, repo, stage, card_errors)

    # Override the deprecated clock call in the base module without
    # changing the global datetime module used by this wrapper.
    class Clock:
        @staticmethod
        def utcnow():
            return datetime.now(timezone.utc)

    class DateTimeAdapter:
        datetime = Clock

    g.datetime = DateTimeAdapter

    previous_argv = sys.argv[:]

    try:
        sys.argv = [
            str(repo / "tools" / "build_ai_index.py"),
            "--repo", str(repo),
            "--out", stage_name,
            "--max-kb", str(args.max_kb),
        ]
        g.main()
    finally:
        sys.argv = previous_argv

    if card_errors:
        fail(
            "Card generation errors; old _ai was preserved:\n"
            + "\n".join(card_errors[:20])
        )

    if not (stage / "VERSION.md").is_file():
        fail("VERSION.md was not generated.")

    if not (stage / "objects.md").is_file():
        fail("objects.md was not generated.")

    if git(repo, "rev-parse", "HEAD").decode("ascii").strip() != head:
        fail("HEAD changed during generation. Old _ai was preserved.")

    if source_status(repo, stage_name).strip():
        fail("Source tree changed during generation. Old _ai was preserved.")

    files = list(stage.rglob("*.md"))

    if not files:
        fail("The generated layer is empty.")

    # Cards can exceed the index part limit; report the actual maximum.
    largest = max(files, key=lambda path: path.stat().st_size)

    generated_bytes = sum(path.stat().st_size for path in files)

    version_path = stage / "VERSION.md"
    with version_path.open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(
            "\n"
            "- Wrapper: " + VERSION + "\n"
            "- Build policy: full rebuild into a new directory.\n"
            "- Source snapshot verified clean except _ai.\n"
            "- Index/table part limit, KiB: " + str(args.max_kb) + "\n"
            "- Card summaries and header indexes are not complete "
            "XML/BSL analysis.\n"
        )

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S-%f")
    backup = repo.parent / ("zup-ai-backup-" + stamp)

    moved_old = False

    if target.exists():
        target.rename(backup)
        moved_old = True

    try:
        stage.rename(target)
    except Exception:
        if moved_old and not target.exists():
            backup.rename(target)
        raise

    print()
    print("FULL REBUILD PASSED.")
    print("Generated Markdown files:", len(files))
    print("Approximate output bytes:", generated_bytes)
    print("Largest file:", largest.relative_to(stage).as_posix())
    print(
        "Largest file bytes:",
        (target / largest.relative_to(stage)).stat().st_size,
    )
    print("Source snapshot commit:", head)
    print("Published layer:", target)

    if moved_old:
        print("Previous layer backup:", backup)

    print("Configuration source files were not modified.")
    print("No commit or push was executed.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("ERROR:", str(error), file=sys.stderr)
        print(
            "Do not commit or push a failed build. "
            "Preserve the temporary directory and error output.",
            file=sys.stderr,
        )
        sys.exit(1)