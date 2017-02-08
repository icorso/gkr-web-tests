# coding=utf-8
from krtech.elements.input import Input

from pages import page, BaseElement, By
from pages.gkr_page import GkrPage


@page(u"Страница редактирования пользователя администратором",
      By.XPATH, "//div[child::div/h6[contains(text(),'Редактирование пользователя')]]")
class CustomerEditPage(GkrPage):

    NAME = Input("Поле 'Имя'", By.XPATH, ".//li[child::*[@for='name']]")
    SURNAME = Input("Поле 'Фамилия'", By.XPATH, ".//li[child::*[@for='surname']]")
    PATRONYMIC = Input("Поле 'Отчество'", By.XPATH, ".//li[child::*[@for='patronymic']]")
    BIRTHDAY = Input("Поле 'Дата рождения'", By.XPATH, ".//li[child::*[@for='birthday']]")
    LOGIN = Input("Поле 'Логин'", By.XPATH, ".//li[child::*[@for='login']]")
    PASSWORD = Input("Поле 'Паспорт'", By.XPATH, ".//li[child::*[@for='password']]")
    EMAIL = Input("Поле 'Email'", By.XPATH, ".//li[child::*[@for='email']]")
    MOBILE = Input("Поле 'Мобильный телефон'", By.XPATH, ".//div[child::*[@for='mobilePhone']]")
    HOME_PHONE = Input("Поле 'Дом. телефон'", By.XPATH, ".//div[child::*[@for='homePhone']]")

    PASSPORT_SERIAL = Input("Поле 'Серия паспорта'", By.XPATH, ".//div[child::*[@for='serial']]")
    PASSPORT_NUMBER = Input("Поле 'Номер паспорта'", By.XPATH, ".//div[child::*[@for='no']]")
    ISSUE_DATE = Input("Поле 'Когда выдан'", By.XPATH, ".//div[child::*[@for='whenAt']]")
    ISSUE = Input("Поле 'Кем выдан'", By.XPATH, ".//li[child::*[@for='issue']]")
    INN = Input("Поле 'Инн'", By.XPATH, "")

    SUBMIT = BaseElement("Кнопка 'Подтвердить'", By.XPATH,
                         ".//*[contains(text(),'Подтвердить') or contains(text(),'Сохранить')]")
