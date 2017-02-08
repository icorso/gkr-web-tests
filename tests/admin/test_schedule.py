# coding=utf-8
import random

import allure
import pytest

from constants.messages import ConfirmationMessages, ErrorMessages
from constants.urls import Urls
from data.admins_data import random_schedule
from data.users import ADMIN
from pages.admin.schedule_page import SchedulePage
from steps.db_steps import GkrDbSteps
from steps.user_steps import GkrUserSteps


@pytest.mark.usefixtures('config')
@allure.feature('Administration')
@allure.story('Schedule')
class TestSchedule:

    def test_existed_schedule_not_duplicate(self, config, setup):
        user = GkrUserSteps(config)
        schedule_page = SchedulePage(config)

        user.opens(Urls.ADMIN_SCHEDULE.url)
        random_option = user.chooses_random_from_select(schedule_page.SCHEDULE_LIST)
        user.clicks(schedule_page.DUPLICATE)
        user.chooses_from_select(schedule_page.SCHEDULE_LIST, random_option.text)
        user.clicks(schedule_page.DUPLICATE)
        user.should_see_element_with_text(schedule_page.ERROR_MESSAGE, ErrorMessages.SCHEDULE_EXISTS)

    def test_unsaved_schedule_not_duplicate(self, config, setup):
        user = GkrUserSteps(config)
        schedule_page = SchedulePage(config)

        user.opens(Urls.ADMIN_SCHEDULE.url)
        random_option = user.chooses_random_from_select(schedule_page.SCHEDULE_LIST)
        user.clicks(schedule_page.DUPLICATE)
        user.chooses_from_select(schedule_page.SCHEDULE_LIST, random_option.text + " - Копия")
        user.clicks(schedule_page.DUPLICATE)
        user.should_see_element_with_text(schedule_page.ERROR_MESSAGE, ErrorMessages.SCHEDULE_NOT_SAVED)

    def test_schedule_duplication(self, config, setup, teardown):
        global schedule_name

        user = GkrUserSteps(config)
        schedule_page = SchedulePage(config)

        user.opens(Urls.ADMIN_SCHEDULE.url)
        id_ = random.randint(1, len(schedule_page.SCHEDULE_LIST.select.options))
        schedule_page.SCHEDULE_LIST.select.select_by_index(id_)
        schedule_name = schedule_page.SCHEDULE_LIST.select.first_selected_option.text + " - Копия"
        user.clicks(schedule_page.DUPLICATE)
        user.should_see_element_with_text(schedule_page.SUCCESS_MESSAGE, ConfirmationMessages.SCHEDULE_DUPLICATED)
        user.should_see_text_in_select(schedule_page.SCHEDULE_LIST, schedule_name)
        user.chooses_from_select(schedule_page.SCHEDULE_LIST, schedule_name)
        user.clicks(schedule_page.SAVE)
        user.waits_for_ajax()
        user.should_see_element_with_text(schedule_page.SUCCESS_MESSAGE, ConfirmationMessages.SCHEDULE_ADDED)
        user.reloads_page()
        user.should_see_text_in_select(schedule_page.SCHEDULE_LIST, schedule_name)

    def test_schedule_deletion(self, config, setup):
        user = GkrUserSteps(config)
        db_user = GkrDbSteps(config)
        schedule_page = SchedulePage(config)

        schedule = random_schedule()
        db_user.creates_schedule(schedule)

        user.opens(Urls.ADMIN_SCHEDULE.url)

        user.chooses_from_select(schedule_page.SCHEDULE_LIST, schedule.name)
        user.clicks(schedule_page.DELETE)
        user.waits_for_alert()
        user.accepts_alert()
        user.should_see_element_with_text(schedule_page.SUCCESS_MESSAGE, ConfirmationMessages.SCHEDULE_REMOVED)

        user.waits_for_ajax()
        user.reloads_page()

        user.should_not_see_text_in_select(schedule_page.SCHEDULE_LIST, schedule.name)

    def test_schedule_edition(self, config, setup, teardown):
        global schedule_name
        user = GkrUserSteps(config)
        db_user = GkrDbSteps(config)
        schedule_page = SchedulePage(config)

        schedule = random_schedule()
        schedule_name = schedule.name
        db_user.creates_schedule(schedule)

        user.opens(Urls.ADMIN_SCHEDULE.url)

        user.chooses_from_select(schedule_page.SCHEDULE_LIST, schedule.name)
        tue = schedule_page.SETTINGS_TABLE.get_row_by_name('Вторник')

        time_from = '08:00'
        time_to = '18:00'
        break_from = '13:00'
        break_to = '14:00'
        duration = '45'
        value = 'value'

        user.enters_text(tue.time_from, time_from)
        user.enters_text(tue.time_to, time_to)
        user.enters_text(tue.break_from, break_from)
        user.enters_text(tue.break_to, break_to)
        user.enters_text(tue.duration, duration)
        user.clicks(schedule_page.SAVE)
        user.waits_for_ajax()
        user.should_see_element_with_text(schedule_page.SUCCESS_MESSAGE, ConfirmationMessages.SCHEDULE_SAVED)
        user.reloads_page()

        user.chooses_from_select(schedule_page.SCHEDULE_LIST, schedule.name)
        user.waits_for_ajax()
        tue = schedule_page.SETTINGS_TABLE.get_row_by_name('Вторник')
        user.should_see_attribute_value(tue.time_from, value, time_from)
        user.should_see_attribute_value(tue.time_to, value, time_to)
        user.should_see_attribute_value(tue.break_from, value, break_from)
        user.should_see_attribute_value(tue.break_to, value, break_to)
        user.should_see_attribute_value(tue.duration, value, duration)


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
        db_steps.delete_schedule_by_name(schedule_name)

    request.addfinalizer(fin)
