# coding=utf-8
from elements.history_services import HistoryServices
from pages import page, BaseElement, By, Input
from pages.gkr_page import GkrPage


@page("Форма 'Данные пользователя'", By.ID, 'userDetailsForm')
class ProfilePage(GkrPage):

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
    INN = Input("Поле 'Инн'", By.XPATH, ".//div[child::*[contains(text(),'Инн')]]")

    PASSWORD = Input("Поле 'Пароль'", By.XPATH, ".//div[child::*[contains(text(),' Новый пароль')]]")
    PASSWORD_CONFIRM = Input("Поле 'Повтор пароля'", By.XPATH, ".//div[child::*[contains(text(),' Повторите пароль')]]")
    ERROR_MESSAGE = BaseElement("Сообщение об ошибке", By.XPATH, ".//div[@style='color: red']")
    SUCCESS_MESSAGE = BaseElement("Сообщение об успешном измении профиля", By.XPATH, ".//div[@style='color: green']")
    SUBMIT = BaseElement("Кнопка 'Сохранить изменения'", By.XPATH, ".//button[contains(text(), 'Сохранить изменения')]")
    TICKETS_HISTORY = HistoryServices("Блок 'История услуг'", By.XPATH, ".//div[@class='history-services']")
