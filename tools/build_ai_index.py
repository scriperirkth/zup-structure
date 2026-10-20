#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_ai_index.py 1.0 — строит производный слой _ai для выгрузки конфигурации 1С (формат Конфигуратора).

Создаёт:
  _ai/VERSION.md              версия выгрузки, коммит, счётчики
  _ai/objects.md              реестр состава по Configuration.xml + сверка с деревом
  _ai/objects/<Папка>.md      таблицы объектов по типам
  _ai/cards/<Папка>/<Имя>.md  карточки объектов (реквизиты, табличные части, типы, регистры)
  _ai/modules/<Папка>/<Имя>.md индекс BSL-модулей (методы, Экспорт, директивы)
  _ai/modules/_summary.md     сводка по модулям

Только стандартная библиотека Python 3.8+. Исходные файлы выгрузки не изменяются.
Запуск (Windows):  py tools\build_ai_index.py --repo . 
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import datetime
import xml.etree.ElementTree as ET

GENERATOR = "build_ai_index 1.0"

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

RU_TYPE = {
    "Document": "Документ", "Catalog": "Справочник", "InformationRegister": "РегистрСведений",
    "AccumulationRegister": "РегистрНакопления", "CalculationRegister": "РегистрРасчета",
    "ChartOfCalculationTypes": "ПланВидовРасчета", "ChartOfCharacteristicTypes": "ПланВидовХарактеристик",
    "ExchangePlan": "ПланОбмена", "Enum": "Перечисление", "Constant": "Константа",
    "DocumentJournal": "ЖурналДокументов", "Report": "Отчет", "DataProcessor": "Обработка",
    "BusinessProcess": "БизнесПроцесс", "Task": "Задача", "ChartOfAccounts": "ПланСчетов",
    "AccountingRegister": "РегистрБухгалтерии",
}

DEFAULT_CARD_FOLDERS = [
    "Documents", "Catalogs", "InformationRegisters", "AccumulationRegisters",
    "CalculationRegisters", "ChartsOfCalculationTypes", "ChartsOfCharacteristicTypes",
    "ExchangePlans", "Enums", "Constants", "DocumentJournals",
]

SIMPLE_PROPS = [
    "Posting", "RealTimePosting", "NumberType", "NumberLength", "Autonumbering", "CheckUnique",
    "Hierarchical", "HierarchyType", "CodeLength", "DescriptionLength", "CodeType",
    "Periodicity", "WriteMode", "RegisterType", "EnableTotalsSplitting", "Posting",
    "InformationRegisterPeriodicity", "ChoiceMode", "EditType", "DataLockControlMode",
]
LIST_PROPS = ["Owners", "BasedOn", "RegisterRecords", "InputByString"]

PRIM = {
    "xs:string": "Строка", "xs:decimal": "Число", "xs:boolean": "Булево", "xs:dateTime": "Дата",
    "v8:ValueStorage": "ХранилищеЗначения", "v8:UUID": "УникальныйИдентификатор",
}

MODULE_NAMES = {
    "ObjectModule.bsl": "Модуль объекта", "ManagerModule.bsl": "Модуль менеджера",
    "RecordSetModule.bsl": "Модуль набора записей", "CommandModule.bsl": "Модуль команды",
    "ValueManagerModule.bsl": "Модуль менеджера значения", "ApplicationModule.bsl": "Модуль приложения",
    "ManagedApplicationModule.bsl": "Модуль управляемого приложения",
    "SessionModule.bsl": "Модуль сеанса", "ExternalConnectionModule.bsl": "Модуль внешнего соединения",
}

HDR = re.compile(r"^\s*(Процедура|Функция|Procedure|Function)\s+([^\s(]+)\s*\(", re.I)


def ln(tag):
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def kid(el, name):
    if el is None:
        return None
    for c in el:
        if ln(c.tag) == name:
            return c
    return None


def kids(el, name):
    if el is None:
        return []
    return [c for c in el if ln(c.tag) == name]


def text_of(el, name):
    c = kid(el, name)
    return (c.text or "").strip() if c is not None else ""


def synonym(props):
    syn = kid(props, "Synonym")
    if syn is None:
        return ""
    items = kids(syn, "item")
    best = ""
    for it in items:
        content = text_of(it, "content")
        if text_of(it, "lang") == "ru":
            return content
        best = best or content
    return best


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def rel(path, base):
    return os.path.relpath(path, base).replace(os.sep, "/")


