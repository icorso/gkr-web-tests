# coding=utf-8
from datetime import datetime, timedelta

import allure
import pytest
from krtech.utils import randrus_str

from constants.urls import Urls
from data.admins_data import random_news
from data.users import ADMIN
from db.qsystem import News
from pages.admin.add_news_page import AddNewsPage
from pages.admin.edit_news_page import EditNewsPage
from pages.admin.news_page import NewsAdminPage
from pages.main_page import MainPage
from steps.db_steps import GkrDbSteps
from steps.user_steps import GkrUserSteps


@pytest.mark.usefixtures('config')
@allure.feature('Administration')
@allure.story('News')
class TestNews:

    def test_news_creation(self, config, setup, teardown):
        global news
        user = GkrUserSteps(config)
        db_user = GkrDbSteps(config)
        news_page = NewsAdminPage(config)
        add_news_page = AddNewsPage(config)

        title = 'created_' + randrus_str(10)
        desc = randrus_str(10)
        date = datetime.now().strftime('%d.%m.%Y')

        user.opens(Urls.ADMIN_NEWS)
        user.clicks(news_page.CREATE_NEWS)
        user.should_see_element(add_news_page)
        user.selects_checkbox(add_news_page.IS_PUBLISHED)
        user.enters_text(add_news_page.PUBLISH_DATE, date)
        user.enters_text(add_news_page.TITLE, title)
        user.enters_text(add_news_page.DESC, desc)
        user.clicks(add_news_page.SUBMIT)
        user.waits_for_ajax()
        user.should_not_see_element(add_news_page.ERROR)
        user.should_see_element(news_page)

        news_row = news_page.NEWS_LIST.get_row_by_title(title)
        user.should_see_table_entry_value(news_row, 'title', title)
        user.should_see_table_entry_value(news_row, 'desc', desc)
        user.should_see_table_entry_value(news_row, 'date', date)
        user.should_see_news_published(news_row.id, True)

        news = db_user.query_first(News, News.news_id == news_row.id)

    def test_news_edit(self, config, setup, teardown):
        global news
        title = 'edited_' + randrus_str(10)
        desc = randrus_str(10)
        date = (datetime.now() + timedelta(days=1)).strftime('%d.%m.%Y')

        user = GkrUserSteps(config)
        db_user = GkrDbSteps(config)
        edit_news_page = EditNewsPage(config)
        news_page = NewsAdminPage(config)

        news = db_user.creates_news(random_news())

        user.opens(Urls.ADMIN_NEWS.url + '/edit?newsId=' + str(news.news_id))
        user.should_see_element(edit_news_page)
        user.enters_text(edit_news_page.TITLE, title)
        user.enters_text(edit_news_page.DESC, desc)
        user.enters_text(edit_news_page.PUBLISH_DATE, date)
        user.unselects_checkbox(edit_news_page.IS_PUBLISHED)
        user.clicks(edit_news_page.SUBMIT)

        user.waits_for_element_displayed(news_page)
        news_row = news_page.NEWS_LIST.get_row_by_title(title)
        user.should_see_table_entry_value(news_row, 'title', title)
        user.should_see_table_entry_value(news_row, 'desc', desc)
        user.should_see_table_entry_value(news_row, 'date', date)
        user.should_see_news_published(news.news_id, False)


@pytest.fixture(scope='function')
def setup(request):
    config = getattr(request, '_funcargs')['config']
    main_page = MainPage(config)
    user = GkrUserSteps(config)
    user.login(ADMIN.login, ADMIN.password)
    user.waits_for_element_displayed(main_page.top_menu.LOGOUT)


@pytest.fixture(scope='function')
def teardown(request):
    def fin():
        config = getattr(request, '_funcargs')['config']
        db_steps = GkrDbSteps(config)
        db_steps.delete_news_by_id(news.news_id)

    request.addfinalizer(fin)
