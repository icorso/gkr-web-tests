# coding=utf-8
from pages import page, BaseElement, By, List, Input
from pages.gkr_page import GkrPage


@page("Форма 'История регистраций'", By.XPATH, "//form[.//child::*[contains(text(),'История')]]")
class HistoryPage(GkrPage):

    SEARCH_FIELD = Input("Поле ввода критерия поиска", By.XPATH, ".//div[contains(@class,'header_history')]")
    SEARCH_BUTTON = BaseElement("Кнопка 'Поиск'", By.XPATH, ".//input[@value='Поиск']")
    SEARCH_ROWS = List("Таблица истории результатов ", By.XPATH, "//table[@class='table']/tbody/tr")
