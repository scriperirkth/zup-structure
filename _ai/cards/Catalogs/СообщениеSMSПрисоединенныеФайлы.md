# Справочник.СообщениеSMSПрисоединенныеФайлы

- Тип XML: Catalog
- Синоним: Присоединенные файлы (Сообщение SMS)
- Источник: Catalogs/СообщениеSMSПрисоединенныеФайлы.xml
- Каталог объекта: Catalogs/СообщениеSMSПрисоединенныеФайлы/ (есть)
- Построено из коммита: 017fc906aca6a153d10c59368f8fd591aa6a4ee7
- Статус: ПОДТВЕРЖДЕНО XML (сгенерировано rebuild_ai 2.0; при расхождении верен исходный XML)
- Autonumbering: false
- CheckUnique: false
- Hierarchical: false
- HierarchyType: HierarchyFoldersAndItems
- CodeLength: 0
- DescriptionLength: 150
- CodeType: String
- ChoiceMode: BothWays
- EditType: InDialog
- DataLockControlMode: Managed
- InputByString: Catalog.СообщениеSMSПрисоединенныеФайлы.StandardAttribute.Description

### Реквизиты (20)

| Имя | Синоним | Тип | FillChecking=ShowError |
|---|---|---|---|
| Автор | Автор | CatalogRef.УчетныеЗаписиСинхронизацииФайлов \| CatalogRef.Пользователи | Да |
| ВладелецФайла | Размещение | DocumentRef.СообщениеSMS |  |
| ДатаЗаема | Дата заема | Дата(DateTime) |  |
| ДатаМодификацииУниверсальная | Дата изменения (универсальное время) | Дата(DateTime) |  |
| ДатаСоздания | Дата создания | Дата(DateTime) | Да |
| Зашифрован | Зашифрован | Булево |  |
| Изменил | Отредактировал | CatalogRef.УчетныеЗаписиСинхронизацииФайлов \| CatalogRef.Пользователи |  |
| ИндексКартинки | Индекс значка | Число(10,0) |  |
| Описание | Описание | Строка(неогр.) |  |
| ПодписанЭП | Подписан электронно | Булево |  |
| ПутьКФайлу | Путь к файлу | Строка(неогр.) |  |
| Размер | Размер (байт) | Число(10,0) |  |
| Расширение | Расширение | Строка(10) |  |
| Редактирует | Редактирует | CatalogRef.УчетныеЗаписиСинхронизацииФайлов \| CatalogRef.Пользователи |  |
| СтатусИзвлеченияТекста | Статус извлечения текста | EnumRef.СтатусыИзвлеченияТекстаФайлов |  |
| ТекстХранилище | Текст | ХранилищеЗначения |  |
| ТипХраненияФайла | Тип хранения файла | EnumRef.ТипыХраненияФайлов | Да |
| Том | Том | CatalogRef.ТомаХраненияФайлов |  |
| ФайлХранилище | Временное хранилище файла | ХранилищеЗначения |  |
| ХранитьВерсии | Хранить версии | Булево |  |

### BSL-модули

- Catalogs/СообщениеSMSПрисоединенныеФайлы/Ext/ManagerModule.bsl (2785 байт)
- Catalogs/СообщениеSMSПрисоединенныеФайлы/Ext/ObjectModule.bsl (3 байт)

Методы: _ai/modules/Catalogs/СообщениеSMSПрисоединенныеФайлы.md

- Source XML SHA-256: 0cb25a5dccd0c97af937e8509e99e17b9b5006a5e13af6226ef6e2a307dc4d03
- This is a generated summary, not the complete XML.
- FillChecking=ShowError is an XML setting; runtime validation requires BSL analysis.