def type_str(t):
    if t is None:
        return ""
    quals = {ln(c.tag): c for c in t}
    parts = []
    for c in t:
        n = ln(c.tag)
        v = (c.text or "").strip()
        if n == "Type":
            base = PRIM.get(v, v[4:] if v.startswith("cfg:") else v)
            if v == "xs:string":
                sq = quals.get("StringQualifiers")
                length = text_of(sq, "Length") if sq is not None else ""
                base = "Строка(%s)" % (length if length and length != "0" else "неогр.")
            elif v == "xs:decimal":
                nq = quals.get("NumberQualifiers")
                if nq is not None:
                    base = "Число(%s,%s)" % (text_of(nq, "Digits"), text_of(nq, "FractionDigits"))
            elif v == "xs:dateTime":
                dq = quals.get("DateQualifiers")
                f = text_of(dq, "DateFractions") if dq is not None else ""
                base = "Дата" + ("(%s)" % f if f else "")
            parts.append(base)
        elif n == "TypeSet":
            parts.append("Набор " + (v[4:] if v.startswith("cfg:") else v))
    return " | ".join(parts)


def choice_links(props):
    res = []
    for link in kids(kid(props, "ChoiceParameterLinks"), "Link"):
        name = text_of(link, "Name")
        path = text_of(link, "DataPath")
        if name or path:
            res.append("%s <- %s" % (name, path))
    return "; ".join(res)


def run_git(repo, args):
    try:
        r = subprocess.run(["git", "-C", repo, "-c", "core.quotepath=off"] + args,
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode != 0:
            return None
        return r.stdout
    except OSError:
        return None


def git_head(repo):
    out = run_git(repo, ["rev-parse", "HEAD"])
    return out.strip() if out else "неизвестен (не git-репозиторий или git недоступен)"


def git_dirty(repo, outname):
    out = run_git(repo, ["status", "--porcelain", "--", ".", ":(exclude)%s" % outname])
    if out is None:
        return "неизвестно"
    return "есть незафиксированные изменения (кроме %s)" % outname if out.strip() else "чистое"


def parse_xml(path):
    with open(path, "rb") as f:
        data = f.read()
    if data.startswith(b"\xef\xbb\xbf"):
        data = data[3:]
    return ET.fromstring(data)


def read_registry(repo):
    cfg_path = os.path.join(repo, "Configuration.xml")
    if not os.path.isfile(cfg_path):
        sys.exit("Не найден Configuration.xml в %s" % repo)
    root = parse_xml(cfg_path)
    cfg = None
    for c in root:
        if ln(c.tag) == "Configuration":
            cfg = c
    if cfg is None:
        sys.exit("В Configuration.xml нет элемента Configuration. Корневые элементы: %s"
                 % ", ".join(ln(c.tag) for c in root))
    child = kid(cfg, "ChildObjects")
    if child is None:
        sys.exit("В Configuration.xml нет ChildObjects. Дочерние элементы Configuration: %s"
                 % ", ".join(ln(c.tag) for c in cfg))
    registry = {}
    unknown = {}
    for c in child:
        tag = ln(c.tag)
        name = (c.text or "").strip()
        if not name:
            continue
        folder = TAG_TO_FOLDER.get(tag)
        if folder is None:
            unknown[tag] = unknown.get(tag, 0) + 1
            folder = tag + "s"
        registry.setdefault(folder, []).append((tag, name))
    props = kid(cfg, "Properties")
    info = {
        "format": root.attrib.get("version", ""),
        "name": text_of(props, "Name"),
        "synonym": synonym(props),
        "version": text_of(props, "Version"),
        "vendor": text_of(props, "Vendor"),
        "compat": text_of(props, "CompatibilityMode"),
    }
    return registry, unknown, info


def scan_bsl(repo, outname):
    found = {}
    for dirpath, dirnames, filenames in os.walk(repo):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != outname]
        for fn in filenames:
            if not fn.lower().endswith(".bsl"):
                continue
            full = os.path.join(dirpath, fn)
            parts = rel(full, repo).split("/")
            if parts[0] == "Ext" and len(parts) >= 2:
                key = ("Ext", "Ext")
            elif len(parts) >= 3:
                key = (parts[0], parts[1])
            else:
                key = ("_root", parts[0])
            found.setdefault(key, []).append(full)
    for k in found:
        found[k].sort()
    return found


def strip_comment(line):
    inq = False
    for i, ch in enumerate(line):
        if ch == '"':
            inq = not inq
        elif ch == "/" and not inq and line[i:i + 2] == "//":
            return line[:i]
    return line


