# METADATA_MAP.md — Карта метаданных ЗУП 3.1

> Репозиторий: `scriperirkth/zup-structure`  
> Ветка: `main`  
> Главный источник: `Configuration.xml`  
> Формат: выгрузка Конфигуратора (XML и BSL)  
> Правила достоверности, пути и статусы: `AI_RULES.md`

## Навигация

1. Сначала искать имя объекта в `Configuration.xml`.
2. Затем открыть `<Папка>/<Имя>.xml` и одноимённый каталог `<Папка>/<Имя>/`.
3. Метаданные объекта подтверждать XML-файлом объекта.
4. Наличие BSL проверять листингом `<Папка>/<Имя>/Ext/` и `Forms/`.
5. Если объект не найден, отвечать по `AI_RULES.md`, раздел 7.
6. Не заменять имена объектов «понятными» аналогами и не достраивать реквизиты по знаниям о ЗУП.

Раскладка в таблицах ниже соответствует `AI_RULES.md`, раздел 2 (проверена на документе и общем модуле; для остальных типов подтверждать листингом).

## Прикладные объекты

| Папка | XML-тип | BSL-синтаксис | Назначение | XML и каталог объекта |
|---|---|---|---|---|
| `Documents/` | `Document` | Документы.<Имя>, Документ.<Имя> | Документы кадров, расчёта, выплат, налогов, пособий | `Documents/<Имя>.xml`, `Documents/<Имя>/` |
| `Catalogs/` | `Catalog` | Справочники.<Имя>, Справочник.<Имя> | Нормативно-справочная информация | `Catalogs/<Имя>.xml`, `Catalogs/<Имя>/` |
| `InformationRegisters/` | `InformationRegister` | РегистрыСведений.<Имя> | Периодические и непериодические сведения | `InformationRegisters/<Имя>.xml`, `InformationRegisters/<Имя>/` |
| `AccumulationRegisters/` | `AccumulationRegister` | РегистрыНакопления.<Имя> | Остатки и обороты | `AccumulationRegisters/<Имя>.xml`, `AccumulationRegisters/<Имя>/` |
| `CalculationRegisters/` | `CalculationRegister` | РегистрыРасчета.<Имя> | Расчёт начислений и удержаний | `CalculationRegisters/<Имя>.xml`, `CalculationRegisters/<Имя>/` |
| `ChartsOfCalculationTypes/` | `ChartOfCalculationTypes` | ПланыВидовРасчета.<Имя> | Виды начислений и удержаний | `ChartsOfCalculationTypes/<Имя>.xml`, `ChartsOfCalculationTypes/<Имя>/` |
| `ChartsOfCharacteristicTypes/` | `ChartOfCharacteristicTypes` | ПланыВидовХарактеристик.<Имя> | Виды характеристик и свойства | `ChartsOfCharacteristicTypes/<Имя>.xml`, `ChartsOfCharacteristicTypes/<Имя>/` |
| `Reports/` | `Report` | Отчеты.<Имя>, Отчет.<Имя> | Отчёты, в том числе СКД | `Reports/<Имя>.xml`, `Reports/<Имя>/` |
| `DataProcessors/` | `DataProcessor` | Обработки.<Имя>, Обработка.<Имя> | Обработки, помощники, загрузки, выгрузки | `DataProcessors/<Имя>.xml`, `DataProcessors/<Имя>/` |
| `BusinessProcesses/` | `BusinessProcess` | БизнесПроцессы.<Имя> | Маршруты бизнес-процессов | `BusinessProcesses/<Имя>.xml`, `BusinessProcesses/<Имя>/` |
| `Tasks/` | `Task` | Задачи.<Имя> | Задачи бизнес-процессов | `Tasks/<Имя>.xml`, `Tasks/<Имя>/` |
| `DocumentJournals/` | `DocumentJournal` | ЖурналыДокументов.<Имя> | Журналы документов | `DocumentJournals/<Имя>.xml`, `DocumentJournals/<Имя>/` |
| `DocumentNumerators/` | `DocumentNumerator` | НумераторыДокументов.<Имя> | Правила нумерации | `DocumentNumerators/<Имя>.xml`, `DocumentNumerators/<Имя>/` |
| `Enums/` | `Enum` | Перечисления.<Имя>.<Значение> | Перечисления | `Enums/<Имя>.xml`, `Enums/<Имя>/` |
| `Constants/` | `Constant` | Константы.<Имя> | Константы конфигурации | `Constants/<Имя>.xml`, `Constants/<Имя>/` |
| `DefinedTypes/` | `DefinedType` | Используется в описаниях типов | Определяемые типы | `DefinedTypes/<Имя>.xml`, `DefinedTypes/<Имя>/` |
| `FilterCriteria/` | `FilterCriterion` | КритерииОтбора.<Имя> | Связанные отборы метаданных | `FilterCriteria/<Имя>.xml`, `FilterCriteria/<Имя>/` |

