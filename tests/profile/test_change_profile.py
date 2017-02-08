# coding=utf-8
from datetime import datetime, timedelta

import allure
import pytest

from constants.messages import ConfirmationMessages
from constants.urls import Urls
from constants.user_roles import UserRoles
from data.registration_invalid_data import password
from data.users import CUSTOMER, random_user
from pages.profile_page import ProfilePage
from pages.registration_page import RegistrationPage
from steps.db_steps import GkrDbSteps
from steps.user_steps import GkrUserSteps


@pytest.mark.usefixtures('config')
@allure.feature('Profile')
@allure.story('Profile change')
class TestProfile:
    @pytest.mark.parametrize('password,password_confirm,message', password)
    def test_password_change_incorrect(self, config, password, password_confirm, message):
        user = GkrUserSteps(config)
        profile_page = ProfilePage(config)
        customer = CUSTOMER

        user.login(customer.customers_data.mobile_phone, customer.password)
        user.waits_for_element_displayed(profile_page)
        user.enters_text(profile_page.PASSWORD, password)
        user.enters_text(profile_page.PASSWORD_CONFIRM, password_confirm)
        user.clicks(profile_page.SUBMIT)
        user.waits_for_element_displayed(profile_page.ERROR_MESSAGE)
        user.should_see_element_with_text(profile_page.ERROR_MESSAGE, message)

    def test_password_change_successfully(self, config, teardown):
        user = GkrUserSteps(config)
        db_user = GkrDbSteps(config)
        profile_page = ProfilePage(config)
        customer = random_user(UserRoles.CUSTOMER)
        db_user.create_user(customer)
        global mobile
        mobile = customer.customers_data.mobile_phone
        password = '87654321'

        user.login(customer.customers_data.mobile_phone, customer.password)
        user.waits_for_element_displayed(profile_page)

        user.enters_text(profile_page.PASSWORD, password)
        user.enters_text(profile_page.PASSWORD_CONFIRM, password)
        user.clicks(profile_page.SUBMIT)

        user.waits_for_element_displayed(profile_page.SUCCESS_MESSAGE)
        user.should_see_element_with_text(profile_page.SUCCESS_MESSAGE, ConfirmationMessages.PROFILE_CHANGED)

        user.login(customer.customers_data.mobile_phone, password)
        user.should_see_element(profile_page)

    def test_birthday_change_successfully(self, config):
        user = GkrUserSteps(config)
        profile_page = ProfilePage(config)
        reg_page = RegistrationPage(config)
        customer = CUSTOMER

        user.login(customer.customers_data.mobile_phone, customer.password)
        user.waits_for_element_displayed(profile_page)

        birthday = (datetime.now() - timedelta(weeks=500)).strftime('%d.%m.%Y')
        user.enters_text(reg_page.BIRTHDAY, birthday)
        user.clicks(profile_page.SUBMIT)
        user.waits_for_element_displayed(profile_page.SUCCESS_MESSAGE)
        user.should_see_element_with_text(profile_page.SUCCESS_MESSAGE,
                                          ConfirmationMessages.PROFILE_CHANGED.text)
        user.opens(Urls.PROFILE)
        user.should_see_field_value(reg_page.BIRTHDAY, birthday)


@pytest.fixture(scope='function')
def teardown(request):
    def fin():
        config = getattr(request, '_funcargs')['config']
        db_steps = GkrDbSteps(config)
        db_steps.delete_user_by_mobile(mobile)

    request.addfinalizer(fin)
