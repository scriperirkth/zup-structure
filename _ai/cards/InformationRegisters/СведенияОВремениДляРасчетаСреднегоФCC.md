# РегистрСведений.СведенияОВремениДляРасчетаСреднегоФCC

- Тип XML: InformationRegister
- Синоним: Сведения о времени для расчета среднего (ФCC)
- Источник: InformationRegisters/СведенияОВремениДляРасчетаСреднегоФCC.xml
- Каталог объекта: InformationRegisters/СведенияОВремениДляРасчетаСреднегоФCC/ (есть)
- Построено из коммита: 017fc906aca6a153d10c59368f8fd591aa6a4ee7
- Статус: ПОДТВЕРЖДЕНО XML (сгенерировано rebuild_ai 2.0; при расхождении верен исходный XML)
- WriteMode: Independent
- InformationRegisterPeriodicity: Nonperiodical
- EditType: InDialog
- DataLockControlMode: Managed

### Реквизиты (2)

| Имя | Синоним | Тип | FillChecking=ShowError |
|---|---|---|---|
| ДанныеИзУчетаСреднегоОбщий | Данные из учета среднего общий | Булево |  |
| ДанныеРассчитаныАвтоматически | Данные рассчитаны автоматически | Булево |  |

### Измерения (4)

| Имя | Синоним | Тип | FillChecking=ShowError |
|---|---|---|---|
| ФизическоеЛицо | Физическое лицо | CatalogRef.ФизическиеЛица |  |
| ГоловнаяОрганизация | Головная организация | CatalogRef.Организации |  |
| Месяц | Месяц | Дата(Date) |  |
| Сотрудник | Сотрудник | CatalogRef.Сотрудники |  |

### Ресурсы (2)

| Имя | Синоним | Тип | FillChecking=ShowError |
|---|---|---|---|
| ОтработаноДнейКалендарных | Отработано дней календарных | Число(7,2) |  |
| ДнейБолезниУходаЗаДетьми | Дней болезни, ухода за детьми и др. | Число(5,2) |  |

### BSL-модули

- InformationRegisters/СведенияОВремениДляРасчетаСреднегоФCC/Ext/ManagerModule.bsl (1635 байт)
- InformationRegisters/СведенияОВремениДляРасчетаСреднегоФCC/Ext/RecordSetModule.bsl (3 байт)

Методы: _ai/modules/InformationRegisters/СведенияОВремениДляРасчетаСреднегоФCC.md

- Source XML SHA-256: 345813dd3490ca9b6856a34b04ac5a25d8132c421bb0711eac2c49b711fdc211
- This is a generated summary, not the complete XML.
- FillChecking=ShowError is an XML setting; runtime validation requires BSL analysis.
