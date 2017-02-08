# coding=utf-8
from pages import page, Input, Checkbox, BasePage, BaseElement, By
from pages.gkr_page import GkrPage


@page(u"Форма редактирования новости", By.XPATH, "//form[..//child::*[contains(text(),'Редактирование новости')]]")
class EditNewsPage(GkrPage):

    TITLE = BaseElement("Поле 'Заголовок новости'", By.ID, "title")
    DESC = BaseElement("Поле 'Текст новости'", By.ID, "text")
    PUBLISH_DATE = Input("Поле 'Дата создания'", By.XPATH, ".//*[child::*[contains(text(),'Дата')]]")
    IS_PUBLISHED = Checkbox("Чекбокс 'Опубликовать'", By.XPATH, ".//input[@type='checkbox']")
    SUBMIT = BaseElement("Кнопка 'Создать'", By.XPATH, ".//button[@type='submit']")

    ERROR = BaseElement("Сообщение об ошибке", By.XPATH, ".//span[contains(@style,'ff0000')]")
