#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Перенос полной выгрузки 1С по CSV сравнения. По умолчанию — проверка."""

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

FOLDERS = set("""
AccumulationRegisters AccountingRegisters BusinessProcesses
CalculationRegisters Catalogs ChartsOfAccounts ChartsOfCalculationTypes
ChartsOfCharacteristicTypes CommandGroups CommonAttributes CommonCommands
CommonForms CommonModules CommonPictures CommonTemplates Constants
DataProcessors DefinedTypes DocumentJournals DocumentNumerators Documents
Enums EventSubscriptions ExchangePlans Ext ExternalDataSources FilterCriteria
FunctionalOptions FunctionalOptionsParameters HTTPServices InformationRegisters
IntegrationServices Languages PaletteColors Reports Roles ScheduledJobs
Sequences SessionParameters SettingsStorages StyleItems Subsystems Tasks
WebServices WSReferences XDTOPackages
""".split())

ROOT_FILES = {"Configuration.xml", "ConfigDumpInfo.xml"}
STATUSES = {"OnlyFresh", "Changed", "OnlyRepo"}


def fail(message):
    raise RuntimeError(message)


def git(repo, *args, data=None):
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        input=data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode not in (0, 1):
        fail(result.stderr.decode("utf-8", errors="replace").strip())
    return result


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def checked_path(root, relative):
    path = root.joinpath(*PurePosixPath(relative).parts)
    current = root
    for part in PurePosixPath(relative).parts:
        current = current / part
        if current.is_symlink() or (
            hasattr(current, "is_junction") and current.is_junction()
        ):
            fail("Ссылка или junction в пути: " + str(current))
    if not path.resolve().is_relative_to(root):
        fail("Путь выходит за пределы корня: " + relative)
    return path


def inventory(root):
    result = set()
    for folder in FOLDERS:
        base = checked_path(root, folder)
        if not base.exists():
            continue
        if not base.is_dir():
            fail("Ожидался каталог: " + str(base))
        for directory, dirs, files in os.walk(base, followlinks=False):
            for name in dirs + files:
                path = Path(directory) / name
                relative = path.relative_to(root).as_posix()
                checked_path(root, relative)
            for name in files:
                result.add((Path(directory) / name).relative_to(root).as_posix())
    for name in ROOT_FILES:
        path = checked_path(root, name)
        if not path.is_file():
            fail("Нет обязательного файла: " + str(path))
        result.add(name)
    return result


