# METADATA_MAP.md — Карта метаданных ЗУП КОРП

> Репозиторий: `scriperirkth/zup-structure`
> Первичный состав: `Configuration.xml`.
> Производный реестр: `_ai/objects`.
> Правила: `AI_RULES.md`.

## Навигация

1. Прочитать `_ai/VERSION.md`.
2. Найти тип в `_ai/objects.md`.
3. Прочитать таблицу типа и её продолжения.
4. Перейти к карточке, если она сформирована.
5. Для точных свойств прочитать исходный XML.
6. Для поведения прочитать BSL, используя индекс как навигацию.

Наличие строки в этой карте не доказывает наличие объектов данного типа в конкретном снимке. Фактический набор типов и объектов устанавливается по реестру.

## Соответствия XML-типов и каталогов

| XML-тип | Каталог |
|---|---|
| AccumulationRegister | `AccumulationRegisters` |
| AccountingRegister | `AccountingRegisters` |
| BusinessProcess | `BusinessProcesses` |
| CalculationRegister | `CalculationRegisters` |
| Catalog | `Catalogs` |
| ChartOfAccounts | `ChartsOfAccounts` |
| ChartOfCalculationTypes | `ChartsOfCalculationTypes` |
| ChartOfCharacteristicTypes | `ChartsOfCharacteristicTypes` |
| CommandGroup | `CommandGroups` |
| CommonAttribute | `CommonAttributes` |
| CommonCommand | `CommonCommands` |
| CommonForm | `CommonForms` |
| CommonModule | `CommonModules` |
| CommonPicture | `CommonPictures` |
| CommonTemplate | `CommonTemplates` |
| Constant | `Constants` |
| DataProcessor | `DataProcessors` |
| DefinedType | `DefinedTypes` |
| DocumentJournal | `DocumentJournals` |
| DocumentNumerator | `DocumentNumerators` |
| Document | `Documents` |
| Enum | `Enums` |
| EventSubscription | `EventSubscriptions` |
| ExchangePlan | `ExchangePlans` |
| ExternalDataSource | `ExternalDataSources` |
| FilterCriterion | `FilterCriteria` |
| FunctionalOption | `FunctionalOptions` |
| FunctionalOptionsParameter | `FunctionalOptionsParameters` |
| HTTPService | `HTTPServices` |
| InformationRegister | `InformationRegisters` |
| IntegrationService | `IntegrationServices` |
| Language | `Languages` |
| PaletteColor | `PaletteColors` |
| Report | `Reports` |
| Role | `Roles` |
| ScheduledJob | `ScheduledJobs` |
| Sequence | `Sequences` |
| SessionParameter | `SessionParameters` |
| SettingsStorage | `SettingsStorages` |
| StyleItem | `StyleItems` |
| Subsystem | `Subsystems` |
| Task | `Tasks` |
| WebService | `WebServices` |
| WSReference | `WSReferences` |
| XDTOPackage | `XDTOPackages` |

Неизвестный тип не сопоставлять автоматически по окончанию имени.

## Исходный XML и каталог объекта

Общая схема:

```text
<Папка>/<Имя>.xml
<Папка>/<Имя>/
```

Каталог объекта может отсутствовать, если дополнительные файлы не выгружены или не требуются.

XML объекта расположен рядом с каталогом, а не обязательно внутри него.

## Модули

| Назначение | Навигационный путь |
|---|---|
| Объект | `<Папка>/<Имя>/Ext/ObjectModule.bsl` |
| Менеджер | `<Папка>/<Имя>/Ext/ManagerModule.bsl` |
| Набор записей | `<Папка>/<Имя>/Ext/RecordSetModule.bsl` |
| Общий модуль | `CommonModules/<Имя>/Ext/Module.bsl` |
| Форма объекта | `<Папка>/<Имя>/Forms/<Форма>/Ext/Form/Module.bsl` |

Пути в таблице — ориентиры. Для конкретного типа и объекта проверять дерево и индекс.

Служебные модули конфигурации искать в корневом `Ext/`. Производный индекс для этой группы — `_ai/modules/Ext/Ext.md`, если он создан.

Не делать вывод о наличии или отсутствии модуля только по виду объекта.

## Формы и макеты

Пример формы объекта:

```text
<Папка>/<Имя>/Forms/<Форма>.xml
<Папка>/<Имя>/Forms/<Форма>/Ext/Form.xml
<Папка>/<Имя>/Forms/<Форма>/Ext/Form/Module.bsl
```

Макеты объекта искать в:

```text
<Папка>/<Имя>/Templates/
```

Состав и расширения файлов зависят от вида формы или макета. Наличие текста, MXL, двоичных и архивных ресурсов проверять по фактической выгрузке.

Не исключать файлы исходников только потому, что их расширение `.zip` или `.bin`.

## Производные файлы

| Вид | Путь |
|---|---|
| Реестр типа | `_ai/objects/<Папка>.md` |
| Карточка | `_ai/cards/<Папка>/<Имя>.md` |
| Индекс BSL | `_ai/modules/<Папка>/<Имя>.md` |

Продолжения имеют имена `.part2.md`, `.part3.md` и далее.

Карточки создаются только для выбранного генератором набора типов. Отсутствие карточки не означает отсутствие XML или объекта.

Карточка не содержит все свойства XML. Индекс BSL не содержит тело метода.

## Служебные файлы и каталоги

| Путь | Назначение |
|---|---|
| `Configuration.xml` | Свойства и зарегистрированный состав |
| `ConfigDumpInfo.xml` | Служебные сведения выгрузки |
| `Ext/` | Модули и другие файлы конфигурации |
| `_ai/` | Производные реестры, карточки и индексы |
| `tools/` | Локальные инструменты |
| `docs/` | Документация репозитория, если присутствует |

`ConfigDumpInfo.xml` не подтверждает прикладное поведение.

## Полнота поиска

Для полного списка объектов читать все части актуального реестра.

Для отрицательного вывода разделять:

- объект не зарегистрирован;
- XML-файл не найден;
- каталог не найден;
- модуль не найден в проверенных путях;
- файл недоступен или обрезан.

Правила формулировок и статусы — `AI_RULES.md`, разделы 6 и 7.