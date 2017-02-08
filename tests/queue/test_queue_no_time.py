# coding=utf-8
from datetime import datetime, timedelta

import allure
import pytest

from constants.departments import Departments
from constants.main_menu import MainMenu
from constants.messages import ErrorMessages
from constants.object_types import ObjectTypes
from constants.services import Services
from data.users import CUSTOMER, OPERATOR
from db.qsystem import Standards
from pages.main_page import MainPage
from pages.queue_page import QueuePage
from steps.db_steps import GkrDbSteps
from steps.user_steps import GkrUserSteps

next_opening_date = (datetime.now() + timedelta(days=10))


@pytest.mark.usefixtures('config')
@allure.feature('Queue')
@allure.story('No time')
class TestQueueNoTime:

    def test_queue_no_time_operator(self, config, setup):
        operator = OPERATOR
        user = GkrUserSteps(config)
        queue_page = QueuePage(config)

        user.login(operator.customers_data.mobile_phone, operator.password)
        user.should_see_element(queue_page)
        user.chooses_from_select(queue_page.SERVICE, Services.SINGLE_WINDOW.name)
        user.chooses_from_select(queue_page.OBJECT_TYPE, ObjectTypes.DOMOVLADENIE.name)
        user.chooses_from_select(queue_page.CITY, Departments.SIMF_DEP.short_name)

        user.waits_for_element_displayed(queue_page.QUEUE_FULL_MESSAGE)
        user.should_see_element_with_text(queue_page.QUEUE_FULL_MESSAGE, ErrorMessages.NEXT_OPENING_DATE.text
                                          + next_opening_date.strftime('%d.%m.%Y'))

    def test_queue_no_time_customer(self, config, setup):
        customer = CUSTOMER
        user = GkrUserSteps(config)
        main_page = MainPage(config)
        queue_page = QueuePage(config)

        user.login(customer.customers_data.mobile_phone, customer.password)
        user.waits_for_element_displayed(main_page.top_menu.LOGOUT)
        user.selects_from_main_menu(MainMenu.QUEUE)
        user.waits_for_element_displayed(queue_page)
        user.chooses_from_select(queue_page.SERVICE, Services.GKN.name)
        user.chooses_from_select(queue_page.OBJECT_TYPE, ObjectTypes.STROI_OBJECT.name)
        user.chooses_from_select(queue_page.CITY, Departments.SIMF_DEP.short_name)

        user.waits_for_element_displayed(queue_page.QUEUE_FULL_MESSAGE)
        user.should_see_element_with_text(queue_page.QUEUE_FULL_MESSAGE, ErrorMessages.NEXT_OPENING_DATE.text
                                          + next_opening_date.strftime('%d.%m.%Y'))


@pytest.fixture(scope='function')
def setup(request):
    config = getattr(request, '_funcargs')['config']
    db_steps = GkrDbSteps(config)
    params = {'next_opening_date': next_opening_date.strftime('%Y-%m-%d')}
    db_steps.update(Standards, Standards.id == 1, params)