def atomic_copy(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix=".sync-", dir=str(target.parent))
    os.close(handle)
    try:
        shutil.copy2(source, temporary)
        os.replace(temporary, target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--fresh", required=True)
    parser.add_argument("--csv", required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    fresh = Path(args.fresh).resolve()
    csv_path = Path(args.csv).resolve()

    if not repo.is_dir() or not fresh.is_dir():
        fail("Не найден репозиторий или каталог свежей выгрузки.")
    if repo == fresh or repo.is_relative_to(fresh) or fresh.is_relative_to(repo):
        fail("Каталоги должны быть раздельными, без вложенности.")

    head_result = git(repo, "rev-parse", "HEAD")
    if head_result.returncode != 0:
        fail("Не удалось определить Git-коммит.")
    head = head_result.stdout.decode().strip()

    unknown = [
        p.name for p in fresh.iterdir()
        if (p.is_dir() and p.name not in FOLDERS)
        or (p.is_file() and p.name not in ROOT_FILES)
    ]
    if unknown:
        fail("Неизвестные элементы в корне свежей выгрузки: " + ", ".join(unknown))

    old_paths = inventory(repo)
    new_paths = inventory(fresh)

    records = []
    seen = set()
    with csv_path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, delimiter=";")
        required = {"Status", "Path", "RepoBytes", "FreshBytes"}
        if not required.issubset(set(reader.fieldnames or [])):
            fail("Неверные столбцы CSV.")

        for row in reader:
            relative = row["Path"].replace("\\", "/")
            parts = PurePosixPath(relative).parts
            if (
                not parts
                or relative.startswith("/")
                or ":" in relative
                or ".." in parts
                or relative != "/".join(parts)
            ):
                fail("Недопустимый путь: " + relative)

            if not (
                relative in ROOT_FILES
                or (len(parts) > 1 and parts[0] in FOLDERS)
            ):
                fail("Путь вне области переноса: " + relative)

            key = relative.casefold()
            if key in seen:
                fail("Повтор пути: " + relative)
            seen.add(key)

            status = row["Status"]
            if status not in STATUSES:
                fail("Неизвестный статус: " + status)

            old = checked_path(repo, relative)
            new = checked_path(fresh, relative)
            old_exists = old.is_file()
            new_exists = new.is_file()
            expected = {
                "OnlyFresh": (False, True),
                "Changed": (True, True),
                "OnlyRepo": (True, False),
            }[status]

            if (old_exists, new_exists) != expected:
                fail("CSV устарел: наличие файлов не совпало: " + relative)

            for path, exists, column in (
                (old, old_exists, "RepoBytes"),
                (new, new_exists, "FreshBytes"),
            ):
                if exists and path.stat().st_size != int(row[column]):
                    fail("CSV устарел: размер не совпал: " + str(path))

            records.append({
                "status": status,
                "path": relative,
                "old_sha256": sha(old) if old_exists else None,
                "new_sha256": sha(new) if new_exists else None,
            })

            if status == "Changed":
                if records[-1]["old_sha256"] == records[-1]["new_sha256"]:
                    fail("Changed, но содержимое уже одинаковое: " + relative)

            if len(records) % 500 == 0:
                print("Проверено строк:", len(records), flush=True)

    for status, actual in (
        ("OnlyFresh", new_paths - old_paths),
        ("OnlyRepo", old_paths - new_paths),
    ):
        reported = {r["path"] for r in records if r["status"] == status}
        if actual != reported:
            fail("CSV не совпадает с текущим списком файлов: " + status)

    payload = b"".join(p.encode("utf-8") + b"\0" for p in sorted(new_paths))
    ignored = git(
        repo, "check-ignore", "--no-index", "-z", "--stdin", data=payload
    )
    if ignored.returncode == 0:
        names = ignored.stdout.decode("utf-8", errors="replace").split("\0")
        fail("Git игнорирует файлы свежей выгрузки:\n" + "\n".join(names[:20]))

    counts = {s: sum(r["status"] == s for r in records) for s in sorted(STATUSES)}
    print("Коммит:", head)
    print("План:", json.dumps(counts, ensure_ascii=False))

    if not args.apply:
        print("Проверка завершена. Исходники и индекс Git не изменялись.")
        print("Для применения предусмотрен --apply. Сейчас его не запускайте.")
        return

    state = git(repo, "status", "--porcelain", "--untracked-files=all")
    if state.returncode != 0 or state.stdout.strip():
        fail("Для применения требуется чистое рабочее дерево.")

    backup = repo.parent / (
        "zup-backup-" + datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S-%f")
    )
    backup.mkdir()
    manifest = {
        "repo": str(repo),
        "fresh": str(fresh),
        "head_before": head,
        "csv": str(csv_path),
        "records": records,
    }
    (backup / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("Резервная копия:", backup, flush=True)

    # Все резервные копии делаются до первого изменения исходников.
    for record in records:
        if record["old_sha256"] is not None:
            source = checked_path(repo, record["path"])
            target = backup / "files" / record["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            if sha(target) != record["old_sha256"]:
                fail("Не совпал хеш резервной копии: " + record["path"])

    # Повторная проверка затрагиваемых файлов после резервного копирования.
    for record in records:
        for root, expected_hash in (
            (repo, record["old_sha256"]),
            (fresh, record["new_sha256"]),
        ):
            path = checked_path(root, record["path"])
            if expected_hash is None:
                if path.exists():
                    fail("Во время проверки появился файл: " + str(path))
            elif not path.is_file() or sha(path) != expected_hash:
                fail("Файл изменился во время подготовки: " + str(path))

    log_path = backup / "applied.jsonl"
    with log_path.open("w", encoding="utf-8") as log:
        for index, record in enumerate(records, 1):
            target = checked_path(repo, record["path"])
            if record["status"] == "OnlyRepo":
                target.unlink()
            else:
                source = checked_path(fresh, record["path"])
                atomic_copy(source, target)
                if sha(target) != record["new_sha256"]:
                    fail("Ошибка проверки скопированного файла: " + str(target))

            log.write(json.dumps(record, ensure_ascii=False) + "\n")
            log.flush()
            if index % 500 == 0:
                print("Применено:", index, flush=True)

    if inventory(repo) != new_paths:
        fail("Итоговый список файлов не совпал со свежей выгрузкой.")

    print("Перенос завершён. Коммит и push не выполнялись.")
    print("Старый _ai не обновлён и пока относится к прежней версии.")
    print("Резервная копия и журнал:", backup)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("ОШИБКА:", error, file=sys.stderr)
        print(
            "Если ошибка возникла во время применения, возможен частичный перенос. "
            "Не коммитьте его; сохраните резервную копию и вывод.",
            file=sys.stderr,
        )
        sys.exit(1)