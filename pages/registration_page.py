# coding=utf-8
from krtech.decorators import page
from krtech.elements.base_element import BaseElement
from krtech.elements.input import Input
from selenium.webdriver.common.by import By

from pages.gkr_page import GkrPage


@page("Форма 'Регистрация в системе'", By.XPATH, "//*[@id='userDetailsForm']")
class RegistrationPage(GkrPage):

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
    INN = Input("Поле 'Инн'", By.XPATH, ".//div[child::*[contains(text(),'ИНН')]]")

    # TODO заменить на типизированный элемент "tab"
    USER_TYPE = BaseElement("Таб 'Физическим лицам'", By.XPATH, ".//li[contains(text(),'Физическим лицам')]")
    LEGAL_TYPE = BaseElement("Таб 'Юридическим лицам'", By.XPATH, ".//li[contains(text(),'Юридическим лицам')]")
    USER_HEADER = BaseElement("Заголовок формы 'Личные данные'", By.ID, "personal_data_label")
    LEGAL_HEADER = BaseElement("Заголовок формы 'Данные компании'", By.ID, "company_data_label")
    INFO = BaseElement("Сообщение", By.XPATH, ".//ul[contains(@class,'body_history')]/li")

    ERROR = BaseElement("Сообщение об ошибке", By.XPATH, ".//div[contains(@class,'errors')]/p")
    CHECKBOX = BaseElement("Чекбокс 'Согласен на обр.данных'", By.ID, "i-agree")
    SUBMIT = BaseElement("Кнопка подтверждения", By.XPATH, ".//button[contains(text(),'зарегистрироваться')]")
