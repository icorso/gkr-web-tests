# coding=utf-8
from krtech.elements.input import Input
from krtech.elements.select import Select

from elements.admin_services_row import AdminServicesTable
from pages import page, BasePage, BaseElement, By
from pages.gkr_page import GkrPage


@page(u"Управление услугами", By.XPATH, "//div[child::div/h6[contains(text(),'Управление услугами')]]")
class ServicesAdminPage(GkrPage):

    SERVICES_LIST = AdminServicesTable(u"Список услуг (администрирование)", By.XPATH, ".//tbody")
    NAME = Input(u"Поле 'Название'", By.XPATH, ".//div[child::input[@id='name']]")
    STATUS = Select(u"Список 'Отображение услуги на терминале'", By.XPATH, ".//select[@id='status']")
    PREFIX = Input(u"Поле 'Префикс'", By.XPATH, ".//div[child::input[@id='servicePrefix']]")
    GROUP = Select(u"Список 'Группа'", By.XPATH, ".//select[@id='groupId']")
    DURATION = Input(u"Поле 'Регламент услуги'", By.XPATH, ".//div[child::input[@id='duration']]")
    ADDITIONAL_DURATION = Input(u"Поле 'Доп. время на объект недвижимости'", By.XPATH,
                                ".//div[child::input[@id='aditional_duration']]")
    PERCENT_RECORDS = Input(u"Поле 'Максимальный % времени для услуги'", By.XPATH,
                            ".//div[child::input[@id='precentRecords']]")
    PERCENT_RECORDS_ADVANCE = Input(u"Поле 'Максимальный % времени для услуги предв.'", By.XPATH,
                                    ".//div[child::input[@id='precentRecordsAdvance']]")
    CALENDAR = Select(u"Список 'Календарь'", By.XPATH, ".//select[@id='calendar']")
    SCHEDULE = Select(u"Список 'Расписание'", By.XPATH, ".//select[@id='schedule']")

    CLEAN = BaseElement(u"Кнопка 'Очистить форму'", By.XPATH, ".//button[@type='button']")
    SUBMIT = BaseElement(u"Кнопка 'Добавить'", By.XPATH, ".//input[@type='submit']")
