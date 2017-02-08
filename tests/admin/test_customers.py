# coding=utf-8

from datetime import datetime, timedelta

import allure
import pytest
from krtech.utils import rand_str

from constants.messages import ErrorMessages
from constants.urls import Urls
from constants.user_roles import UserRoles
from data.users import ADMIN, random_user
from db.qsystem import Customers
from pages.admin.customer_edit_page import CustomerEditPage
from steps.db_steps import GkrDbSteps
from steps.user_steps import GkrUserSteps

creation_time = datetime.now() - timedelta(days=365)
advance_time = datetime.now() - timedelta(days=364)
date_from = creation_time.strftime('%d.%m.%Y')
date_to = advance_time.strftime('%d.%m.%Y')


@pytest.mark.usefixtures('config')
@allure.feature('Administration')
@allure.story('Customer')
class TestCustomers:

    def test_customer_edit(self, config, setup, teardown):
        email = rand_str(10) + '@' + rand_str(10) + '.ru'
        user.login(ADMIN.login, ADMIN.password)
        user.waits_for_ajax()
        db_customer = db_user.query_first(Customers, Customers.name == customer.customers_data.name)
        user.opens(Urls.ADMIN_CUSTOMER_EDIT.url % db_customer.id)
        user.enters_text(customer_edit_page.EMAIL, email)
        user.clicks(customer_edit_page.SUBMIT)

        user.waits_for_ajax()
        user.should_not_see_text(ErrorMessages.ADMIN_CUSTOMER_SAVE.text)
        user.opens(Urls.ADMIN_CUSTOMER_EDIT.url % db_customer.id)
        user.should_see_field_value(customer_edit_page.EMAIL, email)


@pytest.fixture(scope='function')
def setup(request):
    config = getattr(request, '_funcargs')['config']
    global customer, db_user, user, customer_edit_page
    customer = random_user(UserRoles.CUSTOMER)

    db_user = GkrDbSteps(config)
    user = GkrUserSteps(config)
    customer_edit_page = CustomerEditPage(config)

    db_user.create_user(customer)


@pytest.fixture(scope='function')
def teardown(request):
    def fin():
        config = getattr(request, '_funcargs')['config']
        db_steps = GkrDbSteps(config)
        db_steps.delete_user_by_mobile(customer.customers_data.mobile_phone)

    request.addfinalizer(fin)
