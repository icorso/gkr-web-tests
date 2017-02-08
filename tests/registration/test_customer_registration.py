# coding=utf-8

import allure
import pytest

from constants.messages import RegistrationMessages as Messages, ErrorMessages
from constants.urls import Urls
from constants.user_roles import UserRoles
from data.users import random_user
from db.qsystem import TCustomers, AclUsers
from pages.common_blocks import Dialogs
from pages.main_page import MainPage
from pages.profile_page import ProfilePage
from pages.registration_page import RegistrationPage
from steps.db_steps import GkrDbSteps
from steps.user_steps import GkrUserSteps


@pytest.mark.usefixtures('config')
@allure.feature('Registration')
@allure.story('Customer')
class TestCustomerRegistration:

    def test_customer_empty_form(self, config):
        user = GkrUserSteps(config)
        reg_page = RegistrationPage(config)
        main_page = MainPage(config)

        user.logout()
        user.clicks(main_page.top_menu.REG_LINK)
        user.submit_regform()

        error = reg_page.ERROR
        user.waits_for_element_displayed(error)
        user.should_see_element_contains_text(error, ErrorMessages.SURNAME_EMPTY)
        user.should_see_element_contains_text(error, ErrorMessages.NAME_EMPTY)
        user.should_see_element_contains_text(error, ErrorMessages.EMAIL_EMPTY)
        user.should_see_element_contains_text(error, ErrorMessages.BIRTHDAY_MALFORMED)
        user.should_see_element_contains_text(error, ErrorMessages.PASSPORT_SERIAL)
        user.should_see_element_contains_text(error, ErrorMessages.PASSPORT_NUMBER)
        user.should_see_element_contains_text(error, ErrorMessages.ISSUE_EMPTY)
        user.should_see_element_contains_text(error, ErrorMessages.ISSUE_DATE)

    def test_customer_empty_mobile_phone_field(self, config):
        user = GkrUserSteps(config)
        reg_page = RegistrationPage(config)
        main_page = MainPage(config)
        customer = random_user(UserRoles.CUSTOMER)

        user.logout()
        user.clicks(main_page.top_menu.REG_LINK)
        user.fill_registration_form(customer)
        user.enters_text(reg_page.MOBILE, "")
        user.submit_regform()

        user.waits_for_element_displayed(reg_page.ERROR)
        user.should_see_element_contains_text(reg_page.ERROR, ErrorMessages.MOBILE)

    def test_customer_self_registration(self, config, teardown):
        global self_reg_mobile
        customer = random_user(UserRoles.CUSTOMER)
        user = GkrUserSteps(config)
        db_user = GkrDbSteps(config)
        reg_page = RegistrationPage(config)
        profile_page = ProfilePage(config)
        main_page = MainPage(config)
        dialogs = Dialogs(config)

        self_reg_mobile = customer.customers_data.mobile_phone
        user.logout()
        user.clicks(main_page.top_menu.REG_LINK)
        user.fill_registration_form(customer)
        user.submit_regform()
        user.should_see_dialog_text(dialogs.REG_SUCCESS_DIALOG, Messages.REGISTRATION_SUCCESSFUL)

        t_customer = db_user.query_first(TCustomers, TCustomers.mobile_phone == self_reg_mobile)
        user.opens(Urls.REGISTRATION.url + '/customer/?code=' + str(t_customer.code) + '&id=' + str(t_customer.id))
        customer.password = db_user.query_first(AclUsers, AclUsers.name == customer.customers_data.mobile_phone).pwd
        user.should_see_dialog_text(dialogs.EMAIL_SUCCESS_DIALOG, Messages.EMAIL_CONFIRMED)
        user.close(dialogs.EMAIL_SUCCESS_DIALOG)

        user.login(customer.customers_data.mobile_phone, customer.password)
        user.should_see_element(profile_page)

        # проверка доступности полей
        disabled = 'disabled'
        user.should_see_attribute_value(reg_page.NAME, disabled, True)
        user.should_see_attribute_value(reg_page.SURNAME, disabled, True)
        user.should_see_attribute_value(reg_page.PATRONYMIC, disabled, True)
        user.should_see_element_enabled(reg_page.BIRTHDAY)
        user.should_see_attribute_value(reg_page.EMAIL, disabled, True)
        user.should_see_attribute_value(reg_page.MOBILE, disabled, True)
        user.should_see_attribute_value(reg_page.HOME_PHONE, disabled, True)
        user.should_see_attribute_value(reg_page.PASSPORT_SERIAL, disabled, True)
        user.should_see_attribute_value(reg_page.PASSPORT_NUMBER, disabled, True)
        user.should_see_attribute_value(reg_page.ISSUE_DATE, disabled, True)
        user.should_see_attribute_value(reg_page.ISSUE, disabled, True)
        user.should_see_element_enabled(profile_page.PASSWORD)
        user.should_see_element_enabled(profile_page.PASSWORD_CONFIRM)

        # проверка значений
        app_format = '%d.%m.%Y'
        user.should_see_element(profile_page)
        user.should_see_field_value(reg_page.NAME, customer.customers_data.name)
        user.should_see_field_value(reg_page.SURNAME, customer.customers_data.surname)
        user.should_see_field_value(reg_page.PATRONYMIC, customer.customers_data.patronymic)
        user.should_see_field_value(reg_page.BIRTHDAY, customer.customers_data.birthday.strftime(app_format))
        user.should_see_field_value(reg_page.EMAIL, customer.customers_data.email)
        user.should_see_field_value(reg_page.MOBILE, customer.customers_data.mobile_phone)
        user.should_see_field_value(reg_page.HOME_PHONE, '')
        user.should_see_field_value(reg_page.PASSPORT_SERIAL, customer.customers_data.serial)
        user.should_see_field_value(reg_page.PASSPORT_NUMBER, customer.customers_data.no)
        user.should_see_field_value(reg_page.ISSUE, customer.customers_data.issue)
        user.should_see_field_value(reg_page.ISSUE_DATE,
                                    customer.customers_data.when_at.strftime(app_format))


@pytest.fixture(scope='function')
def teardown(request):
    def fin():
        config = getattr(request, '_funcargs')['config']
        db_steps = GkrDbSteps(config)
        db_steps.delete_user_by_mobile(self_reg_mobile)

    request.addfinalizer(fin)
