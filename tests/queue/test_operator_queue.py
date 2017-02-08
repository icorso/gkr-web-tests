# coding=utf-8
from datetime import datetime, timedelta

import allure
import pytest
from krtech.utils import rand_num

from constants.departments import Departments
from constants.object_types import ObjectTypes
from constants.services import Services
from constants.user_roles import UserRoles
from constants.user_types import UserTypes
from data.users import random_user
from pages.queue_page import QueuePage
from pages.ticket_data_dialog import TicketDataDialog
from steps.db_steps import GkrDbSteps
from steps.user_steps import GkrUserSteps


@pytest.mark.usefixtures('config')
@allure.feature('Queue')
@allure.story('Operator')
class TestOperatorQueue:
    
    def test_operator_queue_successful(self, config, teardown):
        operator = random_user(UserRoles.OPERATOR)
        user = GkrUserSteps(config)
        db_user = GkrDbSteps(config)
        queue_page = QueuePage(config)
        ticket_data_dialog = TicketDataDialog(config)
        db_user.create_user(operator)

        global queue_operator_mobile
        queue_operator_mobile = operator.customers_data.mobile_phone

        day = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        print_day = (datetime.now() + timedelta(days=1)).strftime('%d.%m.%Y')

        locality = 'с. Александровка'
        street = 'ул. Виноградная'
        house = rand_num(2)
        flat = rand_num(2)

        user.login(operator.customers_data.mobile_phone, operator.password)
        user.should_see_element(queue_page)
        customer = user.fill_random_operator_queue()
        global queue_customer_by_operator_mobile
        queue_customer_by_operator_mobile = customer.mobile_phone

        user.chooses_from_select(queue_page.SERVICE, Services.DEAL_REGISTER.name)
        user.chooses_from_select(queue_page.OBJECT_TYPE, ObjectTypes.STROI_OBJECT.name)
        user.chooses_from_select(queue_page.CITY, Departments.BEL_DEP.short_name)
        user.enters_suggest(queue_page.LOCALITY, locality)
        user.enters_suggest(queue_page.STREET, street)
        user.enters_text(queue_page.HOUSE, house)
        user.enters_text(queue_page.FLAT, flat)
        user.set_calendar_date(queue_page.CALENDAR, day)
        user.set_calendar_time(queue_page.CALENDAR, None)
        time = queue_page.CALENDAR.time_list[0].text
        user.clicks(queue_page.SUBMIT)

        user.waits_for_element_displayed(ticket_data_dialog)
        user.should_see_element_with_text(ticket_data_dialog.TICKET_TIME, (print_day + ' ' + time))
        user.should_see_element_with_text(ticket_data_dialog.TICKET_SERVICE, Services.DEAL_REGISTER.name)
        user.should_see_element_with_text(ticket_data_dialog.TICKET_DEP, Departments.BEL_DEP.name)

        user.should_see_element_with_text(ticket_data_dialog.TICKET_CUSTOMER, customer.surname + " "
                                          + customer.name + " " + customer.patronymic)
        user.should_see_element_with_text(ticket_data_dialog.TICKET_ADDRESS, Departments.BEL_DEP.short_name + " "
                                          + locality + " " + street + " д. " + house + " кв. " + flat)
        db_user.should_see_service_group_id(ticket_data_dialog.TICKET_NUMBER.element.text, UserTypes.CUSTOMER.id)


@pytest.fixture(scope='function')
def teardown(request):
    def fin():
        config = getattr(request, '_funcargs')['config']
        db_steps = GkrDbSteps(config)
        db_steps.delete_user_by_mobile(queue_operator_mobile)
        db_steps.delete_user_by_mobile(queue_customer_by_operator_mobile)

    request.addfinalizer(fin)
