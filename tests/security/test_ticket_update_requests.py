# coding=utf-8
from datetime import datetime
from time import sleep

import allure
import pytest
from hamcrest import assert_that, equal_to
from krtech.steps.http_steps import HttpSteps
from krtech.utils import rand_str

from constants.departments import Departments
from constants.object_types import ObjectTypes
from constants.services import Services
from constants.urls import Urls
from data.users import CUSTOMER, OPERATOR
from db.qsystem import Advance
from steps.db_steps import GkrDbSteps


@pytest.mark.usefixtures('config')
@allure.feature('Security')
@allure.story('Ticket Update Requests')
class TestTicketUpdateRequests:

    def test_ticket_update_request_by_not_authorized_user(self, config):
        db_user = GkrDbSteps(config)
        session = HttpSteps.HttpSession()
        logout_url = config.base_url + Urls.LOGOUT.url
        ticket_edit_url = config.base_url + Urls.ADMIN_TICKED_EDIT.url
        advance_updated = db_user.fill_advance_queue(Departments.SIMF_DEP, Services.SINGLE_WINDOW, datetime.now(),
                                                     ObjectTypes.STROI_OBJECT, OPERATOR)
        params = {'id': advance_updated.id, 'serviceid': advance_updated.service_id, 'inputData': rand_str(10), 'objectsCount': 2}
        session.with_method('get').with_url(logout_url).submit()
        session.with_method('post').with_url(ticket_edit_url % advance_updated.id).with_params(params).submit()
        sleep(2)

        advance_changed = db_user.query_first(Advance, advance_updated.id == advance_updated.id)
        db_user.delete_advance_by_id(advance_updated.id)
        assert_that(advance_changed.objects_count, equal_to(1), 'Запрос изменения тикета '
                    + ticket_edit_url % advance_updated.id + ' открыт для неавторизованного пользователя')

    @pytest.mark.parametrize('login, password', [(OPERATOR.login, OPERATOR.password),
                                                 (CUSTOMER.login, CUSTOMER.password)])
    def test_ticket_update_request_by_authorized_users(self, config, login, password):
        db_user = GkrDbSteps(config)
        session = HttpSteps.HttpSession()
        login_url = config.base_url + Urls.LOGIN.url + '/ajax'
        ticket_edit_url = config.base_url + Urls.ADMIN_TICKED_EDIT.url
        advance_updated = db_user.fill_advance_queue(Departments.SIMF_DEP, Services.SINGLE_WINDOW, datetime.now(),
                                                     ObjectTypes.STROI_OBJECT, OPERATOR)
        params = {'id': advance_updated.id, 'serviceid': advance_updated.service_id, 'inputData': rand_str(10), 'objectsCount': 2}

        session.with_method('post').with_params({'username': login, 'password': password}).with_url(login_url).submit()
        session.with_method('post').with_url(ticket_edit_url % advance_updated.id).with_params(params).submit()
        sleep(2)

        advance_changed = db_user.query_first(Advance, advance_updated.id == advance_updated.id)
        db_user.delete_advance_by_id(advance_updated.id)
        assert_that(advance_changed.objects_count, equal_to(1), 'Запрос изменения тикета '
                    + ticket_edit_url % advance_updated.id + ' открыт для авторизованного пользователя ' + login)
