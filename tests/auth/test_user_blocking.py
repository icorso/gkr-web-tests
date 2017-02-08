# coding=utf-8

import allure
import pytest

from constants.messages import ErrorMessages
from constants.user_roles import UserRoles
from data.users import random_user
from db.qsystem import Customers
from pages.common_blocks import Dialogs
from pages.main_page import MainPage
from steps.db_steps import GkrDbSteps
from steps.user_steps import GkrUserSteps


@pytest.mark.usefixtures('config', 'setup', 'teardown')
@allure.feature('Authentication')
@allure.story('Blocking')
class TestUserBlocking:

    def test_user_blocking(self, config, setup, teardown):
        user = GkrUserSteps(config)
        main_page = MainPage(config)

        user.login(customer.customers_data.mobile_phone, customer.password)
        user.should_see_element_with_text(main_page.login_form.ERROR, ErrorMessages.LOGIN_BLOCKED.text)

    def test_blocking_password_recovery(self, config, setup, teardown):
        user = GkrUserSteps(config)
        db_user = GkrDbSteps(config)
        main_page = MainPage(config)
        dialogs = Dialogs(config)

        user.logout()
        user.clicks(main_page.top_menu.LOGIN_LINK)
        user.clicks(main_page.login_form.PASSWORD_RECOVERY)
        user.enters_text(main_page.recovery.EMAIL, customer.customers_data.email)
        user.clicks(main_page.login_form.SUBMIT)

        created_c = db_user.query_first(Customers, Customers.mobile_phone == customer.customers_data.mobile_phone)
        user.opens('/forgot/success/?code=' + created_c.code + '&id=' + str(created_c.id))
        user.should_see_dialog_text(dialogs.RESET_PASSWORD_SUCCESS_DIALOG,
                                    ErrorMessages.PASSWORD_RECOVERY_BLOCKED.text)


@pytest.fixture(scope='function')
def setup(request):
    global customer
    config = getattr(request, '_funcargs')['config']

    customer = random_user(UserRoles.CUSTOMER)
    db_user = GkrDbSteps(config)
    db_user.create_user(customer)
    db_user.blocks_user(customer.customers_data.mobile_phone, is_blocked=1)


@pytest.fixture(scope='function')
def teardown(request):
    def fin():
        config = getattr(request, '_funcargs')['config']
        db_steps = GkrDbSteps(config)
        db_steps.delete_user_by_mobile(customer.customers_data.mobile_phone)
    request.addfinalizer(fin)
