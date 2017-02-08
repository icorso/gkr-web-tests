# coding=utf-8

from datetime import datetime, timedelta

import allure
import pytest

from constants.departments import Departments
from constants.object_types import ObjectTypes
from constants.services import Services
from constants.urls import Urls
from constants.user_roles import UserRoles
from data.users import ADMIN, random_user
from pages.admin.statistic_page import StatisticPage
from steps.db_steps import GkrDbSteps
from steps.user_steps import GkrUserSteps


@pytest.mark.usefixtures('config')
@allure.feature('Administration')
@allure.story('Statistic')
class TestStatistic:

    def test_statistic_by_creation_date(self, config, setup, teardown):
        user = GkrUserSteps(config)
        statistic_page = StatisticPage(config)

        creation_date = datetime.now() - timedelta(days=10)
        advance_date = datetime.now() - timedelta(days=9)

        db_user.fill_advance_queue(Departments.SUDAK_DEP, Services.SINGLE_WINDOW, advance_date,
                                   ObjectTypes.STROI_OBJECT, operator, creation_date)
        db_user.fill_advance_queue(Departments.SUDAK_DEP, Services.SINGLE_WINDOW, advance_date,
                                   ObjectTypes.STROI_OBJECT, customer, creation_date)

        user.enters_text(statistic_page.DATE_FROM, creation_date.strftime('%d.%m.%Y'))
        user.enters_text(statistic_page.DATE_TO, creation_date.strftime('%d.%m.%Y'))
        user.chooses_from_select(statistic_page.DEPARTMENT, Departments.SUDAK_DEP.name.replace('  ', ' '))
        user.clicks(statistic_page.CREATION_DATE)
        user.clicks(statistic_page.SUBMIT)
        user.waits_for_ajax()

        dep_row = statistic_page.TABLE.get_row_by_index(1)
        stat_row = statistic_page.TABLE.get_row_by_index(2)

        user.should_see_list_size(statistic_page.TABLE, 3)
        user.should_see_element_with_text(dep_row.department, Departments.SUDAK_DEP.name.replace('  ', ' '))
        user.should_see_element_with_text(stat_row.time, '')
        user.should_see_element_with_text(stat_row.quantity, 2)
        user.should_see_element_with_text(stat_row.physic, 1)
        user.should_see_element_with_text(stat_row.juristic, 1)
        user.should_see_element_with_text(stat_row.internet, 1)
        user.should_see_element_with_text(stat_row.registrators, 1)
        user.should_see_element_with_text(stat_row.rnkb, 0)
        user.should_see_element_with_text(stat_row.genbank, 0)
        user.should_see_element_with_text(stat_row.selsovet, 0)

        user.clicks(statistic_page.ADVANCE_DATE)
        user.enters_text(statistic_page.DATE_FROM, creation_date.strftime('%d.%m.%Y'))
        user.enters_text(statistic_page.DATE_TO, creation_date.strftime('%d.%m.%Y'))
        user.clicks(statistic_page.SUBMIT)
        user.waits_for_ajax()
        user.should_see_list_size(statistic_page.TABLE, 2)

    def test_statistic_by_advance_date(self, config, setup, teardown):
        user = GkrUserSteps(config)
        statistic_page = StatisticPage(config)

        creation_date = datetime.now() - timedelta(days=8)
        advance_date = datetime.now() - timedelta(days=7)

        db_user.fill_advance_queue(Departments.SUDAK_DEP, Services.SINGLE_WINDOW, advance_date,
                                   ObjectTypes.STROI_OBJECT, operator, creation_date)
        db_user.fill_advance_queue(Departments.SUDAK_DEP, Services.SINGLE_WINDOW, advance_date,
                                   ObjectTypes.STROI_OBJECT, customer, creation_date)

        user.enters_text(statistic_page.DATE_FROM, advance_date.strftime('%d.%m.%Y'))
        user.enters_text(statistic_page.DATE_TO, advance_date.strftime('%d.%m.%Y'))
        user.chooses_from_select(statistic_page.DEPARTMENT, Departments.SUDAK_DEP.name.replace('  ', ' '))
        user.clicks(statistic_page.ADVANCE_DATE)
        user.clicks(statistic_page.SUBMIT)
        user.waits_for_ajax()

        dep_row = statistic_page.TABLE.get_row_by_index(1)
        stat_row = statistic_page.TABLE.get_row_by_index(2)

        user.should_see_list_size(statistic_page.TABLE, 3)
        user.should_see_element_with_text(dep_row.department, Departments.SUDAK_DEP.name.replace('  ', ' '))
        user.should_see_element_with_text(stat_row.time, '')
        user.should_see_element_with_text(stat_row.quantity, 2)
        user.should_see_element_with_text(stat_row.physic, 1)
        user.should_see_element_with_text(stat_row.juristic, 1)
        user.should_see_element_with_text(stat_row.internet, 1)
        user.should_see_element_with_text(stat_row.registrators, 1)
        user.should_see_element_with_text(stat_row.rnkb, 0)
        user.should_see_element_with_text(stat_row.genbank, 0)
        user.should_see_element_with_text(stat_row.selsovet, 0)

        user.clicks(statistic_page.CREATION_DATE)
        user.enters_text(statistic_page.DATE_FROM, advance_date.strftime('%d.%m.%Y'))
        user.enters_text(statistic_page.DATE_TO, advance_date.strftime('%d.%m.%Y'))
        user.clicks(statistic_page.SUBMIT)
        user.waits_for_ajax()
        user.should_see_list_size(statistic_page.TABLE, 2)

    def test_statistic_details(self, config, setup, teardown):
        user = GkrUserSteps(config)
        statistic_page = StatisticPage(config)

        creation_date = datetime.now() - timedelta(days=6)
        advance_date = datetime.now() - timedelta(days=5)

        db_user.fill_advance_queue(Departments.SUDAK_DEP, Services.SINGLE_WINDOW, advance_date,
                                   ObjectTypes.STROI_OBJECT, operator, creation_date)
        db_user.fill_advance_queue(Departments.SUDAK_DEP, Services.SINGLE_WINDOW, advance_date,
                                   ObjectTypes.STROI_OBJECT, customer, creation_date)

        user.enters_text(statistic_page.DATE_FROM, advance_date.strftime('%d.%m.%Y'))
        user.enters_text(statistic_page.DATE_TO, advance_date.strftime('%d.%m.%Y'))
        user.chooses_from_select(statistic_page.DEPARTMENT, Departments.SUDAK_DEP.name.replace('  ', ' '))
        user.clicks(statistic_page.ADVANCE_DATE)
        user.clicks(statistic_page.DETAIL_DAY)
        user.clicks(statistic_page.SUBMIT)
        user.waits_for_ajax()
        dep_row = statistic_page.TABLE.get_row_by_index(1)
        stat_row = statistic_page.TABLE.get_row_by_index(2)

        user.should_see_list_size(statistic_page.TABLE, 3)
        user.should_see_element_with_text(dep_row.department, Departments.SUDAK_DEP.name.replace('  ', ' '))
        user.should_see_element_with_text(stat_row.time, advance_date.strftime('%Y-%m-%d'))
        user.should_see_element_with_text(stat_row.quantity, 2)
        user.should_see_element_with_text(stat_row.physic, 1)
        user.should_see_element_with_text(stat_row.juristic, 1)
        user.should_see_element_with_text(stat_row.internet, 1)
        user.should_see_element_with_text(stat_row.registrators, 1)
        user.should_see_element_with_text(stat_row.rnkb, 0)
        user.should_see_element_with_text(stat_row.genbank, 0)
        user.should_see_element_with_text(stat_row.selsovet, 0)

        user.clicks(statistic_page.DETAIL_HOUR)
        user.clicks(statistic_page.SUBMIT)
        user.waits_for_ajax()
        stat_row = statistic_page.TABLE.get_row_by_index(2)

        user.should_see_list_size(statistic_page.TABLE, 3)
        hour = advance_date.strftime('%H')
        user.should_see_element_with_text(stat_row.time, advance_date.strftime('%Y-%m-%d') + ' ' + hour + ':00-'
                                          + hour + ':59')


@pytest.fixture(scope='function')
def setup(request):
    global operator, customer, db_user
    config = getattr(request, '_funcargs')['config']
    db_user = GkrDbSteps(config)
    user = GkrUserSteps(config)

    user.login(ADMIN.login, ADMIN.password)
    user.waits_for_ajax()
    user.opens(Urls.ADMIN_STATISTIC.url)

    operator = random_user(UserRoles.OPERATOR)
    customer = random_user(UserRoles.CUSTOMER, is_legal=True)
    db_user.create_user(operator)
    db_user.create_user(customer)


@pytest.fixture(scope='function')
def teardown(request):
    def fin():
        config = getattr(request, '_funcargs')['config']
        db_steps = GkrDbSteps(config)
        db_steps.delete_user_by_mobile(operator.customers_data.mobile_phone)
        db_steps.delete_user_by_mobile(customer.customers_data.mobile_phone)

    request.addfinalizer(fin)
