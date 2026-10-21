#Область ОбработчикиСобытийФормы

&НаСервере
Процедура ПриСозданииНаСервере(Отказ, СтандартнаяОбработка)
	
	ОписаниеВебСервисов = ИнтеграцияС1СДокументооборотБазоваяФункциональность.ОписаниеВебСервисов();
	
	// АдаптацияИнтерфейса
	Если ОбщегоНазначенияКлиентСервер.ЭтоВариантИнтерфейса85() Тогда
		УстановитьСтиль(
			"<style type=""text/css"">
			|  body {font-family: Arial; font-size: 10pt; width: 99%; max-width: 1890px}
			|  h1 {font-size: 16pt}
			|  h2 {font-size: 14pt}
			|  h3 {font-size: 12pt; margin-top: 20pt; margin-bottom: 10pt; BORDER-BOTTOM: sienna 1px solid; PADDING-BOTTOM: 2px; COLOR: var(--colorOrange70)}
			|  h4 {font-size: 10pt}
			|  a:link, a:visited {COLOR: var(--colorLightBlue70); TEXT-DECORATION: none}
			|  a:hover {COLOR: var(--colorLightBlue70); TEXT-DECORATION: underline}
			|  p.Usual {MARGIN-TOP: 10px}
			|  table {border-collapse: collapse; font-size: 10pt; width: 99%}
			|  td {padding: 3px; border: 1px solid var(--colorText90); vertical-align: top}
			|  td.description {padding: 0px; border: 0px}
			|  td.head {padding: 3px; border: 1px solid var(--colorText90); background-color: var(--colorBack20)}
			|  td.classes {padding: 3px; border: 1px white; vertical-align: top}
			|  pre {background-color: var(--colorBack20); width: 99%}
			|  .src_adm, .src_dev, .src_res {margin-top: 0pt; background: none repeat scroll 0% 0% var(--colorBack10); font: Courier New}
			|  pre.src_dev {color: var(--colorViolet60)}
			|  pre.src_dev span.comment {color: var(--colorGreen70)}
			|  pre.src_dev span.string, pre.src_dev span.number {color: var(--colorBack90)}
			|  pre.src_dev span.keyword, pre.src_dev span.operator {color: var(--colorRed50)}
			|</style>");
	КонецЕсли;
	// Конец АдаптацияИнтерфейса
	
	Параметры.Свойство("Ссылка", Ссылка);
	
КонецПроцедуры

&НаКлиенте
Процедура ПриОткрытии(Отказ)
	
	Если ЗначениеЗаполнено(Ссылка) Тогда
		ПодключитьОбработчикОжидания("ПерейтиКСсылке", 0.2, Истина);
	КонецЕсли;
	
КонецПроцедуры

#КонецОбласти

#Область ОбработчикиСобытийЭлементовШапкиФормы

&НаКлиенте
Процедура ПолеHTMLДокументаПриНажатии(Элемент, ДанныеСобытия, СтандартнаяОбработка)
	
	СтандартнаяОбработка = Ложь;
	Если Не ЗначениеЗаполнено(ДанныеСобытия.HRef) Тогда
		Возврат;
	КонецЕсли;
	
	Позиция = СтрНайти(ДанныеСобытия.HRef, "#", НаправлениеПоиска.СКонца);
	Ссылка = Сред(ДанныеСобытия.HRef, Позиция + 1);
	ПодключитьОбработчикОжидания("ПерейтиКСсылке", 0.2, Истина);
	
КонецПроцедуры

#КонецОбласти

#Область СлужебныеПроцедурыИФункции

&НаКлиенте
Процедура ПерейтиКСсылке()
	
	// При проблемах с совместимостью браузеров откроем документ без позиционирования
	// на ссылке, проглотив исключение как некритичное.
	Попытка
		Документ = Элементы.ПолеHTMLДокумента.Документ;
		Для Каждого Элемент Из Документ.querySelectorAll(СтрШаблон("a[name=""%1""]", Ссылка)) Цикл
			Элемент.scrollIntoView(Истина);
			Прервать;
		КонецЦикла;
	Исключение
		Возврат;
	КонецПопытки;
	
КонецПроцедуры

&НаСервере
Процедура УстановитьСтиль(Стиль)
	
	Начало = СтрНайти(ОписаниеВебСервисов, "<style");
	Конец = СтрНайти(ОписаниеВебСервисов, "</style>");
	
	ОписаниеВебСервисов = Лев(ОписаниеВебСервисов, Начало - 1) + Стиль + Сред(ОписаниеВебСервисов, Конец + 8);
	
КонецПроцедуры

#КонецОбласти