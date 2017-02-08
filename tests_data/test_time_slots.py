# coding=utf-8
import random

import allure
import pytest
from allure.constants import AttachmentType
from selenium.webdriver.common.by import By

from constants import object_types
from constants import services
from constants.departments import Departments
from constants.urls import Urls
from data.users import OPERATOR
from pages.queue_page import QueuePage
from pages.ticket_data_dialog import TicketDataDialog
from steps.user_steps import GkrUserSteps


@pytest.mark.usefixtures('config')
@allure.feature('TimeSlots')
@allure.feature('Data Amount')
class TestTimeSlotsRegistration:

    def test_filling_data(self, config, setup, teardown):
        user = GkrUserSteps(config)
        queue_page = QueuePage(config)
        ticket_data_dialog = TicketDataDialog(config)

        report = ''
        attempts = config.attempts  # тест прерывается, если указанное число раз подряд
                                   # не было свободного времени для записи
        city = Departments.BEL_DEP.short_name
        locality = 'а'
        street = 'ул. Виноградная'

        i = 0
        while i < int(attempts):
            service = random.choice(list(services.Services)).name
            object_type = random.choice(list(object_types.ObjectTypes)).name

            user.waits_for_element_displayed(queue_page)
            user.fill_random_operator_queue()
            user.chooses_from_select(queue_page.SERVICE, service)
            user.chooses_from_select(queue_page.OBJECT_TYPE, object_type)
            user.chooses_from_select(queue_page.CITY, Departments.BEL_DEP.short_name)
            user.enters_suggest(queue_page.LOCALITY, locality)
            user.enters_suggest(queue_page.STREET, street)
            user.enters_text(queue_page.HOUSE, 1)

            user.set_calendar_date(queue_page.CALENDAR, config.timeslot_date)
            if user.set_calendar_time(queue_page.CALENDAR, None) != 0:
                user.clicks(queue_page.SUBMIT)
                user.waits_for_element_displayed(ticket_data_dialog)

                if 'занято' not in config.driver.find_element(By.TAG_NAME, 'body').text:
                    user.should_see_element(ticket_data_dialog)
                    row = u'\nНомер тикета : ' + ticket_data_dialog.TICKET_NUMBER.element.text \
                          + u'\nДата записи : ' + ticket_data_dialog.TICKET_TIME.element.text \
                          + u'\nУслуга : ' + service \
                          + u'\nТип объекта недвижимости : ' + object_type \
                          + u'\nГород : ' + city \
                          + u'\n==='
                    i = 0
                else:
                    row = u'Время ' + config.timeslot_date + ' занято.'
            else:
                row = u'\nДата записи : ' + config.timeslot_date \
                      + u'\nДля услуги \'' + service + '\' и объекта \'' + object_type \
                      + '\' свободное время записи закончилось.'
                i += 1

            report += row
            user.reloads_page()
        allure.attach('response.log', str(report), type=AttachmentType.TEXT)


@pytest.fixture(scope='function')
def setup(request):
    config = getattr(request, '_funcargs')['config']
    user = GkrUserSteps(config)
    user.opens(Urls.MAIN)
    operator = OPERATOR
    user.login(operator.customers_data.mobile_phone, operator.password)


@pytest.fixture(scope='function')
def teardown(request):
    def fin():
        config = getattr(request, '_funcargs')['config']
        user = GkrUserSteps(config)
        user.logout()

    request.addfinalizer(fin)
