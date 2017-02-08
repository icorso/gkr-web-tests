# coding=utf-8
from enum import Enum


class RegistrationMessages(Enum):

    REGISTRATION_SUCCESSFUL = u'Ваши данные успешно приняты на обработку.\nВ ближайшее время вам будет прислано ' \
                              u'письмо с подтверждением регистрации.\nС ув. Администрация'
    EMAIL_CONFIRMED = u'Ваш аккаунт успешно подтверждён.\nНа почтовый ящик отослано письмо с логином и паролем.'

    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text

    def text(self):
        return self.text


class ErrorMessages(Enum):

    PASSPORT_USER_EXISTS = u'Пользователь с такими паспортными данными уже зарегистрирован в системе'
    EMAIL_USER_EXISTS = u'Пользователь с таким email адресом уже зарегистрирован в системе'
    MOBILE_USER_EXISTS = u'Пользователь с таким мобильным телефоном уже зарегистрирован в системе'
    USER_UNREGISTERED = u'Произошла ошибка, пользователь не зарегистрирован'
    SURNAME_EMPTY = u'Поле фамилия не должно быть пустым'
    SURNAME_LENGTH = u'Поле фамилия должно содержать до 255 символов'
    NAME_EMPTY = u'Поле имя не должно быть пустым'
    NAME_LENGTH = u'Поле имя должно содержать до 255 символов'
    EMAIL_MALFORMED = u'Некорректный формат электронного адреса'
    EMAIL_EMPTY = u'Поле email не должно быть пустым'
    EMAIL_LENGTH = u'Длина поля не может быть меньше 6 и больше 255 символов'
    MOBILE = u'Мобильный телефон должен содержать от 8 до 14 символов'
    MOBILE_QUEUE = u'Телефон должен содержать от 8 до 14 символов'
    PASSPORT_SERIAL = u'Серия паспорта состоит из 4 символов'
    PASSPORT_SERIAL_ONLY_DIGITS = u'Серия паспорта должна содержать только цифры'
    PASSPORT_NUMBER = u'Номер паспорта состоит из 6 символов'
    PASSPORT_NUMBER_ONLY_DIGITS = u'Номер паспорта должен содержать только цифры'
    ISSUE_EMPTY = u'Поле кем выдан паспорт не должно быть пустым'
    ISSUE_LENGTH = u'Поле кем выдан паспорт может быть в передах от 15 до 255 символов'
    ISSUE_DATE = u'Некорректный формат даты выдачи паспорта: ДД.ММ.ГГГГ'
    INN = u'Поле ИНН должно содержать от 10 до 12 цифр'

    PASSWORD_RECOVERY_FAILED = u'Пользователь с таким email адресом не зарегистрирован.'
    PASSWORD_RECOVERY_BLOCKED = u'Мы не смогли восстановить ваш пароль. Пожалуйста, попробуйте повторить попытку позже.'
    PASSWORD_LENGTH = u'Пароль должен быть от 8 до 10 символов.'
    PASSWORD_MISMATCH = u'Пароль и подтверждение пароля не совпадают.'
    LOGIN_FAILED = u'Неверный логин / пароль'
    LOGIN_BLOCKED = u'Аккаунт заблокирован\nНеобходимо подтверждение данных пользователя. Отправьте, пожалуйста, ' \
                    u'скан копию оригинала паспорта (для юр лица: свидетельства о постановке на учет в налоговом ' \
                    u'органе) на электронную почту support@krtech.ru.'
    BIRTHDAY_MALFORMED = u'Некорректный формат даты дня рождения: ДД.ММ.ГГГГ'
    TCUSTOMER_EXISTS = u'Вероятно такой пользователь уже существует. ' \
                       u'Попробуйте востопользоваться восстановлением пароля.'  # https://redmine.krtech.ru/issues/2069
    CUSTOMER_REGISTRATION_LIMIT = u'Пользователь с паспортом %s %s взял талон номер %s.\nОдин пользователь может взять ' \
                                  u'не более 1 талона в день'
    LEGAL_REGISTRATION_LIMIT = u'Пользователь с ИНН %s взял талон номер %s.\nОдин пользователь может взять не более ' \
                               u'1 талона в день'
    ADDRESS_MISMATCH = u'Некорректно введен адрес объекта недвижимости'
    DATE_NOT_SPECIFIED = u'Выберите дату и время приема'

    NEXT_OPENING_DATE = u'В выбраном отделении нет свободного времени\nЗапись на следующий период начнется '
    ADMIN_CUSTOMER_SAVE = u'Произошла ошибка, данные пользователя не обновлены'

    # Страница "Управление расписанием"
    SCHEDULE_FORM_ERROR = u'Форма заполнена с ошибками'
    SCHEDULE_NOT_SAVED = u'Сохраните текущую копию'
    SCHEDULE_EXISTS = u'Такой план уже существует'

    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text

    def text(self):
        return self.text


class ConfirmationMessages(Enum):

    PASSWORD_RECOVERY_SUCCESS = u'На ваш электронный ящик было направлено письмо с дальнейшими ' \
                                u'инструкциями по восстановлению пароля.'
    PASSWORD_RECOVERY_EXISTS = u'Такой пользователь уже зарегистрирован в системе.'
    PASSWORD_RECOVERY_CONFIRMED = u'Пароль был успешно изменён.'
    PASSPORT_DIALOG_TEXT = u'Государственный комитет по государственной регистрации и кадастру Республики Крым, ' \
                           u'проводит проверку паспортных данных.\n\nПожалуйста, обратите внимание на корректность ' \
                           u'заполненных данных.'
    PROFILE_CHANGED = u'Данные успешно обновлены'
    HISTORY_EMPTY = u'Сейчас история ваших заявок пуста.'

    # Страница "Управление расписанием"
    SCHEDULE_DUPLICATED = u'План дублирован'
    SCHEDULE_ADDED = u'План добавлен'
    SCHEDULE_SAVED = u'План сохранен'
    SCHEDULE_REMOVED = u'План удален'

    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text

    def text(self):
        return self.text
