# coding=utf-8

from datetime import datetime, timedelta

import allure
import pytest

from constants.messages import RegistrationMessages
from constants.urls import Urls
from data.users import ADMIN, random_tcustomer
from db.qsystem import Customers, TCustomers
from pages.admin.customer_edit_page import CustomerEditPage
from steps.db_steps import GkrDbSteps
from steps.user_steps import GkrUserSteps

creation_time = datetime.now() - timedelta(days=365)
advance_time = datetime.now() - timedelta(days=364)
date_from = creation_time.strftime('%d.%m.%Y')
date_to = advance_time.strftime('%d.%m.%Y')


@pytest.mark.usefixtures('config')
@allure.feature('Administration')
@allure.story('TCustomer')
class TestTCustomer:

    def test_tcustomer_confirmation(self, config, teardown):

        global tcustomer
        tcustomer = random_tcustomer()

        db_user = GkrDbSteps(config)
        user = GkrUserSteps(config)
        tcustomer_page = CustomerEditPage(config)
        db_user.creates_tcustomer(tcustomer)

        user.login(ADMIN.login, ADMIN.password)
        user.waits_for_ajax()
        customer = db_user.query_first(TCustomers, TCustomers.name == tcustomer.customers_data.name)
        user.opens(Urls.ADMIN_TCUSTOMER_EDIT.url % customer.id)
        user.clicks(tcustomer_page.SUBMIT)

        user.waits_for_element_displayed(tcustomer_page.dialogs.EMAIL_SUCCESS_DIALOG)
        user.should_see_dialog_text(tcustomer_page.dialogs.EMAIL_SUCCESS_DIALOG, RegistrationMessages.EMAIL_CONFIRMED.text)

        db_user.should_not_see_db_entry(TCustomers, TCustomers.id == tcustomer.customers_data.id)
        db_user.should_see_db_entry(Customers, Customers.name == tcustomer.customers_data.name)


@pytest.fixture(scope='function')
def teardown(request):
    def fin():
        config = getattr(request, '_funcargs')['config']
        db_steps = GkrDbSteps(config)
        db_steps.delete_user_by_mobile(tcustomer.customers_data.mobile_phone)

    request.addfinalizer(fin)
