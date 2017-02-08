# coding=utf-8
import re

import allure
import pytest

from constants.messages import ErrorMessages
from constants.urls import Urls
from data.registration_invalid_data import email, mobile, passport, issue, fio, inn
from pages.registration_page import RegistrationPage
from steps.user_steps import GkrUserSteps


@pytest.mark.usefixtures('config')
@allure.feature('Registration')
@allure.story('Validation')
class TestRegistrationFieldsValidation:

    @pytest.mark.parametrize('mobile', mobile)
    def test_mobile_field(self, config, mobile, setup):
        user = GkrUserSteps(config)

        reg_page = RegistrationPage(config)
        user.enters_text(reg_page.MOBILE, mobile)
        user.submit_regform()
        user.waits_for_element_displayed(reg_page.ERROR)
        user.should_see_field_value(reg_page.MOBILE, ''.join(re.findall('\d', mobile)))
        user.should_see_element_contains_text(reg_page.ERROR, ErrorMessages.MOBILE)

    def test_mobile_field_limit(self, config, setup):
        user = GkrUserSteps(config)
        reg_page = RegistrationPage(config)
        expected_phone = '12345678901234'
        user.enters_text(reg_page.MOBILE, expected_phone + '5')
        user.submit_regform()
        user.should_see_field_value(reg_page.MOBILE, expected_phone)

    @pytest.mark.parametrize('email, message', email)
    def test_email_field(self, config, email, message, setup):
        user = GkrUserSteps(config)
        reg_page = RegistrationPage(config)

        user.enters_text(reg_page.EMAIL, email)
        user.submit_regform()
        user.waits_for_element_displayed(reg_page.ERROR)
        user.should_see_element_contains_text(reg_page.ERROR, message)

    @pytest.mark.parametrize('passport', passport)
    def test_passport_serial_field(self, config, passport, setup):
        user = GkrUserSteps(config)
        reg_page = RegistrationPage(config)

        user.enters_text(reg_page.PASSPORT_SERIAL, passport)
        user.enters_text(reg_page.PASSPORT_NUMBER, passport)
        user.submit_regform()
        error = reg_page.ERROR
        user.waits_for_element_displayed(error)
        user.should_see_element_contains_text(error, ErrorMessages.PASSPORT_SERIAL)
        user.should_see_element_contains_text(error, ErrorMessages.PASSPORT_NUMBER)

    @pytest.mark.parametrize("issue, message", issue)
    def test_passport_issue_field(self, config, issue, message, setup):
        user = GkrUserSteps(config)
        reg_page = RegistrationPage(config)

        user.enters_text(reg_page.ISSUE, issue)
        user.submit_regform()
        user.waits_for_element_displayed(reg_page.ERROR)
        user.should_see_element_contains_text(reg_page.ERROR, ErrorMessages.PASSPORT_SERIAL)

    @pytest.mark.parametrize("inn, message", inn)
    def test_legal_inn_field(self, config, inn, message, setup):
        user = GkrUserSteps(config)
        reg_page = RegistrationPage(config)

        user.clicks(reg_page.LEGAL_TYPE)
        user.waits_for_element_displayed(reg_page.LEGAL_HEADER)
        user.enters_text(reg_page.INN, inn)
        user.clicks(reg_page.CHECKBOX)
        user.waits_for_element_enabled(reg_page.SUBMIT)
        user.clicks(reg_page.SUBMIT)
        user.waits_for_element_displayed(reg_page.ERROR)
        user.should_see_element_contains_text(reg_page.ERROR, message)


@pytest.fixture(scope='function')
def setup(request):
    config = getattr(request, '_funcargs')['config']
    reg_page = RegistrationPage(config)
    user = GkrUserSteps(config)
    user.logout()
    user.opens(Urls.REGISTRATION)
    user.should_see_element(reg_page)
