# BSL index: CommonForms/ЗагрузкаКандидатаПоUrlРезюме

Generator: rebuild_ai 2.0
Source snapshot commit: 017fc906aca6a153d10c59368f8fd591aa6a4ee7
Navigation only: read the source method body before describing behavior.
Header recognition is heuristic, not a complete BSL parser.
An absent index entry does not prove an absent method.

## CommonForms/ЗагрузкаКандидатаПоUrlРезюме/Ext/Form/Module.bsl

- Module: Модуль формы
- Lines: 77
- Bytes: 2875
- Source SHA-256: 08f3505c5dea49c482430a655de2bb39d587e38604e03ccf2afe25604f512de9

| Line | Kind | Name | Parameters | Export | Directives |
|---|---|---|---|---|---|
| 4 | Процедура | ПриСозданииНаСервере | Отказ, СтандартнаяОбработка |  | &НаСервере |
| 9 | Процедура | ПриОткрытии | Отказ |  | &НаКлиенте |
| 14 | Процедура | ОбработкаОповещения | ИмяСобытия, Параметр, Источник |  | &НаКлиенте |
| 27 | Процедура | ПродолжитьРаботу | Команда |  | &НаКлиенте |
| 36 | Процедура | НачатьЗагрузкуКандидата |  |  | &НаКлиенте |
| 42 | Процедура | ЗаполнитьАдресРезюмеИзБуфераОбмена |  |  | &НаКлиенте |
| 60 | Функция | ДоступнаРаботаСБуферомОбмена |  |  | &НаКлиенте |
| 71 | Функция | ЭтоАдресРезюме | СтрокаИзБуфера |  | &НаСервереБезКонтекста |
