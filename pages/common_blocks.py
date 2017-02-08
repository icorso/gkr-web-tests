# coding=utf-8
from elements.dialog import Dialog
from elements.redirect_dialog import RedirectDialog
from pages import page, BasePage, BaseElement, By, Link, List, Input


@page(u"Верхнее меню", By.XPATH, "//header//div[contains(@class,'links')]")
class TopMenu(BasePage):
    LOGIN_LINK = BaseElement(u"Ссылка 'Войдите'", By.XPATH, ".//a[contains(@class,'link_sign-in')]")
    REG_LINK = Link(u"Ссылка 'Зарегистрируйтесь'", By.XPATH, ".//a[contains(@class,'link_sign-up')]")
    LOGOUT = Link(u"Ссылка 'Выйти'", By.XPATH, ".//a[contains(@href,'logout')]")
    PROFILE = Link(u"Ссылка на профиль пользователя", By.XPATH, ".//a[contains(@href,'customer')]")


@page(u"Главное меню", By.XPATH, "//nav//ul[contains(@class,'menu')]")
class MainMenu(BasePage):
    MENU = List(u"Главное меню", By.XPATH, "//header/nav/ul/li")


@page("Форма 'Вход в систему'", By.XPATH, "//form[@id='header-reception-sign-in']")
class LoginForm(BasePage):
    LOGIN = Input("Поле 'Логин'", By.XPATH, ".//div[child::label[contains(text(), 'Введите логин')]]")
    PASSWORD = Input("Поле 'Пароль'", By.XPATH, ".//div[child::label[contains(text(), 'Введите пароль')]]")
    PASSWORD_RECOVERY = Link("Ссылка 'Забыли пароль?'", By.XPATH, ".//a[contains(text(),'Забыли пароль')]")
    ERROR = BaseElement("Сообщение об ошибке", By.XPATH, ".//div[@class='error' and contains(@style,'visible')]")
    REGISTRATION = BaseElement("Кнопка 'Регистрация'", By.XPATH, ".//*[contains(text(),'Регистрация')]")
    RECOVERY = Link("Ссылка 'Забыли пароль'", By.XPATH, ".//a[contains(@href,'restore')]")
    SUBMIT = BaseElement("Кнопка 'Войти'", By.XPATH, ".//*[contains(text(),'Войти')]")


@page("Диалог 'Восстановить пароль'", By.ID, "restore-password")
class RecoveryForm(BasePage):
    EMAIL = Input("Поле 'E-mail'", By.XPATH, ".//div[child::*[contains(text(),'E-mail адрес')]]")
    ERROR = BaseElement("Сообщение об ошибке", By.XPATH,
                        ".//div[contains(@class,'error') and contains(@style,'visible')]")
    SUBMIT = BaseElement("Кнопка 'Восстановить'", By.XPATH, ".//button[@type='submit']")
    WAIT = BaseElement("Элемент ожидания", By.XPATH, ".//p[@id='restore-password-wait']")
    SUCCESS_TEXT = BaseElement("Успешное подтверждение восстановления", By.XPATH, ".//div[@class='success']")


@page("Диалог 'Редактирование адреса'", By.XPATH, ".//div[@role='dialog']")
class AddressDialog(BasePage):
    VERIFY = BaseElement("Кнопка 'Проверить'", By.XPATH, ".//button[child::*[text()='Проверить']]")
    MANUAL = BaseElement("Кнопка 'Ввести вручную'", By.XPATH, ".//button[child::*[text()='Ввести вручную']]")


@page('Общие диалоги', By.XPATH, '*')
class Dialogs(BasePage):
    RESET_PASSWORD_SUCCESS_DIALOG = RedirectDialog("Диалог 'Сброс пароля'", By.XPATH,
                                                   ".//div[child::*/h6[contains(text(),'Сброс пароля')]]")
    REG_SUCCESS_DIALOG = RedirectDialog("Сообщение об успешной регистрации", By.XPATH,
                                        ".//div[child::div/h6[contains(text(),'Регистрация')]]")
    EMAIL_SUCCESS_DIALOG = RedirectDialog("Сообщение о подтвержении регистрации", By.XPATH,
                                          ".//div[child::div/h6[contains(text(),'Валидация email')]]")
    SAME_USER_REGISTERED_DIALOG = RedirectDialog("Сообщение о регистрации существующего пользователя", By.XPATH,
                                                 ".//div[child::div/h6[contains(text(),'Регистрация')]]")
    REG_CONFIRM_DIALOG = Dialog("Диалог подтверждения регистрации", By.XPATH,
                                ".//div[contains(@class,'ui-dialog ui')]")
