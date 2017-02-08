# coding=utf-8
from pages import page, Checkbox, Input, BaseElement, By
from pages.gkr_page import GkrPage


@page(u"Форма добавления новости", By.XPATH, "//form[..//child::*[contains(text(),'Добавление новости')]]")
class AddNewsPage(GkrPage):

    TITLE = BaseElement("Поле 'Заголовок новости'", By.ID, "title")
    DESC = BaseElement("Поле 'Текст новости'", By.ID, "text")
    PUBLISH_DATE = Input("Поле 'Дата создания'", By.XPATH, ".//*[child::*[contains(text(),'Дата')]]")
    IS_PUBLISHED = Checkbox("Чекбокс 'Опубликовать'", By.XPATH, ".//input[@type='checkbox']")
    SUBMIT = BaseElement("Кнопка 'Создать'", By.XPATH, ".//button[@type='submit']")

    ERROR = BaseElement("Сообщение об ошибке", By.XPATH, ".//span[contains(@style,'ff0000')]")
