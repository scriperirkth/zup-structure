# РегистрСведений.НастройкиСинхронизацииMSExchange

- Тип XML: InformationRegister
- Синоним: Настройки синхронизации Microsoft Exchange
- Источник: InformationRegisters/НастройкиСинхронизацииMSExchange.xml
- Каталог объекта: InformationRegisters/НастройкиСинхронизацииMSExchange/ (есть)
- Построено из коммита: 017fc906aca6a153d10c59368f8fd591aa6a4ee7
- Статус: ПОДТВЕРЖДЕНО XML (сгенерировано rebuild_ai 2.0; при расхождении верен исходный XML)
- WriteMode: Independent
- InformationRegisterPeriodicity: Nonperiodical
- EditType: InDialog
- DataLockControlMode: Managed

### Измерения (1)

| Имя | Синоним | Тип | FillChecking=ShowError |
|---|---|---|---|
| Узел | Узел | ExchangePlanRef.СинхронизацияКалендарей | Да |

### Ресурсы (2)

| Имя | Синоним | Тип | FillChecking=ShowError |
|---|---|---|---|
| СерверMSExchange | Сервер Microsoft Exchange | CatalogRef.СерверыMSExchange | Да |
| ИмяПользователя | Имя пользователя | Строка(100) | Да |

### Формы (3)

- ФормаЗаписи
- ФормаСписка
- НастройкаПодключенияMSExchange

### Команды (1)

- ПроверитьСоединение

### BSL-модули

- InformationRegisters/НастройкиСинхронизацииMSExchange/Commands/ПроверитьСоединение/Ext/CommandModule.bsl (407 байт)
- InformationRegisters/НастройкиСинхронизацииMSExchange/Ext/ManagerModule.bsl (3412 байт)
- InformationRegisters/НастройкиСинхронизацииMSExchange/Forms/НастройкаПодключенияMSExchange/Ext/Form/Module.bsl (17452 байт)
- InformationRegisters/НастройкиСинхронизацииMSExchange/Forms/ФормаЗаписи/Ext/Form/Module.bsl (5342 байт)

Методы: _ai/modules/InformationRegisters/НастройкиСинхронизацииMSExchange.md

- Source XML SHA-256: d8b32e969c3b5e3ce08539cf37fc66c88dcf8e46d2fb68a79ae6469d5ea741a0
- This is a generated summary, not the complete XML.
- FillChecking=ShowError is an XML setting; runtime validation requires BSL analysis.
