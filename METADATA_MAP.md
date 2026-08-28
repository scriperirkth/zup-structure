# METADATA_MAP.md — Карта метаданных ЗУП 3.1

> Репозиторий: `scriperirkth/zup-structure`  
> Ветка: `main`  
> Главный источник: `Configuration.xml`  
> Формат: XML-выгрузка метаданных 1С:Предприятие / EDT  
> Правила достоверности: `AI_RULES.md`

## Навигация

1. Сначала искать имя объекта в `Configuration.xml`.
2. Затем открыть одноимённую папку соответствующего типа.
3. Метаданные объекта подтверждать XML-файлом объекта.
4. Наличие BSL проверять по каталогу `Ext/` и файлам `*.bsl`.
5. Если объект не найден — отвечать: `не найден в репозитории`.
6. Не заменять имена объектов «понятными» аналогами и не достраивать реквизиты по знаниям о ЗУП.

## Прикладные объекты

| Папка | XML-тип | BSL-синтаксис | Назначение | Типовой путь |
|---|---|---|---|---|
| `Documents/` | `Document` | `Документы.<Имя>`, `Документ.<Имя>` | Документы кадров, расчёта, выплат, налогов, пособий | `Documents/<Имя>/` |
| `Catalogs/` | `Catalog` | `Справочники.<Имя>`, `Справочник.<Имя>` | Нормативно-справочная информация | `Catalogs/<Имя>/` |
| `InformationRegisters/` | `InformationRegister` | `РегистрыСведений.<Имя>`, `РегистрСведений.<Имя>` | Периодические и непериодические сведения | `InformationRegisters/<Имя>/` |
| `AccumulationRegisters/` | `AccumulationRegister` | `РегистрыНакопления.<Имя>`, `РегистрНакопления.<Имя>` | Остатки и обороты | `AccumulationRegisters/<Имя>/` |
| `CalculationRegisters/` | `CalculationRegister` | `РегистрыРасчета.<Имя>`, `РегистрРасчета.<Имя>` | Расчёт начислений и удержаний | `CalculationRegisters/<Имя>/` |
| `ChartsOfCalculationTypes/` | `ChartOfCalculationTypes` | `ПланыВидовРасчета.<Имя>` | Виды начислений и удержаний | `ChartsOfCalculationTypes/<Имя>/` |
| `ChartsOfCharacteristicTypes/` | `ChartOfCharacteristicTypes` | `ПланыВидовХарактеристик.<Имя>` | Виды характеристик и свойства | `ChartsOfCharacteristicTypes/<Имя>/` |
| `Reports/` | `Report` | `Отчеты.<Имя>`, `Отчет.<Имя>` | Отчёты, в том числе СКД | `Reports/<Имя>/` |
| `DataProcessors/` | `DataProcessor` | `Обработки.<Имя>`, `Обработка.<Имя>` | Обработки, помощники, загрузки, выгрузки | `DataProcessors/<Имя>/` |
| `BusinessProcesses/` | `BusinessProcess` | `БизнесПроцессы.<Имя>`, `БизнесПроцесс.<Имя>` | Маршруты бизнес-процессов | `BusinessProcesses/<Имя>/` |
| `Tasks/` | `Task` | `Задачи.<Имя>`, `Задача.<Имя>` | Задачи бизнес-процессов | `Tasks/<Имя>/` |
| `DocumentJournals/` | `DocumentJournal` | `ЖурналыДокументов.<Имя>` | Журналы документов | `DocumentJournals/<Имя>/` |
| `DocumentNumerators/` | `DocumentNumerator` | `НумераторыДокументов.<Имя>` | Правила нумерации | `DocumentNumerators/<Имя>/` |
| `Enums/` | `Enum` | `Перечисления.<Имя>.<Значение>` | Перечисления | `Enums/<Имя>/` |
| `Constants/` | `Constant` | `Константы.<Имя>` | Константы конфигурации | `Constants/<Имя>/` |
| `DefinedTypes/` | `DefinedType` | Используется в описаниях типов | Определяемые типы | `DefinedTypes/<Имя>/` |
| `FilterCriteria/` | `FilterCriterion` | `КритерииОтбора.<Имя>` | Связанные отборы метаданных | `FilterCriteria/<Имя>/` |

