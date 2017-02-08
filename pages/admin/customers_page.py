# coding=utf-8
from krtech.elements.input import Input
from krtech.elements.list import List

from pages import page, BaseElement, By
from pages.gkr_page import GkrPage


@page(u"Список пользователей", By.XPATH, "//div[child::div/h6[contains(text(),'Список пользователей')]]")
class CustomersAdminPage(GkrPage):

    TERM_FIELD = Input(u"Поле 'Поиск'", By.XPATH, ".//div[child::input[@name='term']]")
    SEARCH_SUBMIT = BaseElement(u"Кнопка 'Поиск'", By.XPATH, ".//input[@type='submit']")
    TABLE = List(u"Таблица пользователей", By.XPATH, ".//tbody/tr")


@page(u"Список неподтвержденных пользователей", By.XPATH,
      "//div[child::div/h6[contains(text(),'Список неподтвержденных пользователей')]]")
class TCustomersAdminPage(GkrPage):

    TERM_FIELD = Input(u"Поле 'Поиск'", By.XPATH, ".//div[child::input[@name='term']]")
    SEARCH_SUBMIT = BaseElement(u"Кнопка 'Поиск'", By.XPATH, ".//input[@type='submit']")
    TABLE = List(u"Таблица пользователей", By.XPATH, ".//tbody/tr")
