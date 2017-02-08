# coding=utf-8

from datetime import datetime, timedelta
from random import randrange

import allure
import pytest

from constants.urls import Urls
from data.users import ADMIN
from db.qsystem import Standards, Department
from pages.admin.standards_page import StandardsAdminPage
from steps.db_steps import GkrDbSteps
from steps.http_steps import GkrHttpSteps
from steps.user_steps import GkrUserSteps

creation_time = datetime.now() - timedelta(days=365)
advance_time = datetime.now() - timedelta(days=364)
date_from = creation_time.strftime('%d.%m.%Y')
date_to = advance_time.strftime('%d.%m.%Y')


@pytest.mark.usefixtures('config')
@allure.feature('Administration')
@allure.story('Standards')
class TestCustomers:

    def test_standards_save(self, config, teardown):
        global wait_max_advance_old
        user = GkrUserSteps(config)
        stardards_page = StandardsAdminPage(config)

        user.login(ADMIN.login, ADMIN.password)
        user.waits_for_ajax()
        user.opens(Urls.ADMIN_STANDARDS.url)
        wait_max_advance_old = stardards_page.WAIT_MAX_ADVANCE.value
        wait_max_advance_new = int(wait_max_advance_old) + randrange(1, 9)
        user.enters_text(stardards_page.WAIT_MAX_ADVANCE, wait_max_advance_new)
        user.enters_text(stardards_page.FINISH_DATE, (datetime.now() + timedelta(days=2)).strftime('%d.%m.%Y'))
        user.clicks(stardards_page.SUBMIT)
        user.waits_for_ajax()
        user.should_see_element_with_text(stardards_page.SUCCESS_MESSAGE, 'Сохранено')
        user.reloads_page()
        user.should_see_field_value(stardards_page.WAIT_MAX_ADVANCE, wait_max_advance_new)


@pytest.fixture(scope='function')
def teardown(request):
    def fin():
        config = getattr(request, '_funcargs')['config']
        db_steps = GkrDbSteps(config)
        http_steps = GkrHttpSteps(config)
        params = {'wait_max_advance': wait_max_advance_old}
        db_steps.update(Standards, Standards.id == 1, params)

        days_params = {'finish_advance_date': (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')}
        db_steps.update(Department, Department is not None, days_params)

        simf_params = {'finish_advance_date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')}
        db_steps.update(Department, Department.id == 75, simf_params)
        http_steps.renew_queue()

    request.addfinalizer(fin)
