# coding=utf-8
from datetime import datetime, timedelta

import allure
import pytest
from hamcrest import contains_string
from krtech.utils import randrus_str

from constants.departments import Departments
from constants.main_menu import MainMenu
from constants.messages import ConfirmationMessages
from constants.object_types import ObjectTypes
from constants.services import Services
from constants.user_roles import UserRoles
from data.users import random_user
from pages.history_page import HistoryPage
from pages.main_page import MainPage
from steps.db_steps import GkrDbSteps
from steps.user_steps import GkrUserSteps


@pytest.mark.usefixtures('config')
@allure.feature('History')
@allure.story('Operator')
class TestOperatorHistory:

    def test_history_search_by_fio(self, config, teardown):

        global advance_one, advance_two, history_operator

        user = GkrUserSteps(config)
        db_user = GkrDbSteps(config)
        history_page = HistoryPage(config)

        history_operator = random_user(UserRoles.OPERATOR)
        db_user.create_user(history_operator)
        advance_one = db_user.fill_advance_queue(Departments.BEL_DEP, Services.SINGLE_WINDOW,
                                                 datetime.now() - timedelta(days=1),
                                                 ObjectTypes.STROI_OBJECT, history_operator)
        advance_two = db_user.fill_advance_queue(Departments.BEL_DEP, Services.GKN,
                                                 datetime.now() - timedelta(days=2),
                                                 ObjectTypes.DOMOVLADENIE, history_operator)

        user.login(history_operator.customers_data.mobile_phone, history_operator.password)
        user.waits_for_element_displayed(history_page.top_menu.LOGOUT)
        user.selects_from_main_menu(MainMenu.HISTORY)
        # поиск по имени
        user.search_history(advance_two.input_data.split()[2])
        user.should_see_list_size(history_page.SEARCH_ROWS, 1)
        user.should_matches_to_list_item(history_page.SEARCH_ROWS, contains_string(str(advance_two.id)))
        # поиск по фамилии
        user.search_history(advance_one.input_data.split()[1])
        user.should_see_list_size(history_page.SEARCH_ROWS, 1)
        user.should_matches_to_list_item(history_page.SEARCH_ROWS, contains_string(str(advance_one.id)))
        # поиск по отчеству
        user.search_history(advance_two.input_data.split()[3])
        user.should_see_list_size(history_page.SEARCH_ROWS, 1)
        user.should_matches_to_list_item(history_page.SEARCH_ROWS, contains_string(str(advance_two.id)))

    def test_history_search_empty(self, config, teardown):

        global advance_one, advance_two, history_operator

        advance_one = None
        advance_two = None
        user = GkrUserSteps(config)
        db_user = GkrDbSteps(config)
        main_page = MainPage(config)
        history_operator = random_user(UserRoles.OPERATOR)
        db_user.create_user(history_operator)

        user.login(history_operator.customers_data.mobile_phone, history_operator.password)
        user.waits_for_element_displayed(main_page.top_menu.LOGOUT)
        user.selects_from_main_menu(MainMenu.HISTORY)
        user.should_see_text(ConfirmationMessages.HISTORY_EMPTY)

        user.reloads_page()
        user.search_history(randrus_str(7))
        user.should_see_text(ConfirmationMessages.HISTORY_EMPTY)


@pytest.fixture(scope='function')
def teardown(request):
    def fin():
        config = getattr(request, '_funcargs')['config']
        db_steps = GkrDbSteps(config)
        db_steps.delete_user_by_mobile(history_operator.customers_data.mobile_phone)
        if advance_one is not None:
            db_steps.delete_advance_by_id(advance_one.id, advance_two.id)

    request.addfinalizer(fin)
