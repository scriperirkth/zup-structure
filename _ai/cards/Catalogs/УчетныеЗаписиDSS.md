# Справочник.УчетныеЗаписиDSS

- Тип XML: Catalog
- Синоним: Учетные записи DSS
- Источник: Catalogs/УчетныеЗаписиDSS.xml
- Каталог объекта: Catalogs/УчетныеЗаписиDSS/ (есть)
- Построено из коммита: 017fc906aca6a153d10c59368f8fd591aa6a4ee7
- Статус: ПОДТВЕРЖДЕНО XML (сгенерировано rebuild_ai 2.0; при расхождении верен исходный XML)
- Autonumbering: false
- CheckUnique: false
- Hierarchical: false
- HierarchyType: HierarchyFoldersAndItems
- CodeLength: 0
- DescriptionLength: 100
- CodeType: String
- ChoiceMode: BothWays
- EditType: InDialog
- DataLockControlMode: Managed
- Owners: Catalog.ЭкземплярыСервераDSS
- InputByString: Catalog.УчетныеЗаписиDSS.StandardAttribute.Description

### Реквизиты (8)

| Имя | Синоним | Тип | FillChecking=ShowError |
|---|---|---|---|
| Автор | Автор | CatalogRef.Пользователи |  |
| ВторичнаяАвторизация | Вторичная авторизация | EnumRef.СпособыАвторизацииDSS |  |
| ДополнительнаяИнформация | Дополнительная информация | Строка(неогр.) |  |
| Комментарий | Комментарий | Строка(неогр.) |  |
| Логин | Логин | Строка(50) | Да |
| ПервичнаяАутентификация | Первичная аутентификация | EnumRef.СпособыАвторизацииDSS | Да |
| СодержаниеЗаявления | Содержание заявления | ХранилищеЗначения |  |
| СостояниеЗаявления | Состояние заявления | EnumRef.СостоянияЗаявленияУчетнойЗаписиDSS |  |

### BSL-модули

- Catalogs/УчетныеЗаписиDSS/Ext/ManagerModule.bsl (7683 байт)
- Catalogs/УчетныеЗаписиDSS/Ext/ObjectModule.bsl (5619 байт)

Методы: _ai/modules/Catalogs/УчетныеЗаписиDSS.md

- Source XML SHA-256: 4320411496e739a7e095bca7ee9cde1aab5e5be52e1c3262cd0191faa7ee829b
- This is a generated summary, not the complete XML.
- FillChecking=ShowError is an XML setting; runtime validation requires BSL analysis.