def parse_bsl(path):
    with open(path, "rb") as f:
        data = f.read()
    text = data.decode("utf-8-sig", errors="replace")
    lines = text.splitlines()
    n = len(lines)
    methods = []
    pending = []
    i = 0
    while i < n:
        raw = lines[i]
        s = raw.strip()
        if s.startswith("&"):
            pending.append(s)
            i += 1
            continue
        m = HDR.match(raw)
        if m:
            header = strip_comment(raw).strip()
            j = i
            while header.count("(") > header.count(")") and j + 1 < n and j - i < 60:
                j += 1
                header += " " + strip_comment(lines[j]).strip()
            close = header.rfind(")")
            after = header[close + 1:] if close >= 0 else ""
            export = re.search(r"\b(Экспорт|Export)\b", after, re.I) is not None
            params = header[header.find("(") + 1:close] if close >= 0 else ""
            params = re.sub(r"\s+", " ", params).strip()
            kind = "Функция" if m.group(1).lower() in ("функция", "function") else "Процедура"
            methods.append((i + 1, kind, m.group(2), params, export, list(pending)))
            pending = []
            i = j + 1
            continue
        if s and not s.startswith("//") and not s.startswith("#"):
            pending = []
        i += 1
    return n, len(data), methods


def module_title(repo, path):
    fn = os.path.basename(path)
    if fn in MODULE_NAMES:
        return MODULE_NAMES[fn]
    r = rel(path, repo)
    if fn == "Module.bsl":
        if "/Forms/" in r or r.startswith("CommonForms/"):
            return "Модуль формы"
        if r.startswith("CommonModules/"):
            return "Общий модуль"
        return "Модуль"
    return fn


def write_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def write_chunked(path, header, rows, max_bytes):
    """Пишет таблицу; при превышении max_bytes делит на path.partN.md."""
    head = "\n".join(header) + "\n"
    chunks, cur, size = [], [], len(head.encode("utf-8"))
    for r in rows:
        b = len(r.encode("utf-8")) + 1
        if cur and size + b > max_bytes:
            chunks.append(cur)
            cur, size = [], len(head.encode("utf-8"))
        cur.append(r)
        size += b
    chunks.append(cur)
    written = []
    base, ext = os.path.splitext(path)
    for idx, ch in enumerate(chunks, 1):
        p = path if idx == 1 else "%s.part%d%s" % (base, idx, ext)
        note = "" if len(chunks) == 1 else "\n(Часть %d из %d)\n" % (idx, len(chunks))
        write_text(p, head + note + "\n".join(ch) + "\n")
        written.append(p)
    return written


def group_children(child):
    groups = {}
    for c in child if child is not None else []:
        groups.setdefault(ln(c.tag), []).append(c)
    return groups


def element_name(el):
    if len(el) == 0:
        return (el.text or "").strip(), ""
    props = kid(el, "Properties")
    return text_of(props, "Name"), synonym(props)


def fields_table(title, elements):
    if not elements:
        return []
    rows = []
    has_links = False
    for el in elements:
        props = kid(el, "Properties")
        links = choice_links(props)
        has_links = has_links or bool(links)
        required = "Да" if text_of(props, "FillChecking") == "ShowError" else ""
        rows.append((text_of(props, "Name"), synonym(props), type_str(kid(props, "Type")), required, links))
    out = ["", "### %s (%d)" % (title, len(rows)), ""]
    if has_links:
        out += ["| Имя | Синоним | Тип | Обязательно | Связи выбора |", "|---|---|---|---|---|"]
        out += ["| %s | %s | %s | %s | %s |" % tuple(cell(x) for x in r) for r in rows]
    else:
        out += ["| Имя | Синоним | Тип | Обязательно |", "|---|---|---|---|"]
        out += ["| %s | %s | %s | %s |" % tuple(cell(x) for x in r[:4]) for r in rows]
    return out


