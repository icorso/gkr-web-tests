# coding=utf-8

import allure
import pytest
from hamcrest import contains_string, any_of

from constants.messages import RegistrationMessages as Messages, ErrorMessages
from constants.urls import Urls
from data.users import LEGAL, LEGAL_REG
from db.qsystem import TCustomers, AclUsers
from pages.common_blocks import Dialogs
from pages.profile_page import ProfilePage
from pages.registration_page import RegistrationPage
from steps.db_steps import GkrDbSteps
from steps.user_steps import GkrUserSteps


@pytest.mark.usefixtures('config')
@allure.feature('Registration')
@allure.story('Legal')
class TestLegalRegistration:

    def test_empty_legal_form(self, config):
        user = GkrUserSteps(config)
        reg_page = RegistrationPage(config)

        user.opens(Urls.REGISTRATION)
        user.should_see_element(reg_page)
        user.clicks(reg_page.LEGAL_TYPE)
        user.waits_for_element_displayed(reg_page.LEGAL_HEADER)
        user.clicks(reg_page.CHECKBOX)
        user.waits_for_element_enabled(reg_page.SUBMIT)
        user.clicks(reg_page.SUBMIT)

        error = reg_page.ERROR
        user.waits_for_element_displayed(error)
        user.should_see_element_contains_text(error, ErrorMessages.INN)
        user.should_see_element_contains_text(error, ErrorMessages.SURNAME_EMPTY)
        user.should_see_element_contains_text(error, ErrorMessages.NAME_EMPTY)
        user.should_see_element_contains_text(error, ErrorMessages.EMAIL_EMPTY)

    def test_legal_empty_mobile_phone_field(self, config):
        legal = LEGAL_REG
        user = GkrUserSteps(config)
        reg_page = RegistrationPage(config)

        user.opens(Urls.REGISTRATION)
        user.should_see_element(reg_page)
        user.clicks(reg_page.LEGAL_TYPE)
        user.waits_for_element_displayed(reg_page.LEGAL_HEADER)
        user.fill_legal_registration_form(legal)
        user.enters_text(reg_page.MOBILE, "")
        user.clicks(reg_page.CHECKBOX)
        user.waits_for_element_enabled(reg_page.SUBMIT)
        user.clicks(reg_page.SUBMIT)

        user.should_see_element_contains_text(reg_page.ERROR, ErrorMessages.MOBILE)

    def test_legal_self_registration(self, config, teardown):
        global legal_mobile
        legal = LEGAL_REG
        user = GkrUserSteps(config)
        db_user = GkrDbSteps(config)
        reg_page = RegistrationPage(config)
        dialogs = Dialogs(config)
        profile_page = ProfilePage(config)
        legal_mobile = legal.customers_data.mobile_phone

        user.opens(Urls.REGISTRATION)
        user.should_see_element(reg_page)
        user.clicks(reg_page.LEGAL_TYPE)
        user.waits_for_element_displayed(reg_page.LEGAL_HEADER)
        user.fill_legal_registration_form(legal)
        user.clicks(reg_page.CHECKBOX)
        user.waits_for_element_enabled(reg_page.SUBMIT)
        user.clicks(reg_page.SUBMIT)

        user.waits_for_element_displayed(dialogs.REG_SUCCESS_DIALOG)
        user.should_see_dialog_text(dialogs.REG_SUCCESS_DIALOG, Messages.REGISTRATION_SUCCESSFUL.text)
        user.close(dialogs.REG_SUCCESS_DIALOG)

        t_customer = db_user.query_first(TCustomers, TCustomers.mobile_phone == legal.customers_data.mobile_phone)
        user.opens(Urls.REGISTRATION.url + '/customer/?code=' + str(t_customer.code) + '&id=' + str(t_customer.id))
        legal.password = db_user.query_first(AclUsers, AclUsers.name == legal.customers_data.mobile_phone).pwd

        user.should_see_element(dialogs.EMAIL_SUCCESS_DIALOG)
        user.should_see_dialog_text(dialogs.EMAIL_SUCCESS_DIALOG, Messages.EMAIL_CONFIRMED.text)
        user.close(dialogs.EMAIL_SUCCESS_DIALOG)

        user.login(legal.customers_data.mobile_phone, legal.password)

        # проверка доступности полей
        disabled = 'disabled'
        user.should_see_attribute_value(profile_page.SURNAME, disabled, True)
        user.should_see_attribute_value(profile_page.NAME, disabled, True)
        user.should_see_attribute_value(profile_page.PATRONYMIC, disabled, True)
        user.should_see_attribute_value(profile_page.EMAIL, disabled, True)
        user.should_see_attribute_value(profile_page.MOBILE, disabled, True)
        user.should_see_attribute_value(profile_page.INN, disabled, True)

        user.should_see_element_enabled(profile_page.PASSWORD)
        user.should_see_element_enabled(profile_page.PASSWORD_CONFIRM)

        # проверка значений
        user.should_see_field_value(profile_page.INN, legal.customers_data.inn)
        user.should_see_field_value(profile_page.SURNAME, legal.customers_data.surname)
        user.should_see_field_value(profile_page.NAME, legal.customers_data.name)
        user.should_see_field_value(profile_page.PATRONYMIC, legal.customers_data.patronymic)
        user.should_see_field_value(profile_page.EMAIL, legal.customers_data.email)
        user.should_see_field_value(profile_page.MOBILE, legal.customers_data.mobile_phone)

    def test_same_legal_registration(self, config):
        user = GkrUserSteps(config)
        reg_page = RegistrationPage(config)
        existed_legal = LEGAL

        user.logout()
        user.clicks(reg_page.top_menu.REG_LINK)
        user.should_see_element(reg_page)
        user.clicks(reg_page.LEGAL_TYPE)
        user.waits_for_element_displayed(reg_page.LEGAL_HEADER)
        user.fill_legal_registration_form(existed_legal)
        user.clicks(reg_page.CHECKBOX)
        user.waits_for_element_enabled(reg_page.SUBMIT)
        user.clicks(reg_page.SUBMIT)
        error = reg_page.ERROR
        user.waits_for_element_displayed(error)
        user.should_see_element_matched_to(error, any_of(contains_string(ErrorMessages.MOBILE_USER_EXISTS.text),
                                                         contains_string(ErrorMessages.EMAIL_USER_EXISTS.text)))


@pytest.fixture(scope='function')
def teardown(request):
    def fin():
        config = getattr(request, '_funcargs')['config']
        db_steps = GkrDbSteps(config)
        db_steps.delete_user_by_mobile(legal_mobile)

    request.addfinalizer(fin)
