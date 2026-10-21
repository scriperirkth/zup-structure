# BSL index: CommonForms/ОтправкаSMS

Generator: rebuild_ai 2.0
Source snapshot commit: 017fc906aca6a153d10c59368f8fd591aa6a4ee7
Navigation only: read the source method body before describing behavior.
Header recognition is heuristic, not a complete BSL parser.
An absent index entry does not prove an absent method.

## CommonForms/ОтправкаSMS/Ext/Form/Module.bsl

- Module: Модуль формы
- Lines: 223
- Bytes: 14156
- Source SHA-256: 15c8b934d96989e762b0a831e4b68dbb953ef072ef9c01a6d5a770c3f63d93c1

| Line | Kind | Name | Parameters | Export | Directives |
|---|---|---|---|---|---|
| 12 | Процедура | ПриСозданииНаСервере | Отказ, СтандартнаяОбработка |  | &НаСервере |
| 46 | Процедура | ПриОткрытии | Отказ |  | &НаКлиенте |
| 55 | Процедура | ДобавлятьОтправителяПриИзменении | Элемент |  | &НаКлиенте |
| 64 | Процедура | Отправить | Команда |  | &НаКлиенте |
| 100 | Процедура | ОтправитьSMS |  |  | &НаСервере |
| 124 | Процедура | ПроверитьСтатусДоставки |  |  | &НаКлиенте |
| 161 | Функция | СтатусДоставки | ИдентификаторСообщения |  | &НаСервереБезКонтекста |
| 184 | Процедура | ТекстИзменениеТекстаРедактирования | Элемент, Текст, СтандартнаяОбработка |  | &НаКлиенте |
| 190 | Функция | ОтправкаSMSНастроена |  |  | &НаСервереБезКонтекста |
| 195 | Функция | ФорматированнаяСтрока | Текст |  | &НаСервереБезКонтекста |
