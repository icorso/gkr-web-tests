# coding=utf-8
from krtech.elements.input import Input

from pages import page, BaseElement, By
from pages.gkr_page import GkrPage


@page(u"Управление стандартами", By.XPATH, "//div[child::div/h6[contains(text(),'Управление стандартами')]]")
class StandardsAdminPage(GkrPage):
    WAIT_MAX_ADVANCE = Input(u"Поле 'Опоздание на регистрацию из предварительной очереди, в минутах'",
                             By.XPATH, ".//table[@class='table']/tbody/tr[2]/td")
    FINISH_DATE = Input(u"Поле 'Конечная дата предварительной записи, в минутах'",
                        By.XPATH, ".//table[@class='table']/tbody/tr[3]/td")
    SUCCESS_MESSAGE = BaseElement(u"Сообщение об успешном сохранении формы", By.ID, "saved")
    SUBMIT = BaseElement(u"Кнопка 'Сохранить'", By.ID, "saveBut")
