# Справочник.УчетныеЗаписиDSS

- Тип XML: Catalog
- Синоним: Учетные записи DSS
- Источник: Catalogs/УчетныеЗаписиDSS.xml
- Каталог объекта: Catalogs/УчетныеЗаписиDSS/ (есть)
- Построено из коммита: 6666cacc9b4d0c0af95da892dfd99e04107ace80
- Статус: ПОДТВЕРЖДЕНО XML (сгенерировано build_ai_index 1.0; при расхождении верен исходный XML)
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

| Имя | Синоним | Тип | Обязательно |
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
