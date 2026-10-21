#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
find_orphans.py 1.0 — находит в выгрузке конфигурации 1С файлы объектов, которых нет в составе.

Объект считается «сиротой», если <Папка>/<Имя>.xml лежит в дереве, но его нет ни в
Configuration.xml, ни в ConfigDumpInfo.xml (запись Metadata name="Тип.Имя").
По умолчанию только отчёт. Удаление: ключ --apply, через git rm (обратимо: git restore / revert).

Запуск (Windows):  py tools\find_orphans.py --repo .
"""
import argparse
import os
import subprocess
import sys
import xml.etree.ElementTree as ET

TAG_TO_FOLDER = {
    "Language": "Languages", "Subsystem": "Subsystems", "StyleItem": "StyleItems",
    "CommonPicture": "CommonPictures", "SessionParameter": "SessionParameters", "Role": "Roles",
    "CommonTemplate": "CommonTemplates", "FilterCriterion": "FilterCriteria",
    "CommonModule": "CommonModules", "CommonAttribute": "CommonAttributes",
    "ExchangePlan": "ExchangePlans", "XDTOPackage": "XDTOPackages", "WebService": "WebServices",
    "HTTPService": "HTTPServices", "WSReference": "WSReferences",
    "EventSubscription": "EventSubscriptions", "ScheduledJob": "ScheduledJobs",
    "SettingsStorage": "SettingsStorages", "FunctionalOption": "FunctionalOptions",
    "FunctionalOptionsParameter": "FunctionalOptionsParameters", "DefinedType": "DefinedTypes",
    "CommonCommand": "CommonCommands", "CommandGroup": "CommandGroups", "Constant": "Constants",
    "CommonForm": "CommonForms", "Catalog": "Catalogs", "Document": "Documents",
    "DocumentNumerator": "DocumentNumerators", "Sequence": "Sequences",
    "DocumentJournal": "DocumentJournals", "Enum": "Enums", "Report": "Reports",
    "DataProcessor": "DataProcessors", "InformationRegister": "InformationRegisters",
    "AccumulationRegister": "AccumulationRegisters",
    "ChartOfCharacteristicTypes": "ChartsOfCharacteristicTypes", "ChartOfAccounts": "ChartsOfAccounts",
    "AccountingRegister": "AccountingRegisters", "ChartOfCalculationTypes": "ChartsOfCalculationTypes",
    "CalculationRegister": "CalculationRegisters", "BusinessProcess": "BusinessProcesses",
    "Task": "Tasks", "ExternalDataSource": "ExternalDataSources",
    "IntegrationService": "IntegrationServices",
}
FOLDER_TO_TAG = {v: k for k, v in TAG_TO_FOLDER.items()}


def ln(tag):
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def parse_xml(path):
    with open(path, "rb") as f:
        data = f.read()
    if data.startswith(b"\xef\xbb\xbf"):
        data = data[3:]
    return ET.fromstring(data)


def read_registry(repo):
    root = parse_xml(os.path.join(repo, "Configuration.xml"))
    cfg = next((c for c in root if ln(c.tag) == "Configuration"), None)
    child = next((c for c in cfg if ln(c.tag) == "ChildObjects"), None) if cfg is not None else None
    if child is None:
        sys.exit("В Configuration.xml не найден Configuration/ChildObjects")
    names = {}
    for c in child:
        name = (c.text or "").strip()
        if name:
            names.setdefault(ln(c.tag), set()).add(name)
    return names


def read_dumpinfo(repo):
    path = os.path.join(repo, "ConfigDumpInfo.xml")
    if not os.path.isfile(path):
        return None
    result = set()
    for _, el in ET.iterparse(path, events=("end",)):
        if ln(el.tag) == "Metadata":
            n = el.attrib.get("name", "")
            if n.count(".") == 1:
                result.add(n)
        el.clear()
    return result


def dir_stats(path):
    count = size = 0
    for dp, _, fns in os.walk(path):
        for fn in fns:
            count += 1
            size += os.path.getsize(os.path.join(dp, fn))
    return count, size


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Поиск файлов выгрузки без записи в составе конфигурации")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--apply", action="store_true", help="удалить найденные файлы через git rm")
    ap.add_argument("--max", type=int, default=100, help="предохранитель: больше этого числа не удалять")
    ap.add_argument("--force", action="store_true", help="разрешить удаление при незафиксированных изменениях")
    a = ap.parse_args()
    repo = os.path.abspath(a.repo)

    registry = read_registry(repo)
    dumpinfo = read_dumpinfo(repo)
    if dumpinfo is None:
        print("ConfigDumpInfo.xml не найден: проверка только по Configuration.xml")

    orphans = []
    for folder, tag in sorted(FOLDER_TO_TAG.items()):
        fdir = os.path.join(repo, folder)
        if not os.path.isdir(fdir):
            continue
        known = registry.get(tag, set())
        for fn in sorted(os.listdir(fdir)):
            if not fn.lower().endswith(".xml"):
                continue
            name = fn[:-4]
            if name in known:
                continue
            in_dump = (dumpinfo is not None) and ("%s.%s" % (tag, name) in dumpinfo)
            orphans.append((folder, tag, name, in_dump))

    print("Найдено файлов без записи в Configuration.xml: %d" % len(orphans))
    paths = []
    for folder, tag, name, in_dump in orphans:
        xml_rel = "%s/%s.xml" % (folder, name)
        dir_rel = "%s/%s" % (folder, name)
        dpath = os.path.join(repo, folder, name)
        cnt = size = 0
        if os.path.isdir(dpath):
            cnt, size = dir_stats(dpath)
        mark = "ЕСТЬ в ConfigDumpInfo (не удалять, разобраться)" if in_dump else "нет в ConfigDumpInfo"
        print("- %s; каталог: %s; файлов в каталоге: %d, байт: %d; %s" % (
            xml_rel, "есть" if cnt or os.path.isdir(dpath) else "нет", cnt, size, mark))
        if not in_dump:
            paths.append(xml_rel)
            if os.path.isdir(dpath):
                paths.append(dir_rel)

    safe = [o for o in orphans if not o[3]]
    print("К удалению (нет ни в Configuration.xml, ни в ConfigDumpInfo.xml): %d" % len(safe))
    if not a.apply:
        print("Режим отчёта. Для удаления добавьте --apply (git rm; откат: git restore --staged --worktree).")
        return
    if len(safe) > a.max:
        sys.exit("Сирот больше предохранителя --max=%d. Проверьте список или увеличьте --max." % a.max)
    st = subprocess.run(["git", "-C", repo, "status", "--porcelain"], capture_output=True, text=True,
                        encoding="utf-8", errors="replace")
    if st.returncode != 0:
        sys.exit("git недоступен или это не репозиторий")
    if st.stdout.strip() and not a.force:
        sys.exit("Есть незафиксированные изменения. Закоммитьте их или используйте --force.")
    if not paths:
        print("Удалять нечего.")
        return
    r = subprocess.run(["git", "-C", repo, "rm", "-r", "-q", "--ignore-unmatch", "--"] + paths,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        sys.exit("git rm завершился ошибкой: %s" % r.stderr.strip())
    print("Удалено из индекса git и рабочего дерева. Проверьте git status и закоммитьте.")


if __name__ == "__main__":
    main()
