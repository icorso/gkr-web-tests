# coding=utf-8
from time import sleep

import allure
import pytest
from hamcrest import assert_that, equal_to
from krtech.steps.http_steps import HttpSteps

from constants.urls import Urls
from constants.user_roles import UserRoles
from data.users import CUSTOMER, OPERATOR, random_user
from db.qsystem import Customers
from steps.db_steps import GkrDbSteps


@pytest.mark.usefixtures('config')
@allure.feature('Security')
@allure.story('Requests')
class TestUserBlockingRequests:

    def test_blocking_request_by_not_authorized_user(self, config, setup, teardown):
        session.with_method('get').with_url(logout_url).submit()
        session.with_method('post').with_url(blocking_url).with_params({'usersList': customer.id}).submit()
        sleep(1)
        blocking_state = db_user.query_first(Customers, Customers.mobile_phone == customer.mobile_phone).blocked
        assert_that(blocking_state, equal_to(0), 'Запрос блокировки пользователя ' + blocking_url +
                    ' открыт для неавторизованного пользователя')

    @pytest.mark.parametrize('login, password', [(OPERATOR.login, OPERATOR.password),
                                                 (CUSTOMER.login, CUSTOMER.password)])
    def test_blocking_request_by_authorized_users(self, config, login, password, setup, teardown):
        params = {'username': login, 'password': password}

        session.with_method('post').with_url(login_url).with_params(params).submit()
        session.with_method('post').with_url(blocking_url).with_params({'usersList': customer.id}).submit()
        sleep(1)
        blocking_state = db_user.query_first(Customers, Customers.mobile_phone == customer.mobile_phone).blocked
        assert_that(blocking_state, equal_to(0), 'Запрос блокировки пользователя ' + blocking_url +
                    ' открыт для не администратора')


@pytest.fixture(scope='function')
def setup(request):
    global db_user, session, login_url, logout_url, blocking_url, ticket_edit_url, customer
    config = getattr(request, '_funcargs')['config']
    db_user = GkrDbSteps(config)
    session = HttpSteps.HttpSession()
    logout_url = config.base_url + Urls.LOGOUT.url
    blocking_url = config.base_url + Urls.ADMIN_BLOCKING.url
    login_url = config.base_url + Urls.LOGIN.url + '/ajax'
    ticket_edit_url = config.base_url + Urls.ADMIN_TICKED_EDIT.url

    r_user = random_user(UserRoles.CUSTOMER)
    db_user.create_user(r_user)
    sleep(1)
    customer = db_user.query_first(Customers, Customers.mobile_phone == r_user.customers_data.mobile_phone)


@pytest.fixture(scope='function')
def teardown(request):
    def fin():
        config = getattr(request, '_funcargs')['config']
        db_steps = GkrDbSteps(config)
        db_steps.delete_user_by_mobile(customer.mobile_phone)

    request.addfinalizer(fin)
