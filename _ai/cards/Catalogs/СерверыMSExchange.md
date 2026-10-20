# Справочник.СерверыMSExchange

- Тип XML: Catalog
- Синоним: Серверы Microsoft Exchange
- Источник: Catalogs/СерверыMSExchange.xml
- Каталог объекта: Catalogs/СерверыMSExchange/ (есть)
- Построено из коммита: 6666cacc9b4d0c0af95da892dfd99e04107ace80
- Статус: ПОДТВЕРЖДЕНО XML (сгенерировано build_ai_index 1.0; при расхождении верен исходный XML)
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

| Имя | Синоним | Тип | Обязательно |
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
