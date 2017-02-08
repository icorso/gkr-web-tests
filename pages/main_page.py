# coding=utf-8
from krtech.decorators import page
from selenium.webdriver.common.by import By

from elements.redirect_dialog import RedirectDialog
from pages.common_blocks import LoginForm, RecoveryForm
from pages.gkr_page import GkrPage


@page('Главная страница', By.XPATH, "//main[contains(@class,'home')]")
class MainPage(GkrPage):

    @property
    def login_form(self):
        return LoginForm(self.config)

    @property
    def recovery(self):
        return RecoveryForm(self.config)

    RESET_PASSWORD_SUCCESS_DIALOG = RedirectDialog("Диалог 'Сброс пароля'", By.XPATH,
                                                   "//div[child::*/h6[contains(text(),'Сброс пароля')]]")
