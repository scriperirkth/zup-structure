# BSL index: WebServices/Exchange_3_0_1_1

Generator: rebuild_ai 2.0
Source snapshot commit: 017fc906aca6a153d10c59368f8fd591aa6a4ee7
Navigation only: read the source method body before describing behavior.
Header recognition is heuristic, not a complete BSL parser.
An absent index entry does not prove an absent method.

## WebServices/Exchange_3_0_1_1/Ext/Module.bsl

- Module: Модуль
- Lines: 139
- Bytes: 8393
- Source SHA-256: 1cef513573f69dff9fcc4366d3e3d1bd613e9e2ecb518b25c27d8d1c9282dfb7

| Line | Kind | Name | Parameters | Export | Directives |
|---|---|---|---|---|---|
| 15 | Функция | ВыполнитьВыгрузку | ИмяПланаОбмена, КодУзлаИнформационнойБазы, ХранилищеСообщенияОбмена |  |  |
| 22 | Функция | ВыполнитьВыгрузкуДанных | ИмяПланаОбмена, КодУзлаИнформационнойБазы, ИдентификаторФайлаСтрокой, ДлительнаяОперация, ИдентификаторОперации, ДлительнаяОперацияРазрешена |  |  |
| 31 | Функция | ВыполнитьЗагрузку | ИмяПланаОбмена, КодУзлаИнформационнойБазы, ХранилищеСообщенияОбмена |  |  |
| 39 | Функция | ВыполнитьЗагрузкуДанных | ИмяПланаОбмена, КодУзлаИнформационнойБазы, ИдентификаторФайлаСтрокой, ДлительнаяОперация, ИдентификаторОперации, ДлительнаяОперацияРазрешена |  |  |
| 48 | Функция | ПолучитьПараметрыИнформационнойБазы | ИмяПланаОбмена, КодУзла, СообщениеОбОшибке |  |  |
| 56 | Функция | СоздатьУзелОбменаДанными | ПараметрыXDTO |  |  |
| 63 | Функция | УдалитьУзелОбменаДанными | ИмяПланаОбмена, ИдентификаторУзла |  |  |
| 70 | Функция | ПолучитьСостояниеДлительнойОперации | ИдентификаторОперации, СтрокаСообщенияОбОшибке |  |  |
| 78 | Функция | PrepareGetFile | FileId, BlockSize, TransferId, PartQuantity |  |  |
| 85 | Функция | GetFilePart | TransferId, PartNumber, PartData |  |  |
| 92 | Функция | ReleaseFile | TransferId |  |  |
| 105 | Функция | PutFilePart | TransferId, PartNumber, PartData |  |  |
| 112 | Функция | SaveFileFromParts | TransferId, PartQuantity, FileId |  |  |
| 119 | Функция | PutMessageForDataMatching | ИмяПланаОбмена, ИдентификаторУзла, ИдентификаторФайла |  |  |
| 127 | Функция | Ping |  |  |  |
| 133 | Функция | TestConnection | ИмяПланаОбмена, КодУзла, Результат |  |  |
