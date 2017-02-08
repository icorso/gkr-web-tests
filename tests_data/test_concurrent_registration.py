# coding=utf-8

import allure
from allure.constants import AttachmentType
import pytest

from db.qsystem import TCustomers, Customers
from pages.common_blocks import Dialogs
from steps.db_steps import GkrDbSteps
from steps.user_steps import GkrUserSteps
from pages.registration_page import RegistrationPage
from constants.urls import Urls
from krtech.utils import rand_str, rand_num, randrus_str


@pytest.mark.usefixtures('config')
@allure.feature('Registration')
@allure.story('Concurrent Registration')
class TestConcurrentRegistered:

    def test_concurrent_registration(self, config):
        user = GkrUserSteps(config)
        db_user = GkrDbSteps(config)
        reg_page = RegistrationPage(config)
        dialogs = Dialogs(config)

        i = 0
        report = ''
        while i < int(config.attempts):
            mobile = '9777' + rand_num(7)
            user.opens(Urls.REGISTRATION)
            user.should_see_element(reg_page)
            user.enters_text(reg_page.SURNAME, randrus_str(15))
            user.enters_text(reg_page.NAME, randrus_str(15))
            user.enters_text(reg_page.PATRONYMIC, randrus_str(15))
            user.enters_text(reg_page.BIRTHDAY, '12.06.1984')
            user.enters_text(reg_page.PASSPORT_SERIAL, rand_num(4))
            user.enters_text(reg_page.PASSPORT_NUMBER, rand_num(6))
            user.enters_text(reg_page.ISSUE, randrus_str(15))
            user.enters_text(reg_page.ISSUE_DATE, '09.01.2015')
            user.enters_text(reg_page.MOBILE, mobile)
            user.enters_text(reg_page.EMAIL, rand_str() + '@' + rand_str() + '.com')

            user.waits_for_element_enabled(reg_page.SUBMIT)
            user.submit_regform()

            user.waits_for_element_displayed(dialogs.REG_SUCCESS_DIALOG)
            tc = db_user.query_first(TCustomers, TCustomers.mobile_phone == mobile)
            user.opens(Urls.LOGOUT)
            user.opens('/registration/customer/?code=' + str(tc.code) + '&id=' + str(tc.id))
            user.waits_for_element_displayed(dialogs.EMAIL_SUCCESS_DIALOG)

            c = db_user.query_first(Customers, Customers.mobile_phone == mobile)
            report = report + '\nНовый пользователь id=' + str(c.id) + ', phone=' + c.mobile_phone
            user.logout()
            i += 1

        allure.attach('response.log', str(report), type=AttachmentType.TEXT)
