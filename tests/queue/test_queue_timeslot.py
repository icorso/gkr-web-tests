# coding=utf-8
import random
from datetime import datetime, timedelta

import allure
import pytest

from constants.departments import Departments
from constants.main_menu import MainMenu
from constants.services import Services
from constants.urls import Urls
from constants.user_roles import UserRoles
from data.queue_timeslot_data import legal_timeslot_data, operator_timeslot_data
from data.users import random_user
from pages.profile_page import ProfilePage
from pages.queue_page import QueuePage
from pages.ticket_data_dialog import TicketDataDialog
from steps.db_steps import GkrDbSteps
from steps.user_steps import GkrUserSteps


@pytest.mark.usefixtures('config')
@allure.feature('Queue')
@allure.story('Timeslot')
class TestTimeslot:

    def test_operator_timeslot(self, config):
        user = GkrUserSteps(config)
        db_user = GkrDbSteps(config)
        queue_page = QueuePage(config)
        ticket_data_dialog = TicketDataDialog(config)

        day = (datetime.now() + timedelta(days=random.randrange(0, 2))).strftime('%Y-%m-%d')

        locality = 'с. Виноградное'
        street = 'ул. Горная'
        house = 1

        for i in operator_timeslot_data:
            operator = random_user(UserRoles.OPERATOR)
            db_user.create_user(operator)

            object_type = i[0]
            stat_value = i[1]
            user.login(operator.customers_data.mobile_phone, operator.password)
            user.should_see_element(queue_page)
            user.fill_random_operator_queue()

            user.chooses_from_select(queue_page.SERVICE, Services.DEAL_REGISTER.name)
            user.chooses_from_select(queue_page.OBJECT_TYPE, object_type)
            user.chooses_from_select(queue_page.CITY, Departments.FEO_DEP.short_name)
            user.enters_suggest(queue_page.LOCALITY, locality)
            user.enters_suggest(queue_page.STREET, street)
            user.enters_text(queue_page.HOUSE, house)
            user.set_calendar_date(queue_page.CALENDAR, day)
            user.set_calendar_time(queue_page.CALENDAR, None)
            user.clicks(queue_page.SUBMIT)

            user.waits_for_element_displayed(ticket_data_dialog)
            user.opens(Urls.REGISTRATOR)
            user.chooses_from_select(queue_page.CITY, Departments.FEO_DEP.short_name)
            user.waits_for_ajax()
            user.should_see_element_with_text(queue_page.STAT_INDICATOR, stat_value)
            db_user.delete_user_by_mobile(operator.customers_data.mobile_phone)

    def test_legal_timeslot(self, config):
        user = GkrUserSteps(config)
        db_user = GkrDbSteps(config)
        queue_page = QueuePage(config)
        profile_page = ProfilePage(config)
        ticket_data_dialog = TicketDataDialog(config)

        for i in legal_timeslot_data:
            legal = random_user(UserRoles.CUSTOMER, is_legal=True)
            db_user.create_user(legal)
            day = (datetime.now() + timedelta(days=random.randrange(0, 2))).strftime('%Y-%m-%d')

            service = i[0]
            stat_value = i[1]
            locality = 'с. Виноградное'
            street = 'ул. Горная'

            user.login(legal.customers_data.mobile_phone, legal.password)
            user.waits_for_element_displayed(profile_page)
            user.selects_from_main_menu(MainMenu.QUEUE)
            user.waits_for_element_displayed(queue_page)

            user.chooses_from_select(queue_page.CITY, Departments.FEO_DEP.short_name)
            user.chooses_from_select(queue_page.SERVICE, service)
            user.chooses_from_select(queue_page.OBJECT_TYPE, '1')
            user.enters_suggest(queue_page.LOCALITY, locality)
            user.enters_suggest(queue_page.STREET, street)
            user.enters_text(queue_page.HOUSE, 2)
            user.set_calendar_date(queue_page.CALENDAR, day)
            user.set_calendar_time(queue_page.CALENDAR, None)
            user.enters_text(queue_page.CAPTCHA, '11111')
            user.clicks(queue_page.SUBMIT)
            user.waits_for_element_displayed(ticket_data_dialog)

            user.login(legal.customers_data.mobile_phone, legal.password)
            user.waits_for_element_displayed(profile_page)
            user.selects_from_main_menu(MainMenu.QUEUE)
            user.chooses_from_select(queue_page.CITY, Departments.FEO_DEP.short_name)
            user.chooses_from_select(queue_page.SERVICE, service)
            user.waits_for_ajax()
            user.should_see_element_with_text(queue_page.STAT_INDICATOR, stat_value)

            db_user.delete_user_by_mobile(legal.customers_data.mobile_phone)
