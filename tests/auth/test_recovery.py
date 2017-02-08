# coding=utf-8

import allure
from hamcrest import contains_string
import pytest
from krtech.utils import rand_str

from constants.messages import ErrorMessages, ConfirmationMessages
from constants.user_roles import UserRoles
from data.users import random_user
from db.qsystem import AclUsers, Customers
from pages.common_blocks import LoginForm, Dialogs
from pages.main_page import MainPage
from pages.profile_page import ProfilePage
from steps.db_steps import GkrDbSteps
from steps.user_steps import GkrUserSteps

customer = random_user(UserRoles.CUSTOMER)


@pytest.mark.usefixtures('config')
@allure.feature('Authentication')
@allure.story('Password Recovery')
class TestRecovery:

    def test_not_exist_recovery_email(self, config):
        user = GkrUserSteps(config)
        main_page = MainPage(config)

        user.logout()
        user.clicks(main_page.top_menu.LOGIN_LINK)
        user.clicks(main_page.login_form.RECOVERY)
        user.enters_text(main_page.recovery.EMAIL, rand_str(10) + '@' + rand_str(10) + '.' + rand_str(3))
        user.clicks(main_page.recovery.SUBMIT)
        user.should_see_element_with_text(main_page.recovery.ERROR, ErrorMessages.PASSWORD_RECOVERY_FAILED.text)

    def test_password_recovery(self, config, teardown):
        user = GkrUserSteps(config)
        db_user = GkrDbSteps(config)
        login_page = LoginForm(config)
        main_page = MainPage(config)
        profile_page = ProfilePage(config)
        dialogs = Dialogs(config)
        db_user.create_user(customer)

        user.logout()
        user.clicks(main_page.top_menu.LOGIN_LINK)
        user.clicks(main_page.login_form.RECOVERY)
        user.enters_text(main_page.recovery.EMAIL, customer.customers_data.email)
        user.clicks(main_page.recovery.SUBMIT)
        user.waits_for_element_disappeared(main_page.recovery.WAIT, config.page_load_timeout)
        user.should_see_element_with_text(main_page.recovery.SUCCESS_TEXT,
                                          ConfirmationMessages.PASSWORD_RECOVERY_SUCCESS)
        created_c = db_user.query_first(Customers, Customers.mobile_phone == customer.customers_data.mobile_phone)
        user.opens('/forgot/success/?code=' + created_c.code + '&id=' + str(created_c.id))
        user.should_see_element_matched_to(dialogs.RESET_PASSWORD_SUCCESS_DIALOG,
                                           contains_string(ConfirmationMessages.PASSWORD_RECOVERY_CONFIRMED.text))
        new_password = db_user.query_first(AclUsers, AclUsers.name == customer.customers_data.mobile_phone)

        user.login(customer.customers_data.mobile_phone, customer.password)
        user.should_see_element_with_text(login_page.ERROR, ErrorMessages.LOGIN_FAILED)

        user.login(customer.customers_data.mobile_phone, new_password.pwd)
        user.should_see_element(profile_page)


@pytest.fixture(scope='function')
def teardown(request):
    def fin():
        config = getattr(request, '_funcargs')['config']
        db_steps = GkrDbSteps(config)
        db_steps.delete_user_by_mobile(customer.customers_data.mobile_phone)

    request.addfinalizer(fin)
