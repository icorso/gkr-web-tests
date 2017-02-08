# coding=utf-8

import allure
import pytest
from krtech.utils import randrus_str

from constants.departments import Departments
from constants.main_menu import MainMenu
from data.users import CUSTOMER
from pages.main_page import MainPage
from pages.queue_page import QueuePage
from steps.user_steps import GkrUserSteps


@pytest.mark.usefixtures('config')
@allure.feature('Queue')
@allure.story('Validation')
class TestCustomAddress:

    def test_custom_street(self, config, setup):
        user = GkrUserSteps(config)
        queue_page = QueuePage(config)
        locality = 'с. Александровка'
        street = randrus_str(10)

        user.chooses_from_select(queue_page.CITY, Departments.BEL_DEP.short_name)
        user.enters_suggest(queue_page.LOCALITY, locality)
        user.enters_text(queue_page.STREET, street)
        user.waits_for_element_displayed(queue_page.address_dialog)
        user.clicks(queue_page.address_dialog.MANUAL)
        user.waits_for_element_disappeared(queue_page.address_dialog)
        user.should_see_element_enabled(queue_page.OTHER)
        user.should_see_field_value(queue_page.OTHER, locality + ', ' + street)

    def test_custom_verify_button(self, config, setup):
        user = GkrUserSteps(config)
        queue_page = QueuePage(config)
        locality = randrus_str(10)

        user.chooses_from_select(queue_page.CITY, Departments.BEL_DEP.short_name)
        user.enters_text(queue_page.LOCALITY, locality)
        user.waits_for_element_displayed(queue_page.address_dialog)
        user.clicks(queue_page.address_dialog.VERIFY)
        user.waits_for_element_disappeared(queue_page.address_dialog)
        user.should_see_field_value(queue_page.OTHER, '')
        user.should_see_attribute_value(queue_page.OTHER, 'disabled', True)


@pytest.fixture(scope='function')
def setup(request):
    config = getattr(request, '_funcargs')['config']
    user = GkrUserSteps(config)
    main_page = MainPage(config)
    user.login(CUSTOMER.customers_data.mobile_phone, CUSTOMER.password)
    user.waits_for_element_displayed(main_page.top_menu.LOGOUT)
    user.selects_from_main_menu(MainMenu.QUEUE)
