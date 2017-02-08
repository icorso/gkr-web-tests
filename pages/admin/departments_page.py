# coding=utf-8
from krtech.elements.base_element import BaseElement
from krtech.elements.checkbox import Checkbox
from krtech.elements.input import Input
from krtech.elements.select import Select

from elements.admin_departments import AdminDepartmentsTable
from pages import page, BasePage, By
from pages.gkr_page import GkrPage


@page(u"Администрирование отделений", By.XPATH, "//div[child::div[contains(text(),'Отделения')]]")
class DepartmentsAdminPage(GkrPage):

    DEPARTMENTS_LIST = Select("Список отделений", By.ID, "departList")
    NEW_DEPARTMENT = BaseElement("Кнопка 'Добавить отделение'", By.ID, "addDepartmentBut")
    NAME = Input("Поле 'Имя'", By.XPATH, ".//tr[child::td='Название']")
    DESC = Input("Поле 'Краткое описание'", By.XPATH, ".//tr[child::td='Краткое описание']")
    SCHEDULE = Select("Список 'Расписание'", By.XPATH, ".//select[@ng-model='curSchedule']")
    CALENDAR = Select("Список 'Календарь'", By.XPATH, ".//select[@ng-model='curCalendar']")
    PHYS_CHECKBOX = Checkbox("Чекбокс 'Процент записи в отделение для физлиц'",
                             By.XPATH, ".//input[@ng-model='fizActive']")
    PHYS_INPUT = BaseElement("Поле 'Процент записи в отделение для физлиц'",
                             By.XPATH, ".//input[@ng-model='fizPercent']")
    LEGAL_CHECKBOX = Checkbox("Чекбокс 'Процент записи в отделение для юрлиц'",
                              By.XPATH, ".//input[@ng-model='urActive']")
    LEGAL_INPUT = BaseElement("Поле 'Процент записи в отделение для юрлиц'",
                              By.XPATH, ".//input[@ng-model='urPercent']")
    REGIONS_SELECT = Select("Список 'Связанный территориальный регион'", By.XPATH, ".//select[@ng-model='newItem']")
    REGIONS_LIST = AdminDepartmentsTable("Список выбранных территориальных регионов",
                                         By.XPATH, ".//table[@class='table']")
    SAVE = BaseElement("Кнопка 'Сохранить'", By.ID, "saveBut")
    SAVED = BaseElement("Сообщение 'Сохранено'", By.ID, "saved")
