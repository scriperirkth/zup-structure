# РегистрСведений.НастройкиСинхронизацииMSExchange

- Тип XML: InformationRegister
- Синоним: Настройки синхронизации Microsoft Exchange
- Источник: InformationRegisters/НастройкиСинхронизацииMSExchange.xml
- Каталог объекта: InformationRegisters/НастройкиСинхронизацииMSExchange/ (есть)
- Построено из коммита: 6666cacc9b4d0c0af95da892dfd99e04107ace80
- Статус: ПОДТВЕРЖДЕНО XML (сгенерировано build_ai_index 1.0; при расхождении верен исходный XML)
- WriteMode: Independent
- InformationRegisterPeriodicity: Nonperiodical
- EditType: InDialog
- DataLockControlMode: Managed

### Измерения (1)

| Имя | Синоним | Тип | Обязательно |
|---|---|---|---|
| Узел | Узел | ExchangePlanRef.СинхронизацияКалендарей | Да |

### Ресурсы (2)

| Имя | Синоним | Тип | Обязательно |
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
