# coding=utf-8

import allure
import pytest

from constants.urls import Urls
from constants.user_roles import UserRoles
from data.users import ADMIN, random_tcustomer, random_user
from db.qsystem import TCustomers
from pages.admin.admin_page import AdminPage
from pages.admin.customers_page import CustomersAdminPage, TCustomersAdminPage
from steps.db_steps import GkrDbSteps
from steps.user_steps import GkrUserSteps


@pytest.mark.usefixtures('config')
@allure.feature('Administration')
@allure.story('Search')
class TestSearch:
    expected_rows = 1
    search_attributes = ['mobile_phone', 'name', 'surname', 'patronymic', 'email', 'no']

    @pytest.mark.parametrize('attribute', search_attributes)
    def test_customers_search(self, config, attribute, setup, teardown):
        user = GkrUserSteps(config)
        db_user = GkrDbSteps(config)
        customers_admin_page = CustomersAdminPage(config)
        db_user.create_user(customer)

        user.opens(Urls.ADMIN_CUSTOMERS.url)
        user.should_see_element(customers_admin_page)
        user.enters_text(customers_admin_page.TERM_FIELD, "")
        user.clicks(customers_admin_page.SEARCH_SUBMIT)
        user.waits_for_ajax()

        term = getattr(getattr(customer, 'customers_data'), attribute)
        user.enters_text(customers_admin_page.TERM_FIELD, term)
        user.clicks(customers_admin_page.SEARCH_SUBMIT)
        user.waits_for_ajax()
        user.should_see_list_size(customers_admin_page.TABLE, self.expected_rows)
        user.should_see_element_contains_text(customers_admin_page.TABLE.elements[self.expected_rows - 1], term)

    @pytest.mark.parametrize('attribute', search_attributes)
    def test_uncomfirmed_customer_search(self, config, attribute, setup, teardown):
        user = GkrUserSteps(config)
        tcustomers_admin_page = TCustomersAdminPage(config)
        db_user = GkrDbSteps(config)
        db_user.creates_tcustomer(tcustomer)

        user.opens(Urls.ADMIN_UNCONFIRMED_CUSTOMERS.url)
        user.should_see_element(tcustomers_admin_page)
        user.enters_text(tcustomers_admin_page.TERM_FIELD, "")
        user.clicks(tcustomers_admin_page.SEARCH_SUBMIT)
        user.waits_for_ajax()

        term = getattr(getattr(tcustomer, 'customers_data'), attribute)
        user.enters_text(tcustomers_admin_page.TERM_FIELD, term)
        user.clicks(tcustomers_admin_page.SEARCH_SUBMIT)
        user.waits_for_ajax()
        user.should_see_list_size(tcustomers_admin_page.TABLE, self.expected_rows)
        user.should_see_element_contains_text(tcustomers_admin_page.TABLE.elements[self.expected_rows - 1], term)


@pytest.fixture(scope='class')
def setup(request):
    config = getattr(request, '_funcargs')['config']
    admin_page = AdminPage(config)
    user = GkrUserSteps(config)
    user.login(ADMIN.login, ADMIN.password)
    user.waits_for_element_displayed(admin_page)
    global customer, tcustomer
    customer = random_user(UserRoles.CUSTOMER)
    tcustomer = random_tcustomer(UserRoles.CUSTOMER)


@pytest.fixture(scope='class')
def teardown(request):
    def fin():
        config = getattr(request, '_funcargs')['config']
        db_steps = GkrDbSteps(config)
        db_steps.delete(TCustomers, TCustomers.id == tcustomer.customers_data.id)
        db_steps.delete_user_by_mobile(customer.login)

    request.addfinalizer(fin)
