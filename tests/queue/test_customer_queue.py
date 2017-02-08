# coding=utf-8
from datetime import datetime, timedelta

import allure
import pytest
from krtech.utils import rand_num

from constants.departments import Departments
from constants.main_menu import MainMenu
from constants.messages import ErrorMessages
from constants.object_types import ObjectTypes
from constants.services import Services
from constants.urls import Urls
from constants.user_roles import UserRoles
from constants.user_types import UserTypes
from data.users import CUSTOMER
from data.users import random_user
from pages.profile_page import ProfilePage
from pages.queue_page import QueuePage
from pages.ticket_data_dialog import TicketDataDialog
from steps.db_steps import GkrDbSteps
from steps.user_steps import GkrUserSteps


@pytest.mark.usefixtures('config')
@allure.feature('Queue')
@allure.story('Customer')
class TestCustomerQueue:
    
    def test_customer_queue_successful(self, config, teardown):
        customer = random_user(UserRoles.CUSTOMER)
        user = GkrUserSteps(config)
        db_user = GkrDbSteps(config)
        profile_page = ProfilePage(config)
        queue_page = QueuePage(config)
        ticket_data_dialog = TicketDataDialog(config)
        db_user.create_user(customer)

        global queue_mobile
        queue_mobile = customer.customers_data.mobile_phone

        day = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        print_day = (datetime.now() + timedelta(days=1)).strftime('%d.%m.%Y')

        locality = 'с. Александровка'
        street = 'ул. Виноградная'
        house = rand_num(2) + '/1a'
        flat = rand_num(2) + 'б'

        user.login(customer.customers_data.mobile_phone, customer.password)
        user.should_see_element(profile_page)
        user.selects_from_main_menu(MainMenu.QUEUE)
        user.waits_for_element_displayed(queue_page)
        user.chooses_from_select(queue_page.SERVICE, Services.SINGLE_WINDOW.name)
        user.chooses_from_select(queue_page.OBJECT_TYPE, ObjectTypes.DOMOVLADENIE.name)
        user.chooses_from_select(queue_page.CITY, Departments.BEL_DEP.short_name)
        user.enters_suggest(queue_page.LOCALITY, locality)
        user.enters_suggest(queue_page.STREET, street)
        user.enters_text(queue_page.HOUSE, house)
        user.enters_text(queue_page.FLAT, flat)
        user.enters_text(queue_page.CAPTCHA, '11111')
        user.clicks(queue_page.SUBMIT)

        user.waits_for_element_displayed(queue_page.CALENDAR)
        user.set_calendar_date(queue_page.CALENDAR, day)
        user.set_calendar_time(queue_page.CALENDAR, None)
        time = queue_page.CALENDAR.time_list[0].text

        user.clicks(queue_page.SUBMIT)

        user.waits_for_element_displayed(ticket_data_dialog)
        ticket_id = ticket_data_dialog.TICKET_NUMBER.element.text
        user.should_see_element_with_text(ticket_data_dialog.TICKET_TIME, (print_day + ' ' + time))
        user.should_see_element_with_text(ticket_data_dialog.TICKET_SERVICE, Services.SINGLE_WINDOW.name)
        user.should_see_element_with_text(ticket_data_dialog.TICKET_DEP, Departments.BEL_DEP.name)

        user.should_see_element_with_text(ticket_data_dialog.TICKET_CUSTOMER, customer.customers_data.surname + " "
                                          + customer.customers_data.name + " " + customer.customers_data.patronymic)
        user.should_see_element_with_text(ticket_data_dialog.TICKET_ADDRESS, Departments.BEL_DEP.short_name + " "
                                          + locality + " " + street + " д. " + house + " кв. " + flat)
        db_user.should_see_service_group_id(ticket_id, UserTypes.CUSTOMER.id)
        user.close(ticket_data_dialog)
        user.selects_from_main_menu(MainMenu.QUEUE)
        user.waits_for_element_displayed(queue_page)
        user.clicks(queue_page.SUBMIT)
        user.waits_for_element_displayed = user.waits_for_element_displayed(queue_page.ERROR_TEXT)
        user.should_see_text_in_list(queue_page.ERROR_TEXT,
                                     ErrorMessages.CUSTOMER_REGISTRATION_LIMIT.text
                                     % (customer.customers_data.serial, customer.customers_data.no, ticket_id))

        user.opens(Urls.PROFILE)
        history_item = profile_page.TICKETS_HISTORY.get_history_by_id(ticket_id)
        user.should_see_history_services(history_item, ticket_id, Services.SINGLE_WINDOW.name, print_day + ' ' + time)

    def test_customer_objects_type_values(self, config):
        user = GkrUserSteps(config)
        queue_page = QueuePage(config)

        user.login(CUSTOMER.login, CUSTOMER.password)

        user.opens(Urls.QUEUE.url)
        object_types = list(map(str, ObjectTypes))
        object_types.append('---')
        user.should_see_list_values(queue_page.OBJECT_TYPE, object_types)


@pytest.fixture(scope='function')
def teardown(request):
    def fin():
        config = getattr(request, '_funcargs')['config']
        db_steps = GkrDbSteps(config)
        db_steps.delete_user_by_mobile(queue_mobile)

    request.addfinalizer(fin)
