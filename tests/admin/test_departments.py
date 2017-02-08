# coding=utf-8

import allure
import pytest
from hamcrest import contains_string
from krtech.utils import randrus_str

from constants.calendars import Calendars
from constants.depart_region import DepartRegion
from constants.urls import Urls
from data.departments_data import rand_department
from data.users import ADMIN
from pages.admin.departments_page import DepartmentsAdminPage
from steps.db_steps import GkrDbSteps
from steps.http_steps import GkrHttpSteps
from steps.user_steps import GkrUserSteps


@pytest.mark.usefixtures('config')
@allure.feature('Administration')
@allure.story('Departments')
class TestDepartments:

    def test_department_creation(self, config, setup, teardown):
        global department_name

        user = GkrUserSteps(config)
        department_admin_page = DepartmentsAdminPage(config)

        # test data
        name = randrus_str(10)
        description = randrus_str(20)
        schedule = "алушта"
        phys_percents = 77
        legal_percents = 33
        department_name = name

        # filling form
        user.opens(Urls.ADMIN_DEPS.url)
        user.clicks(department_admin_page.NEW_DEPARTMENT)
        user.appends_text(department_admin_page.NAME, name)
        user.appends_text(department_admin_page.DESC, description)
        user.chooses_from_select(department_admin_page.SCHEDULE, schedule)
        user.chooses_from_select(department_admin_page.CALENDAR, Calendars.BEL_CALENDAR.name)
        user.selects_checkbox(department_admin_page.PHYS_CHECKBOX)
        user.selects_checkbox(department_admin_page.LEGAL_CHECKBOX)
        user.enters_text(department_admin_page.PHYS_INPUT, phys_percents)
        user.enters_text(department_admin_page.LEGAL_INPUT, legal_percents)
        user.chooses_from_select(department_admin_page.REGIONS_SELECT, DepartRegion.ARMYANSK.location)
        user.chooses_from_select(department_admin_page.REGIONS_SELECT, DepartRegion.ALUSHTA.location)
        user.clicks(department_admin_page.SAVE)
        user.waits_for_element_displayed(department_admin_page.SAVED, 10)
        user.reloads_page()
        user.chooses_from_select(department_admin_page.DEPARTMENTS_LIST, description)

        # verification
        user.should_see_field_value(department_admin_page.NAME, name)
        user.should_see_field_value(department_admin_page.DESC, description)
        user.should_see_element_enabled(department_admin_page.PHYS_INPUT)
        user.should_see_element_enabled(department_admin_page.LEGAL_INPUT)

        user.should_see_list_size(department_admin_page.REGIONS_LIST, 2)
        user.should_see_selected_text(department_admin_page.SCHEDULE, schedule)
        user.should_see_selected_text(department_admin_page.CALENDAR, Calendars.BEL_CALENDAR.name)
        user.should_matches_to_list_item(department_admin_page.REGIONS_LIST,
                                         contains_string(DepartRegion.ARMYANSK.location))
        user.should_matches_to_list_item(department_admin_page.REGIONS_LIST,
                                         contains_string(DepartRegion.ALUSHTA.location))

    def test_department_edition(self, config, setup, teardown):
        global department_name
        append_text = randrus_str(5)
        disabled = "disabled"

        user = GkrUserSteps(config)
        db_user = GkrDbSteps(config)
        http_user = GkrHttpSteps(config)
        department_admin_page = DepartmentsAdminPage(config)

        department = db_user.creates_department(rand_department(), DepartRegion.ARMYANSK, DepartRegion.BELOGORSKI,
                                                phys_percent=0.1, legal_percent=0.2)
        department_name = department.name + append_text

        http_user.renew_queue()
        user.opens(Urls.ADMIN_DEPS)
        user.chooses_from_select(department_admin_page.DEPARTMENTS_LIST, department.description)
        user.waits_for_ajax()

        user.appends_text(department_admin_page.NAME, append_text)
        user.appends_text(department_admin_page.DESC, append_text)
        user.chooses_from_select(department_admin_page.SCHEDULE, Calendars.BEL_CALENDAR.name)
        user.chooses_from_select(department_admin_page.CALENDAR, Calendars.BEL_CALENDAR.name)
        user.unselects_checkbox(department_admin_page.PHYS_CHECKBOX)
        user.unselects_checkbox(department_admin_page.LEGAL_CHECKBOX)
        user.clicks(department_admin_page.REGIONS_LIST.get_row_by_name(DepartRegion.ARMYANSK.location).delete)
        user.chooses_from_select(department_admin_page.REGIONS_SELECT, DepartRegion.ALUSHTA.location)
        user.clicks(department_admin_page.SAVE)
        user.waits_for_element_displayed(department_admin_page.SAVED)

        user.reloads_page()
        user.chooses_from_select(department_admin_page.DEPARTMENTS_LIST, department.description + append_text)

        user.should_see_field_value(department_admin_page.NAME, department.name + append_text)
        user.should_see_field_value(department_admin_page.DESC, department.description + append_text)
        user.should_see_attribute_value(department_admin_page.PHYS_INPUT, disabled, True)
        user.should_see_attribute_value(department_admin_page.LEGAL_INPUT, disabled, True)

        user.should_see_list_size(department_admin_page.REGIONS_LIST, 2)
        user.should_not_matches_to_list_item(department_admin_page.REGIONS_LIST,
                                             contains_string(DepartRegion.ARMYANSK.location))
        user.should_matches_to_list_item(department_admin_page.REGIONS_LIST,
                                         contains_string(DepartRegion.ALUSHTA.location))


@pytest.fixture(scope='function')
def setup(request):
    config = getattr(request, '_funcargs')['config']
    user = GkrUserSteps(config)
    user.login(ADMIN.login, ADMIN.password)


@pytest.fixture(scope='function')
def teardown(request):
    def fin():
        config = getattr(request, '_funcargs')['config']
        db_steps = GkrDbSteps(config)
        db_steps.delete_department_by_name(department_name)

    request.addfinalizer(fin)
