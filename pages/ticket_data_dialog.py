# coding=utf-8
from pages import page, BasePage, BaseElement, By


@page("Данные регистрации", By.ID, "get-ticket")
class TicketDataDialog(BasePage):

    TICKET_NUMBER = BaseElement("Номер", By.ID, "ticket_id")
    TICKET_TIME = BaseElement("Время", By.ID, "ticket_time")
    TICKET_SERVICE = BaseElement("Услуга", By.ID, "ticket_service")
    TICKET_DEP = BaseElement("Отделение", By.ID, "ticket_department")
    TICKET_CUSTOMER = BaseElement("Посетитель", By.ID, "ticket_customer")
    TICKET_ADDRESS = BaseElement("Недвижимость", By.ID, "ticket_address")
    TICKET_PRINT = BaseElement("Кнопка 'Печать талона'", By.ID, "pdf_ticket")
    GET_TICKET = BaseElement("Кнопка 'Получить талон'", By.ID, "submit")

    @property
    def close(self):
        return self.element.find_element(By.XPATH, ".//a[contains(@class,'close')]")

