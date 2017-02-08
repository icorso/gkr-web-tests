# coding=utf-8
from elements.admin_news_row import AdminNewsTable
from pages import page, BaseElement, By
from pages.gkr_page import GkrPage


@page(u"Администрирование новостей", By.XPATH, "//form[..//child::*[contains(text(),'Список новостей')]]")
class NewsAdminPage(GkrPage):

    CREATE_NEWS = BaseElement("Кнопка 'Создать новость'", By.XPATH, ".//a[@class='button_type1']")
    NEWS_LIST = AdminNewsTable("Список администрируемых новостей'", By.XPATH, ".//tbody")
