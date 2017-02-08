# coding=utf-8
import os

import allure
import pytest
from hamcrest import contains_string

from constants.urls import Urls
from data.users import ADMIN
from pages.admin.import_page import ImportPage
from steps.db_steps import GkrDbSteps
from steps.user_steps import GkrUserSteps


@pytest.mark.usefixtures('config')
@allure.feature('Administration')
@allure.story('Import')
class TestCustomers:

    def test_import_successful(self, config, teardown):

        global mobile
        mobile = '7990999999'

        user = GkrUserSteps(config)
        import_page = ImportPage(config)

        user.login(ADMIN.login, ADMIN.password)
        user.waits_for_ajax()
        user.opens(Urls.ADMIN_IMPORT.url)

        import_file_path = os.path.abspath(__file__)
        import_file_path = import_file_path.replace('tests/admin/test_import.py', 'data/import.xls')
        import_page.IMPORT_FILE.element.send_keys(import_file_path)
        user.clicks(import_page.SUBMIT)

        user.should_see_element(import_page.IMPORT_BUTTON)
        user.should_see_list_size(import_page.READY_TABLE, 1)
        user.should_matches_to_list_item(import_page.READY_TABLE, contains_string(mobile))
        user.selects_checkbox(import_page.ADD_CHECKBOX)
        user.chooses_from_select(import_page.ORGANIZATIONS, 'РНКБ')
        user.clicks(import_page.IMPORT_BUTTON)

        user.should_see_element(import_page.ADDED)
        user.should_see_element_matched_to(import_page.ADDED, contains_string('Добавлено: 1'))


@pytest.fixture(scope='function')
def teardown(request):
    def fin():
        config = getattr(request, '_funcargs')['config']
        db_steps = GkrDbSteps(config)
        db_steps.delete_user_by_mobile(mobile)
        db_steps.delete_user_by_mobile('import@import.imp')

    request.addfinalizer(fin)