## Общие объекты

| Папка | XML-тип | BSL-синтаксис | Назначение | Типовой путь |
|---|---|---|---|---|
| `CommonModules/` | `CommonModule` | `<ИмяМодуля>.<Метод>()` | Общая серверная, клиентская и интеграционная логика | `CommonModules/<Имя>/` |
| `CommonForms/` | `CommonForm` | `ПолучитьОбщуюФорму("<Имя>")` | Общие управляемые формы | `CommonForms/<Имя>/` |
| `CommonCommands/` | `CommonCommand` | Команда интерфейса / API платформы | Общие команды | `CommonCommands/<Имя>/` |
| `CommandGroups/` | `CommandGroup` | Нет прямого BSL-обращения | Группы команд интерфейса | `CommandGroups/<Имя>/` |
| `CommonAttributes/` | `CommonAttribute` | Реквизит объекта | Общие реквизиты | `CommonAttributes/<Имя>/` |
| `CommonTemplates/` | `CommonTemplate` | `ПолучитьОбщийМакет("<Имя>")` | Макеты, шаблоны, печатные формы | `CommonTemplates/<Имя>/` |
| `CommonPictures/` | `CommonPicture` | Ссылка в форме или макете | Общие изображения | `CommonPictures/<Имя>/` |
| `StyleItems/` | `StyleItem` | Свойства формы и элементов | Стили интерфейса | `StyleItems/<Имя>/` |
| `SettingsStorages/` | `SettingsStorage` | `ХранилищаНастроек.<Имя>` | Хранилища пользовательских настроек | `SettingsStorages/<Имя>/` |
| `Languages/` | `Language` | Используется в метаданных | Языки конфигурации | `Languages/<Имя>/` |
| `Subsystems/` | `Subsystem` | Нет прямого BSL-обращения | Подсистемы и разделы интерфейса | `Subsystems/<Имя>/` |
| `FunctionalOptions/` | `FunctionalOption` | `ПолучитьФункциональнуюОпцию("<Имя>")` | Включение функциональности | `FunctionalOptions/<Имя>/` |
| `FunctionalOptionsParameters/` | `FunctionalOptionParameter` | Используется при расчёте опции | Параметры функциональных опций | `FunctionalOptionsParameters/<Имя>/` |
| `SessionParameters/` | `SessionParameter` | `ПараметрыСеанса.<Имя>` | Параметры сеанса | `SessionParameters/<Имя>/` |

## Интеграции

| Папка | XML-тип | BSL-синтаксис | Назначение | Типовой путь |
|---|---|---|---|---|
| `ExchangePlans/` | `ExchangePlan` | `ПланыОбмена.<Имя>`, `ПланОбмена.<Имя>` | Регистрация изменений и обмены | `ExchangePlans/<Имя>/` |
| `HTTPServices/` | `HTTPService` | HTTP-запросы, обработчики BSL | HTTP API | `HTTPServices/<Имя>/` |
| `WebServices/` | `WebService` | SOAP-вызовы, экспортные методы | SOAP web-сервисы | `WebServices/<Имя>/` |
| `WSReferences/` | `WSReference` | Создание WS-прокси | Ссылки на внешние web-сервисы | `WSReferences/<Имя>/` |
| `XDTOPackages/` | `XDTOPackage` | `ФабрикаXDTO.Создать(...)` | XDTO-типы и XML-схемы | `XDTOPackages/<Имя>/` |
| `IntegrationServices/` | `IntegrationService` | Зависит от описания сервиса | Сервисы интеграционной платформы | `IntegrationServices/<Имя>/` |
| `EventSubscriptions/` | `EventSubscription` | Обработчик общего модуля | Подписки на события объектов | `EventSubscriptions/<Имя>/` |

