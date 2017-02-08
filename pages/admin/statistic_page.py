# coding=utf-8
from krtech.elements.select import Select

from elements.table import StatisticTable
from pages import page, BaseElement, By
from pages.gkr_page import GkrPage


@page("Статистика", By.XPATH, "//div[child::div[contains(text(),'Статистика')]]")
class StatisticPage(GkrPage):

    CREATION_DATE = BaseElement("Кнопка фильтра по дате создания", By.XPATH, ".//input[@value='created']")
    ADVANCE_DATE = BaseElement("Кнопка фильтра по дате посещения'", By.XPATH, ".//input[@value='advance']")
    DATE_FROM = BaseElement("Поле дата с", By.ID, "from")
    DATE_TO = BaseElement("Поле дата по", By.ID, "to")
    DEPARTMENT = Select("Список подразделений", By.NAME, "department")
    DETAIL_DAY = BaseElement("Кнопка фильтра по дате создания", By.XPATH, ".//input[@value='day']")
    DETAIL_HOUR = BaseElement("Кнопка фильтра по дате создания", By.XPATH, ".//input[@value='hour']")
    TABLE = StatisticTable("Таблица статистики", By.XPATH, ".//table")
    SUBMIT = BaseElement("Кнопка 'Ок'", By.XPATH, ".//button[@type='submit']")
