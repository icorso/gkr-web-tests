# coding=utf-8

import allure
import pytest
from hamcrest import contains_string
from krtech.utils import randrus_str

from constants.urls import Urls
from constants.user_types import UserTypes
from data import admins_data
from data.users import ADMIN
from db.qsystem import Services
from pages.admin.admin_page import AdminPage
from pages.admin.services_page import ServicesAdminPage
from steps.db_steps import GkrDbSteps
from steps.user_steps import GkrUserSteps


@pytest.mark.usefixtures('config')
@allure.feature('Administration')
@allure.story('Services')
class TestServices:

    def test_service_creation(self, config, setup, teardown):
        global service
        user = GkrUserSteps(config)
        db_user = GkrDbSteps(config)
        services_page = ServicesAdminPage(config)

        name = randrus_str(10)
        prefix = randrus_str(2)
        group = UserTypes.LEGAL
        duration = 10
        additional_duration = 5
        percent_records = 30
        percent_records_advance = 60
        button_text = "<html><b><p align=center><span style='font-size:40.0pt;color:white'>%s</span></b>" % name

        user.opens(Urls.ADMIN_SERVICES)
        user.enters_text(services_page.NAME, name)
        user.enters_text(services_page.PREFIX, prefix)
        user.chooses_from_select(services_page.GROUP, group.name)
        user.enters_text(services_page.DURATION, duration)
        user.enters_text(services_page.ADDITIONAL_DURATION, additional_duration)
        user.enters_text(services_page.PERCENT_RECORDS, percent_records)
        user.enters_text(services_page.PERCENT_RECORDS_ADVANCE, percent_records_advance)
        user.waits_for_element_enabled(services_page.SUBMIT)
        user.clicks(services_page.SUBMIT)
        user.waits_for_ajax()
        user.reloads_page()
        service = db_user.query_first(Services, Services.name == name)

        # проверяет данные в таблице
        row = services_page.SERVICES_LIST.get_row_by_title(name)
        user.should_see_element_with_text(row.id, service.id)
        user.should_see_element_with_text(row.title, name)
        user.should_see_element_with_text(row.group, group.name)

        # проверяет данные в базе
        db_user.should_see_db_entry_value(service, 'name', name)
        db_user.should_see_db_entry_value(service, 'service_prefix', prefix)
        db_user.should_see_db_entry_value(service, 'group_id', group.id)
        db_user.should_see_db_entry_value(service, 'duration', duration)
        db_user.should_see_db_entry_value(service, 'aditional_duration', additional_duration)
        db_user.should_see_db_entry_value(service, 'precent_records', percent_records/100)
        db_user.should_see_db_entry_value(service, 'precent_records_advance', percent_records_advance/100)
        db_user.should_see_db_entry_value(service, 'button_text', button_text)

    def test_service_deletion(self, config, setup):
        global service
        user = GkrUserSteps(config)
        db_user = GkrDbSteps(config)
        services_page = ServicesAdminPage(config)
        service = db_user.creates_service(admins_data.random_service())
        user.opens(Urls.ADMIN_SERVICES)
        user.clicks(services_page.SERVICES_LIST.get_row_by_title(service.name).delete)
        user.waits_for_alert()
        user.waits_for(2)
        user.accepts_alert()
        user.waits_for_ajax()
        user.waits_for(2)
        user.should_not_matches_to_list_item(services_page.SERVICES_LIST, contains_string(str(service.id)))


@pytest.fixture(scope='function')
def setup(request):
    config = getattr(request, '_funcargs')['config']
    admin_page = AdminPage(config)
    user = GkrUserSteps(config)
    user.login(ADMIN.login, ADMIN.password)
    user.waits_for_element_displayed(admin_page)


@pytest.fixture(scope='function')
def teardown(request):
    def fin():
        config = getattr(request, '_funcargs')['config']
        db_steps = GkrDbSteps(config)
        db_steps.delete_service_by_id(service.id)

    request.addfinalizer(fin)
