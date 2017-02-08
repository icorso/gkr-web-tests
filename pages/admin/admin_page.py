# coding=utf-8
from krtech.elements.list import List

from pages import page, By
from pages.gkr_page import GkrPage


@page(u"Страница администрировния", By.XPATH, "//div[child::div[contains(text(),'Администрирование')]]")
class AdminPage(GkrPage):
    ADMIN_MENU = List(u"Меню администрирования", By.XPATH, ".//ul[@class='admin-menu']/li/a")
