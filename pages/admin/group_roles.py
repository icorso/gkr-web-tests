# coding=utf-8
from krtech.elements.base_element import BaseElement
from krtech.elements.list import List
from krtech.elements.select import Select

from pages import page, By
from pages.gkr_page import GkrPage


@page(u"Управление группами ролей", By.XPATH, "//section/div[//child::*[contains(text(),'Управление группами ролей')]]")
class GroupRolesPage(GkrPage):

    GROUP_LIST = Select("Список групп", By.XPATH, ".//td[1]/select")
    ROLE_LIST = List("Список ролей", By.XPATH, ".//tr[contains(@ng-repeat,'item')]")

    GROUP_LIST_COUNT = BaseElement("Счётчик групп", By.XPATH, ".//form/table/tbody/tr[1]/td[1]")
    ROLE_LIST_COUNT = BaseElement("Счётчик ролей", By.XPATH, ".//form/table/tbody/tr[1]/td[2]")

