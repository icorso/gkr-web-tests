# coding=utf-8
from krtech.elements.calendar import Calendar
from pages import page, BasePage, BaseElement, By, Select, List, Input

from pages.common_blocks import AddressDialog
from pages.gkr_page import GkrPage


@page(u"Форма 'Регистрация в очереди'", By.ID, "history")
class QueuePage(GkrPage):

    @property
    def address_dialog(self):
        return AddressDialog(self.config)

    SURNAME = Input("Поле 'Фамилия'", By.XPATH, ".//div[child::*[contains(text(),' Фамилия')]]")
    NAME = Input("Поле 'Имя'", By.XPATH, ".//div[child::*[contains(text(),' Имя')]]")
    PATRONYMIC = Input("Поле 'Отчество'", By.XPATH, ".//div[child::*[contains(text(),' Отчество')]]")
    BIRTHDAY = Input("Поле 'Дата рождения'", By.XPATH, ".//div[child::*[contains(text(),'Дата рождения')]]")
    EMAIL = Input("Поле 'Email'", By.XPATH, ".//div[child::*[contains(text(),' E-mail')]]")
    MOBILE = Input("Поле 'Мобильный телефон'", By.XPATH, ".//div[child::*[contains(text(),' Мобильный')]]")
    HOME_PHONE = Input("Поле 'Дом. телефон'", By.XPATH, ".//div[child::*[contains(text(),' Домашний')]]")
    PASSPORT_SERIAL = Input("Поле 'Серия паспорта'", By.XPATH, ".//div[child::*[contains(text(),'ерия паспорта')]]")
    PASSPORT_NUMBER = Input("Поле 'Номер паспорта'", By.XPATH, ".//div[child::*[contains(text(),'Номер паспорта')]]")
    ISSUE = Input("Поле 'Кем выдан'", By.XPATH, ".//div[child::*[contains(text(),'Кем выдан')]]")
    ISSUE_DATE = Input("Поле 'Когда выдан'", By.XPATH, ".//div[child::*[contains(text(),'Когда выдан')]]")

    DEPARTMENT_SELECT = Select(u"Список 'Отделение'", By.ID, "department_id")
    DEPARTMENT_TEXT = BaseElement(u"Текст 'Отделение'", By.ID, "department_name")
    SERVICE = Select(u"Список 'Услуга'", By.ID, "serviceId")
    OBJECT_TYPE = Select(u"Список 'Тип объекта недвижимости'", By.ID, "objectsCount")
    SUGGEST = List(u"Саджест 'Адрес объекта недвижимости'", By.XPATH, "//li[contains(@id,'ui-id')]")
    CITY = Select(u"Список 'Район / Город'", By.ID, "address.region")
    LOCALITY = Input(u"Поле 'Населенный пункт'", By.XPATH, ".//div[./label[contains(text(),'Населенный пункт')]]")
    STREET = Input(u"Поле 'Улица'", By.XPATH, ".//div[./label[contains(text(),'Улица')]]")
    HOUSE = Input(u"Поле 'Дом'", By.XPATH, ".//div[./label[contains(text(),'Дом')]]")
    FLAT = Input(u"Поле 'Квартира'", By.XPATH, ".//div[./label[contains(text(),'Квартира')]]")
    OTHER = Input(u"Поле 'Иное'", By.XPATH, ".//div[./label[contains(text(),'Адрес с правоустанавливающего')]]")
    CAPTCHA = Input(u"Поле 'Текст с картинки'", By.XPATH, ".//div[./label[contains(text(),'Введите текст')]]")
    STAT_INDICATOR = BaseElement("Уровень занятости отдела", By.XPATH, ".//span[@class='statistics-indicator__value']")
    ERROR_TEXT = List("Сообщения с ошибками", By.XPATH, "//div[@class='text_error']")
    QUEUE_FULL_MESSAGE = BaseElement("Сообщения о следующей дате открытия", By.XPATH,
                                     ".//div[@id='no-time' and not(contains(@style,'display'))]")
    CALENDAR = Calendar("Календарь", By.XPATH, "//div[contains(@class,'datetime')]")
    SUBMIT = BaseElement("Кнопка 'Получить талон'", By.ID, "submit")
