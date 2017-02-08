# coding=utf-8

import allure
import pytest
from krtech.utils import rand_str, rand_num

from constants.messages import ErrorMessages
from constants.urls import Urls
from constants.user_roles import UserRoles
from data.users import random_user
from pages.registration_page import RegistrationPage
from steps.db_steps import GkrDbSteps
from steps.user_steps import GkrUserSteps


@pytest.mark.usefixtures('config')
@allure.feature('Registration')
@allure.story('Already Registered')
class TestAlreadyRegistered:

    def test_exists_passport_data(self, config, setup, teardown):
        user = GkrUserSteps(config)
        reg_page = RegistrationPage(config)
        user.enters_text(reg_page.EMAIL, rand_str() + '@' + rand_str() + '.com')
        user.enters_text(reg_page.MOBILE, rand_num(11))
        user.submit_regform()
        user.waits_for_element_displayed(reg_page.ERROR)
        user.should_see_element_contains_text(reg_page.ERROR, ErrorMessages.PASSPORT_USER_EXISTS)

    def test_exists_email(self, config, setup, teardown):
        user = GkrUserSteps(config)
        reg_page = RegistrationPage(config)
        user.enters_text(reg_page.MOBILE, rand_num(11))
        user.enters_text(reg_page.PASSPORT_NUMBER, rand_num(6))
        user.enters_text(reg_page.PASSPORT_SERIAL, rand_num(4))
        user.submit_regform()
        user.waits_for_element_displayed(reg_page.ERROR)
        user.should_see_element_contains_text(reg_page.ERROR, ErrorMessages.EMAIL_USER_EXISTS)

    def test_exists_mobile(self, config, setup, teardown):
        user = GkrUserSteps(config)
        reg_page = RegistrationPage(config)
        user.enters_text(reg_page.EMAIL, rand_str() + '@' + rand_str() + '.com')
        user.enters_text(reg_page.PASSPORT_NUMBER, rand_num(6))
        user.enters_text(reg_page.PASSPORT_SERIAL, rand_num(4))
        user.submit_regform()
        user.waits_for_element_displayed(reg_page.ERROR)
        user.should_see_element_contains_text(reg_page.ERROR, ErrorMessages.MOBILE_USER_EXISTS)


@pytest.fixture(scope='function')
def setup(request):
    global customer
    config = getattr(request, '_funcargs')['config']
    user = GkrUserSteps(config)
    db_user = GkrDbSteps(config)

    user.logout()
    customer = random_user(UserRoles.CUSTOMER)
    db_user.create_user(customer)

    user.opens(Urls.REGISTRATION)
    user.fill_registration_form(customer)


@pytest.fixture(scope='function')
def teardown(request):
    def fin():
        config = getattr(request, '_funcargs')['config']
        db_steps = GkrDbSteps(config)
        db_steps.delete_user_by_mobile(customer.customers_data.mobile_phone)

    request.addfinalizer(fin)