def build_card(repo, folder, tag, name, commit, bsl_files):
    xml_path = os.path.join(repo, folder, name + ".xml")
    root = parse_xml(xml_path)
    obj = None
    for c in root:
        obj = c
        break
    if obj is None:
        raise ValueError("пустой XML")
    props = kid(obj, "Properties")
    child = kid(obj, "ChildObjects")
    ru = RU_TYPE.get(tag, tag)
    obj_dir = os.path.join(repo, folder, name)
    out = ["# %s.%s" % (ru, name), ""]
    out.append("- Тип XML: %s" % tag)
    out.append("- Синоним: %s" % (synonym(props) or "—"))
    out.append("- Источник: %s/%s.xml" % (folder, name))
    out.append("- Каталог объекта: %s/%s/ (%s)" % (folder, name, "есть" if os.path.isdir(obj_dir) else "нет"))
    out.append("- Построено из коммита: %s" % commit)
    out.append("- Статус: ПОДТВЕРЖДЕНО XML (сгенерировано %s; при расхождении верен исходный XML)" % GENERATOR)
    shown = []
    for p in SIMPLE_PROPS:
        v = text_of(props, p)
        if v and p not in shown:
            shown.append(p)
            out.append("- %s: %s" % (p, v))
    for p in LIST_PROPS:
        el = kid(props, p)
        vals = [(x.text or "").strip() for x in el] if el is not None else []
        vals = [v for v in vals if v]
        if vals:
            out.append("- %s: %s" % (p, ", ".join(vals)))
    groups = group_children(child)
    out += fields_table("Реквизиты", groups.pop("Attribute", []))
    out += fields_table("Измерения", groups.pop("Dimension", []))
    out += fields_table("Ресурсы", groups.pop("Resource", []))
    for ts in groups.pop("TabularSection", []):
        tprops = kid(ts, "Properties")
        out += fields_table("Табличная часть %s" % text_of(tprops, "Name"),
                            kids(kid(ts, "ChildObjects"), "Attribute"))
    enum_vals = groups.pop("EnumValue", [])
    if enum_vals:
        out += ["", "### Значения (%d)" % len(enum_vals), "", "| Имя | Синоним |", "|---|---|"]
        for ev in enum_vals:
            n, s = element_name(ev)
            out.append("| %s | %s |" % (cell(n), cell(s)))
    for key, title in (("Form", "Формы"), ("Command", "Команды"), ("Template", "Макеты")):
        els = groups.pop(key, [])
        if els:
            names = [element_name(e)[0] for e in els]
            out += ["", "### %s (%d)" % (title, len(names)), ""] + ["- %s" % n for n in names]
    if groups:
        out += ["", "### Прочие дочерние элементы", ""]
        out += ["- %s: %d" % (k, len(v)) for k, v in sorted(groups.items())]
    out += ["", "### BSL-модули", ""]
    if bsl_files:
        for p in bsl_files:
            out.append("- %s (%d байт)" % (rel(p, repo), os.path.getsize(p)))
        out.append("")
        out.append("Методы: _ai/modules/%s/%s.md" % (folder, name))
    else:
        out.append("- не найдено в дереве (проверка: os.walk по %s/%s/)" % (folder, name))
    return "\n".join(out) + "\n"


def build_module_index(repo, folder, name, files, commit, max_bytes, out_dir):
    total_methods = total_export = 0
    sections = []
    rows_all = []
    for p in files:
        lines_n, size, methods = parse_bsl(p)
        exp = sum(1 for m in methods if m[4])
        total_methods += len(methods)
        total_export += exp
        sections.append((p, lines_n, size, len(methods), exp))
        rows_all.append("")
        rows_all.append("## %s — %s" % (rel(p, repo), module_title(repo, p)))
        rows_all.append("")
        rows_all.append("Строк: %d, байт: %d, методов: %d, экспортных: %d" % (lines_n, size, len(methods), exp))
        if methods:
            rows_all += ["", "| Строка | Вид | Имя | Параметры | Экспорт | Директивы |", "|---|---|---|---|---|---|"]
            for (ln_no, kind, mname, params, export, dirs) in methods:
                rows_all.append("| %d | %s | %s | %s | %s | %s |" % (
                    ln_no, kind, cell(mname), cell(params[:300]), "Да" if export else "", cell(" ".join(dirs))))
    header = ["# Модули: %s/%s" % (folder, name), "",
              "Построено из коммита: %s" % commit,
              "Статус: ПОДТВЕРЖДЕНО BSL (сгенерировано %s; номера строк относятся к указанному коммиту)" % GENERATOR]
    path = os.path.join(out_dir, "modules", folder, name + ".md")
    write_chunked(path, header, rows_all, max_bytes)
    return total_methods, total_export