## Общие объекты

| Папка | XML-тип | BSL-синтаксис | Назначение | XML и каталог объекта |
|---|---|---|---|---|
| `CommonModules/` | `CommonModule` | <ИмяМодуля>.<Метод>() | Общая серверная, клиентская и интеграционная логика | `CommonModules/<Имя>.xml`, `CommonModules/<Имя>/` |
| `CommonForms/` | `CommonForm` | ПолучитьОбщуюФорму("<Имя>") | Общие управляемые формы | `CommonForms/<Имя>.xml`, `CommonForms/<Имя>/` |
| `CommonCommands/` | `CommonCommand` | Команда интерфейса / API платформы | Общие команды | `CommonCommands/<Имя>.xml`, `CommonCommands/<Имя>/` |
| `CommandGroups/` | `CommandGroup` | Нет прямого BSL-обращения | Группы команд интерфейса | `CommandGroups/<Имя>.xml`, `CommandGroups/<Имя>/` |
| `CommonAttributes/` | `CommonAttribute` | Реквизит объекта | Общие реквизиты | `CommonAttributes/<Имя>.xml`, `CommonAttributes/<Имя>/` |
| `CommonTemplates/` | `CommonTemplate` | ПолучитьОбщийМакет("<Имя>") | Макеты, шаблоны, печатные формы | `CommonTemplates/<Имя>.xml`, `CommonTemplates/<Имя>/` |
| `CommonPictures/` | `CommonPicture` | Ссылка в форме или макете | Общие изображения | `CommonPictures/<Имя>.xml`, `CommonPictures/<Имя>/` |
| `StyleItems/` | `StyleItem` | Свойства формы и элементов | Стили интерфейса | `StyleItems/<Имя>.xml`, `StyleItems/<Имя>/` |
| `SettingsStorages/` | `SettingsStorage` | ХранилищаНастроек.<Имя> | Хранилища пользовательских настроек | `SettingsStorages/<Имя>.xml`, `SettingsStorages/<Имя>/` |
| `Languages/` | `Language` | Используется в метаданных | Языки конфигурации | `Languages/<Имя>.xml`, `Languages/<Имя>/` |
| `Subsystems/` | `Subsystem` | Нет прямого BSL-обращения | Подсистемы и разделы интерфейса | `Subsystems/<Имя>.xml`, `Subsystems/<Имя>/` |
| `FunctionalOptions/` | `FunctionalOption` | ПолучитьФункциональнуюОпцию("<Имя>") | Включение функциональности | `FunctionalOptions/<Имя>.xml`, `FunctionalOptions/<Имя>/` |
| `FunctionalOptionsParameters/` | `FunctionalOptionParameter` | Используется при расчёте опции | Параметры функциональных опций | `FunctionalOptionsParameters/<Имя>.xml`, `FunctionalOptionsParameters/<Имя>/` |
| `SessionParameters/` | `SessionParameter` | ПараметрыСеанса.<Имя> | Параметры сеанса | `SessionParameters/<Имя>.xml`, `SessionParameters/<Имя>/` |

