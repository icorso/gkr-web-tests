# coding=utf-8

import allure
import pytest
from hamcrest import equal_to_ignoring_case
from krtech.utils import rand_str

from constants.main_menu import MainMenu
from constants.messages import ErrorMessages
from data.users import OPERATOR, CUSTOMER
from pages.common_blocks import LoginForm
from pages.main_page import MainPage
from steps.user_steps import GkrUserSteps


@pytest.mark.usefixtures('config')
@allure.feature('Authentication')
@allure.story('Login')
class TestAuth:

    def test_not_exist_login(self, config, setup, teardown):
        user = GkrUserSteps(config)
        main_page = MainPage(config)

        user.login(rand_str(10), rand_str(10))
        user.waits_for_element_displayed(main_page.login_form.ERROR)
        user.should_see_element_with_text(main_page.login_form.ERROR, ErrorMessages.LOGIN_FAILED.text)

    def test_not_exist_password(self, config, setup, teardown):
        user = GkrUserSteps(config)
        login_page = LoginForm(config)

        user.login(OPERATOR.customers_data.mobile_phone, '')
        user.waits_for_element_displayed(login_page.ERROR)
        user.should_see_element_with_text(login_page.ERROR, ErrorMessages.LOGIN_FAILED.text)

    def test_logged_customer_header_and_menu(self, config, setup, teardown):
        user = GkrUserSteps(config)
        main_page = MainPage(config)
        c = CUSTOMER
        user.login(c.customers_data.mobile_phone, c.password)
        user.should_see_element(main_page.top_menu.PROFILE)
        user.should_see_element_matched_to(main_page.top_menu.PROFILE, equal_to_ignoring_case(c.customers_data.name
            + ' ' + c.customers_data.patronymic))

        customer_menu_items = menu_items
        customer_menu_items.remove(MainMenu.HISTORY.item)
        user.should_see_list_values(main_page.main_menu.MENU, menu_items)

    def test_logged_operator_header_and_menu(self, config, setup, teardown):
        user = GkrUserSteps(config)
        main_page = MainPage(config)
        o = OPERATOR
        user.login(o.customers_data.mobile_phone, o.password)
        user.should_not_see_element(main_page.top_menu.PROFILE)
        user.should_see_element(main_page.top_menu.LOGOUT)

        user.should_see_list_values(main_page.main_menu.MENU, menu_items)


@pytest.fixture(scope='function')
def setup(request):
    global menu_items

    menu_items = list(map(str, MainMenu))
    menu_items.append('')
    menu_items.append('')


@pytest.fixture(scope='function')
def teardown(request):
    def fin():
        config = getattr(request, '_funcargs')['config']
        user = GkrUserSteps(config)
        user.logout()
    request.addfinalizer(fin)
