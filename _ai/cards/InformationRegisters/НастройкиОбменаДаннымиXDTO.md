# РегистрСведений.НастройкиОбменаДаннымиXDTO

- Тип XML: InformationRegister
- Синоним: Настройки обмена данными XDTO
- Источник: InformationRegisters/НастройкиОбменаДаннымиXDTO.xml
- Каталог объекта: InformationRegisters/НастройкиОбменаДаннымиXDTO/ (есть)
- Построено из коммита: 017fc906aca6a153d10c59368f8fd591aa6a4ee7
- Статус: ПОДТВЕРЖДЕНО XML (сгенерировано rebuild_ai 2.0; при расхождении верен исходный XML)
- WriteMode: Independent
- InformationRegisterPeriodicity: Nonperiodical
- EditType: InDialog
- DataLockControlMode: Managed

### Реквизиты (2)

| Имя | Синоним | Тип | FillChecking=ShowError |
|---|---|---|---|
| ИмяПланаОбменаКорреспондента | Имя плана обмена корреспондента | Строка(80) |  |
| ХешНастроек | Хеш настроек | ХранилищеЗначения |  |

### Измерения (1)

| Имя | Синоним | Тип | FillChecking=ShowError |
|---|---|---|---|
| УзелИнформационнойБазы | Узел информационной базы | Набор ExchangePlanRef |  |

### Ресурсы (4)

| Имя | Синоним | Тип | FillChecking=ShowError |
|---|---|---|---|
| Настройки | Настройки | ХранилищеЗначения |  |
| НастройкиКорреспондента | Настройки корреспондента | ХранилищеЗначения |  |
| ПропускатьОбъектыСОшибкамиПроверкиПоСхеме | Пропускать объекты с ошибками проверки по схеме | Булево |  |
| РасширениеФормата | Расширение формата | Строка(250) |  |

### Формы (1)

- ФормаЗаписи

### BSL-модули

- InformationRegisters/НастройкиОбменаДаннымиXDTO/Ext/ManagerModule.bsl (8549 байт)
- InformationRegisters/НастройкиОбменаДаннымиXDTO/Forms/ФормаЗаписи/Ext/Form/Module.bsl (3404 байт)

Методы: _ai/modules/InformationRegisters/НастройкиОбменаДаннымиXDTO.md

- Source XML SHA-256: b10af9bb87c899937e97a49e352cfcf7d6f62eb316f885366fbff703c1da972a
- This is a generated summary, not the complete XML.
- FillChecking=ShowError is an XML setting; runtime validation requires BSL analysis.