def affected_keys(repo, since):
    out = run_git(repo, ["diff", "--name-only", "-z", since, "HEAD"])
    if out is None:
        sys.exit("Не удалось выполнить git diff от %s" % since)
    keys = set()
    for p in [x for x in out.split("\0") if x]:
        parts = p.split("/")
        if parts[0] in ("Configuration.xml", "ConfigDumpInfo.xml") or parts[0].startswith("_ai"):
            continue
        if parts[0] == "Ext":
            keys.add(("Ext", "Ext"))
        elif len(parts) >= 2:
            nm = parts[1][:-4] if len(parts) == 2 and parts[1].lower().endswith(".xml") else parts[1]
            keys.add((parts[0], nm))
    return keys


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Строит слой _ai для выгрузки конфигурации 1С")
    ap.add_argument("--repo", default=".", help="корень выгрузки (где лежит Configuration.xml)")
    ap.add_argument("--out", default="_ai", help="имя каталога результата внутри репозитория")
    ap.add_argument("--cards", default="default",
                    help="папки для карточек через запятую, 'default' или 'all'")
    ap.add_argument("--only", default="", help="одна пара Папка/Имя для проверки, например Documents/ИмяДокумента")
    ap.add_argument("--changed-since", default="", help="коммит: перестроить только затронутые объекты")
    ap.add_argument("--no-cards", action="store_true")
    ap.add_argument("--no-modules", action="store_true")
    ap.add_argument("--max-kb", type=int, default=700, help="предел размера одного md-файла")
    a = ap.parse_args()

    repo = os.path.abspath(a.repo)
    out_dir = os.path.join(repo, a.out)
    max_bytes = a.max_kb * 1024
    commit = git_head(repo)
    print("Репозиторий:", repo)
    print("Коммит:", commit)

    registry, unknown, info = read_registry(repo)
    total = sum(len(v) for v in registry.values())
    print("Объектов в Configuration.xml: %d, типов: %d" % (total, len(registry)))
    if unknown:
        print("Внимание, неизвестные теги Configuration.xml (папка = тег+'s'):", unknown)

    bsl = scan_bsl(repo, a.out)

    if a.cards == "all":
        card_folders = [f for f in registry if f in FOLDER_TO_TAG]
    elif a.cards == "default":
        card_folders = [f for f in DEFAULT_CARD_FOLDERS if f in registry]
    else:
        card_folders = [x.strip() for x in a.cards.split(",") if x.strip()]

    only = None
    if a.only:
        pf = a.only.replace("\\", "/").split("/", 1)
        only = {(pf[0], pf[1])}
    keys = None
    mode = "полная"
    if only:
        keys = only
        mode = "одиночная: %s" % a.only
    elif a.changed_since:
        keys = affected_keys(repo, a.changed_since)
        mode = "инкрементальная от %s" % a.changed_since
        print("Затронуто объектов:", len(keys))

    # реестр и сверка с деревом
    mismatch = []
    obj_rows = {}
    for folder, items in sorted(registry.items()):
        fdir = os.path.join(repo, folder)
        files_xml = set()
        if os.path.isdir(fdir):
            files_xml = {fn[:-4] for fn in os.listdir(fdir) if fn.lower().endswith(".xml")}
        names = {n for _, n in items}
        for tag, n in sorted(items, key=lambda x: x[1]):
            has_xml = n in files_xml
            has_dir = os.path.isdir(os.path.join(fdir, n))
            nb = len(bsl.get((folder, n), []))
            card = "cards/%s/%s.md" % (folder, n) if folder in card_folders else ""
            if not has_xml:
                mismatch.append("- В Configuration.xml есть %s.%s, но нет файла %s/%s.xml" % (tag, n, folder, n))
            obj_rows.setdefault(folder, []).append(
                "| %s | %s | %s | %s | %d | %s |" % (
                    cell(n), tag, ("%s/%s.xml" % (folder, n)) if has_xml else "НЕТ ФАЙЛА",
                    "да" if has_dir else "нет", nb, card))
        for extra in sorted(files_xml - names):
            mismatch.append("- Файл %s/%s.xml есть в дереве, но не найден в Configuration.xml" % (folder, extra))

    idx = ["# Реестр состава конфигурации", "",
           "Построено из коммита: %s" % commit,
           "Источник: Configuration.xml. Статус: ПОДТВЕРЖДЕНО СОСТАВОМ (сгенерировано %s)." % GENERATOR, "",
           "| Папка | Тип XML | Объектов | Таблица |", "|---|---|---|---|"]
    for folder, items in sorted(registry.items()):
        tag = items[0][0]
        idx.append("| %s | %s | %d | objects/%s.md |" % (folder, tag, len(items), folder))
    idx += ["", "Всего объектов: %d" % total, "", "## Расхождения реестра и дерева", ""]
    idx += mismatch if mismatch else ["Расхождений не найдено."]
    write_text(os.path.join(out_dir, "objects.md"), "\n".join(idx) + "\n")
    for folder, rows in obj_rows.items():
        header = ["# %s" % folder, "", "Построено из коммита: %s" % commit, "",
                  "| Имя | Тип XML | Путь XML | Каталог | Файлов BSL | Карточка |",
                  "|---|---|---|---|---|---|"]
        write_chunked(os.path.join(out_dir, "objects", folder + ".md"), header, rows, max_bytes)

    # удаление устаревших файлов при полной сборке
    valid = {(f, n) for f, items in registry.items() for _, n in items}

    # карточки
    made = errors = 0
    if not a.no_cards:
        for folder in card_folders:
            for tag, name in registry.get(folder, []):
                if keys is not None and (folder, name) not in keys:
                    continue
                try:
                    text = build_card(repo, folder, tag, name, commit, bsl.get((folder, name), []))
                    write_text(os.path.join(out_dir, "cards", folder, name + ".md"), text)
                    made += 1
                except (OSError, ET.ParseError, ValueError) as e:
                    errors += 1
                    print("ОШИБКА карточки %s/%s: %s" % (folder, name, e))
        print("Карточек построено: %d, ошибок: %d" % (made, errors))

    # индекс модулей
    summary = {}
    mm = 0
    if not a.no_modules:
        for key, files in sorted(bsl.items()):
            folder, name = key
            s = summary.setdefault(folder, [0, 0])
            s[0] += len(files)
            s[1] += sum(os.path.getsize(p) for p in files)
            if keys is not None and key not in keys:
                continue
            build_module_index(repo, folder, name, files, commit, max_bytes, out_dir)
            mm += 1
        print("Индексов модулей построено: %d" % mm)
        rows = ["| %s | %d | %d |" % (f, v[0], v[1]) for f, v in sorted(summary.items())]
        header = ["# Сводка по BSL-модулям", "", "Построено из коммита: %s" % commit, "",
                  "| Папка | Файлов BSL | Байт |", "|---|---|---|"]
        write_chunked(os.path.join(out_dir, "modules", "_summary.md"), header, rows, max_bytes)

    # чистка осиротевших файлов (только при полной сборке)
    removed = 0
    if keys is None:
        for sub in ("cards", "modules"):
            base = os.path.join(out_dir, sub)
            if not os.path.isdir(base):
                continue
            for folder in os.listdir(base):
                fdir = os.path.join(base, folder)
                if not os.path.isdir(fdir):
                    continue
                for fn in os.listdir(fdir):
                    nm = re.sub(r"(\.part\d+)?\.md$", "", fn)
                    ok = (folder, nm) in valid or (sub == "modules" and (folder, nm) in bsl)
                    if not ok:
                        os.remove(os.path.join(fdir, fn))
                        removed += 1
        print("Удалено устаревших файлов: %d" % removed)
    else:
        # в инкрементальном режиме удаляем только то, чего уже нет в составе
        for (folder, name) in keys:
            if (folder, name) not in valid and (folder, name) not in bsl:
                for sub in ("cards", "modules"):
                    for fn in (name + ".md",):
                        p = os.path.join(out_dir, sub, folder, fn)
                        if os.path.isfile(p):
                            os.remove(p)
                            removed += 1
        print("Удалено устаревших файлов: %d" % removed)

    ver = ["# Версия выгрузки и слоя _ai", "",
           "- Генератор: %s" % GENERATOR,
           "- Дата построения (UTC): %s" % datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
           "- Режим: %s" % mode,
           "- Коммит выгрузки: %s" % commit,
           "- Рабочее дерево: %s" % git_dirty(repo, a.out),
           "- Формат выгрузки (version в MetaDataObject): %s" % (info["format"] or "не указан"),
           "- Конфигурация: %s" % (info["name"] or "не указана"),
           "- Синоним: %s" % (info["synonym"] or "не указан"),
           "- Версия конфигурации (Properties/Version): %s" % (info["version"] or "не указана"),
           "- Поставщик: %s" % (info["vendor"] or "не указан"),
           "- Режим совместимости: %s" % (info["compat"] or "не указан"),
           "- Объектов в составе: %d" % total,
           "- Расхождений реестра и дерева: %d" % len(mismatch),
           "",
           "Версия рабочей базы по этому файлу не подтверждается: сверяйте с базой отдельно."]
    write_text(os.path.join(out_dir, "VERSION.md"), "\n".join(ver) + "\n")
    print("Готово:", out_dir)


if __name__ == "__main__":
    main()