## Администрирование

| Папка | XML-тип | BSL-синтаксис | Назначение | Типовой путь |
|---|---|---|---|---|
| `Roles/` | `Role` | `ПравоДоступа(...)` | Роли и права доступа | `Roles/<Имя>/` |
| `ScheduledJobs/` | `ScheduledJob` | Вызов экспортного метода общего модуля | Регламентные задания | `ScheduledJobs/<Имя>/` |
| `Ext/` | Служебные модули | Зависит от модуля | Модуль приложения и служебные модули | `Ext/` |
| `Configuration.xml` | `Configuration` | `Метаданные`, глобальный контекст | Полный состав конфигурации | Корень |
| `ConfigDumpInfo.xml` | Служебный файл выгрузки | Не используется в BSL | Данные о выгрузке конфигурации | Корень |
| `docs/` | Документация | Не используется в BSL | Документация репозитория | `docs/` |

## Типовая структура объекта

```text
<Папка>/<ИмяОбъекта>/
├── <ИмяОбъекта>.xml
└── Ext/
    ├── ObjectModule.bsl
    ├── ManagerModule.bsl
    └── Forms/
        └── <ИмяФормы>/
            └── Ext/
                ├── Form.xml
                └── FormModule.bsl
```

Фактический состав зависит от типа объекта. Отсутствие `ObjectModule.bsl`, `ManagerModule.bsl` или `FormModule.bsl` необходимо подтверждать фактическим просмотром папки конкретного объекта.

## Правила поиска

### По синтаксису BSL

| Конструкция в BSL | Папка поиска |
|---|---|
| `Документы.<Имя>` или `Документ.<Имя>` | `Documents/<Имя>/` |
| `Справочники.<Имя>` или `Справочник.<Имя>` | `Catalogs/<Имя>/` |
| `РегистрыСведений.<Имя>` | `InformationRegisters/<Имя>/` |
| `РегистрыНакопления.<Имя>` | `AccumulationRegisters/<Имя>/` |
| `РегистрыРасчета.<Имя>` | `CalculationRegisters/<Имя>/` |
| `ПланыВидовРасчета.<Имя>` | `ChartsOfCalculationTypes/<Имя>/` |
| `ПланыВидовХарактеристик.<Имя>` | `ChartsOfCharacteristicTypes/<Имя>/` |
| `Отчеты.<Имя>` | `Reports/<Имя>/` |
| `Обработки.<Имя>` | `DataProcessors/<Имя>/` |
| `Перечисления.<Имя>` | `Enums/<Имя>/` |
| `Константы.<Имя>` | `Constants/<Имя>/` |
| `ПланыОбмена.<Имя>` | `ExchangePlans/<Имя>/` |
| `ПараметрыСеанса.<Имя>` | `SessionParameters/<Имя>/` |
| `<ИмяОбщегоМодуля>.<Метод>()` | `CommonModules/<ИмяОбщегоМодуля>/` |

### По тематике

Для первичного поиска по бизнес-теме использовать фрагменты русских имён:

```text
НДФЛ
Отпуск
Больнич
Пособ
СФР
ФСС
ПФР
Зарплат
Удержан
Начислен
Штат
Воин
Персональн
ГПХ
Заем
Обмен
```

Результат поиска по имени не подтверждает бизнес-логику объекта. Для подтверждения назначения читать XML и связанные BSL-модули.

## Ограничения

- `Configuration.xml` размером более 1 МБ может не открываться через GitHub Contents API; использовать raw URL или приложенный файл.
- `ConfigDumpInfo.xml` — служебный файл выгрузки, не использовать как источник прикладной логики.
- `README.md`, `TOP_OBJECTS_ZUP.md` и прочие MD-файлы являются навигационными материалами; полный состав объектов подтверждает только `Configuration.xml`.
- Не делать вывод о наличии BSL только по типу метаданных: проверять фактический каталог `Ext/`.