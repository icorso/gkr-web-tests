# coding=utf-8
from krtech.elements.select import Select

from elements.admin_schedule_table import AdminScheduleTable
from pages import page, BaseElement, By
from pages.gkr_page import GkrPage


@page("Управление расписанием", By.XPATH, "//div[child::div[contains(text(),'Управление расписанием')]]")
class SchedulePage(GkrPage):

    SCHEDULE_LIST = Select("Список расписаний", By.ID, "scheduleList")
    DUPLICATE = BaseElement("Кнопка 'Дублировать план'", By.XPATH, ".//button[text()='Дублировать план']")
    SAVE = BaseElement("Кнопка 'Сохранить план'", By.XPATH, ".//button[text()='Сохранить план']")
    DELETE = BaseElement("Кнопка 'Удалить план'", By.XPATH, ".//button[text()='Удалить план']")
    SETTINGS_TABLE = AdminScheduleTable("Таблица параметров плана'", By.XPATH, ".//table[@class='table']")
    SUCCESS_MESSAGE = BaseElement("Сообщение об успешном действии", By.ID, "successlabel")
    ERROR_MESSAGE = BaseElement("Сообщение об ошибке", By.ID, "errorLabel")
