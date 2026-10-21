# Справочник.СерверыMSExchange

- Тип XML: Catalog
- Синоним: Серверы Microsoft Exchange
- Источник: Catalogs/СерверыMSExchange.xml
- Каталог объекта: Catalogs/СерверыMSExchange/ (есть)
- Построено из коммита: 017fc906aca6a153d10c59368f8fd591aa6a4ee7
- Статус: ПОДТВЕРЖДЕНО XML (сгенерировано rebuild_ai 2.0; при расхождении верен исходный XML)
- Autonumbering: true
- CheckUnique: true
- Hierarchical: false
- HierarchyType: HierarchyFoldersAndItems
- CodeLength: 9
- DescriptionLength: 100
- CodeType: String
- ChoiceMode: BothWays
- EditType: InDialog
- DataLockControlMode: Managed
- InputByString: Catalog.СерверыMSExchange.StandardAttribute.Description, Catalog.СерверыMSExchange.StandardAttribute.Code

### Реквизиты (9)

| Имя | Синоним | Тип | FillChecking=ShowError |
|---|---|---|---|
| АдресРесурса | Адрес ресурса | Строка(300) | Да |
| ИспользоватьЗащищенноеСоединение | Использовать защищенное соединение | Булево |  |
| ИспользоватьАутентификациюОС | Использовать аутентификацию ОС | Булево |  |
| Порт | Порт | Число(10,0) |  |
| Сервер | Сервер | Строка(100) | Да |
| Таймаут | Таймаут | Число(5,0) |  |
| ВерсияСервера | Версия сервера | EnumRef.ВерсииСерверовMSExchange | Да |
| ВидКонтактнойИнформацииПользователей | Вид контактной информации пользователей | CatalogRef.ВидыКонтактнойИнформации | Да |
| ВидКонтактнойИнформацииПомещений | Вид контактной информации помещений | CatalogRef.ВидыКонтактнойИнформации |  |

### Формы (2)

- ФормаЭлемента
- ФормаСписка

### BSL-модули

- Catalogs/СерверыMSExchange/Ext/ManagerModule.bsl (12685 байт)

Методы: _ai/modules/Catalogs/СерверыMSExchange.md

- Source XML SHA-256: 9853cfd7ee96d506853ee0fb264075946b3122910fa84b07cf2edb523bbd73af
- This is a generated summary, not the complete XML.
- FillChecking=ShowError is an XML setting; runtime validation requires BSL analysis.