## Интеграции

| Папка | XML-тип | BSL-синтаксис | Назначение | XML и каталог объекта |
|---|---|---|---|---|
| `ExchangePlans/` | `ExchangePlan` | ПланыОбмена.<Имя>, ПланОбмена.<Имя> | Регистрация изменений и обмены | `ExchangePlans/<Имя>.xml`, `ExchangePlans/<Имя>/` |
| `HTTPServices/` | `HTTPService` | HTTP-запросы, обработчики BSL | HTTP API | `HTTPServices/<Имя>.xml`, `HTTPServices/<Имя>/` |
| `WebServices/` | `WebService` | SOAP-вызовы, экспортные методы | SOAP web-сервисы | `WebServices/<Имя>.xml`, `WebServices/<Имя>/` |
| `WSReferences/` | `WSReference` | Создание WS-прокси | Ссылки на внешние web-сервисы | `WSReferences/<Имя>.xml`, `WSReferences/<Имя>/` |
| `XDTOPackages/` | `XDTOPackage` | ФабрикаXDTO.Создать(...) | XDTO-типы и XML-схемы | `XDTOPackages/<Имя>.xml`, `XDTOPackages/<Имя>/` |
| `IntegrationServices/` | `IntegrationService` | Зависит от описания сервиса | Сервисы интеграционной платформы | `IntegrationServices/<Имя>.xml`, `IntegrationServices/<Имя>/` |
| `EventSubscriptions/` | `EventSubscription` | Обработчик общего модуля | Подписки на события объектов | `EventSubscriptions/<Имя>.xml`, `EventSubscriptions/<Имя>/` |

## Администрирование

| Папка | XML-тип | BSL-синтаксис | Назначение | XML и каталог объекта |
|---|---|---|---|---|
| `Roles/` | `Role` | ПравоДоступа(...) | Роли и права доступа | `Roles/<Имя>.xml`, `Roles/<Имя>/` |
| `ScheduledJobs/` | `ScheduledJob` | Вызов экспортного метода общего модуля | Регламентные задания | `ScheduledJobs/<Имя>.xml`, `ScheduledJobs/<Имя>/` |

| Объект | Назначение |
|---|---|
| `Ext/` | Модуль приложения и служебные модули |
| `Configuration.xml` | Полный состав конфигурации (корень) |
| `ConfigDumpInfo.xml` | Служебный файл выгрузки, не используется в BSL |
| `docs/` | Документация репозитория |

## Типовая структура объекта

```text
<Папка>/
├── <Имя>.xml
└── <Имя>/
    ├── Ext/
    │   ├── ObjectModule.bsl
    │   └── ManagerModule.bsl
    ├── Forms/
    │   ├── <Форма>.xml
    │   └── <Форма>/
    │       └── Ext/
    │           ├── Form.xml
    │           └── Form/
    └── Templates/
```

Фактический состав зависит от типа объекта. Для общих модулей модуль лежит в `CommonModules/<Имя>/Ext/Module.bsl`. Отсутствие `ObjectModule.bsl`, `ManagerModule.bsl` или модуля формы необходимо подтверждать листингом каталога конкретного объекта.

## Правила поиска

### По синтаксису BSL

Таблица соответствий конструкций и папок — в `PERPLEXITY_USAGE.md`, раздел 3.

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

- `Configuration.xml` размером более 1 МБ может не открываться через GitHub Contents API; использовать raw URL или приложенный файл (см. `AI_RULES.md`, раздел 11).
- `ConfigDumpInfo.xml` — служебный файл выгрузки, не использовать как источник прикладной логики.
- `README.md`, `TOP_OBJECTS_ZUP.md` и прочие MD-файлы являются навигационными материалами; полный состав объектов подтверждает только `Configuration.xml`.
- Не делать вывод о наличии BSL только по типу метаданных: проверять фактический каталог `Ext/`.
