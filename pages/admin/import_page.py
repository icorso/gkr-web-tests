# coding=utf-8
from krtech.elements.checkbox import Checkbox
from krtech.elements.list import List
from krtech.elements.select import Select

from pages import page, BaseElement, By
from pages.gkr_page import GkrPage


@page("Импорт регистраторов", By.XPATH, "//div[child::div/h6[contains(text(),'мпорт')]]")
class ImportPage(GkrPage):

    IMPORT_FILE = BaseElement("Поле добавления файла", By.XPATH, ".//input[@type='file']")
    SUBMIT = BaseElement("Кнопка 'Загрузить файл'", By.XPATH, ".//input[@type='submit']")

    # подстраница Предпросмотр перед импортом регистраторов
    ORGANIZATIONS = Select("Список 'Организация'", By.ID, 'selectSome')
    ADD_CHECKBOX = Checkbox("Чекбокс 'Добавить новых регистраторов'", By.ID, 'addNew1')
    READY_TABLE = List("Таблица 'Готово к импорту'", By.XPATH,
                       ".//div[following-sibling::span[contains(text(),'Готово к импорту')]]//tbody/tr")
    IMPORT_BUTTON = BaseElement("Кнопка 'Импорт'", By.ID, "importButton")

    # подстраница Отчет о импорте
    ADDED = BaseElement("Количество добавленных регистраторов", By.XPATH, u"//div[contains(@class,'type2')]/div[5]/h3")
