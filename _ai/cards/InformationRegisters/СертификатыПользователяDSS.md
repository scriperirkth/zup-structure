# РегистрСведений.СертификатыПользователяDSS

- Тип XML: InformationRegister
- Синоним: Сертификаты пользователя DSS
- Источник: InformationRegisters/СертификатыПользователяDSS.xml
- Каталог объекта: InformationRegisters/СертификатыПользователяDSS/ (нет)
- Построено из коммита: 017fc906aca6a153d10c59368f8fd591aa6a4ee7
- Статус: ПОДТВЕРЖДЕНО XML (сгенерировано rebuild_ai 2.0; при расхождении верен исходный XML)
- WriteMode: Independent
- InformationRegisterPeriodicity: Nonperiodical
- EditType: InDialog
- DataLockControlMode: Managed

### Реквизиты (1)

| Имя | Синоним | Тип | FillChecking=ShowError |
|---|---|---|---|
| ДатаДобавления | Дата добавления | Дата(DateTime) |  |

### Измерения (2)

| Имя | Синоним | Тип | FillChecking=ShowError |
|---|---|---|---|
| УчетнаяЗаписьDSS | Учетная запись DSS | CatalogRef.УчетныеЗаписиDSS | Да |
| Отпечаток | Отпечаток | Строка(40) | Да |

### Ресурсы (10)

| Имя | Синоним | Тип | FillChecking=ShowError |
|---|---|---|---|
| Идентификатор | Идентификатор | Число(10,0) |  |
| СерийныйНомер | Серийный номер | Строка(100) |  |
| ДатаНачала | Дата начала | Дата(DateTime) |  |
| ДатаОкончания | Дата окончания | Дата(DateTime) |  |
| Наименование | Наименование | Строка(256) |  |
| АлгоритмКлюча | Алгоритм ключа | Строка(100) |  |
| АлгоритмПодписи | Алгоритм подписи | Строка(100) |  |
| АлгоритмХеширования | Алгоритм хеширования | Строка(100) |  |
| ДанныеСертификата | Данные сертификата | ХранилищеЗначения |  |
| ИдентификаторСертификата | Идентификатор сертификата | Строка(40) |  |

### BSL-модули

- не найдено в дереве (проверка: os.walk по InformationRegisters/СертификатыПользователяDSS/)

- Source XML SHA-256: 5435b48c7e9999956cc70552b38e263b23a48b4719474ceca1f5ea530f263e72
- This is a generated summary, not the complete XML.
- FillChecking=ShowError is an XML setting; runtime validation requires BSL analysis.
