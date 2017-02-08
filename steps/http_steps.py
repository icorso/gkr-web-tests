# coding=utf-8

from hamcrest import assert_that, contains_string
from krtech.steps.http_steps import HttpSteps
from requests import codes

from constants.urls import Urls
from data.users import ADMIN
from steps import allure


class GkrHttpSteps(HttpSteps):
    def __init__(self, config):
        super().__init__(config)

    @allure.step("Авторизует пользователя '{1}' через http")
    def login(self, username, password, url=None):
        # закомментировано для версии 1.3.6 с вынесеными сессиями и DAO в подпроекты
        s = self.HttpSession().with_url(self.base_url).submit()
        # sid = s.response.cookies['SESSION']
        params = {'username': username, 'password': password}
        # headers = {'X-Requested-With': 'XMLHttpRequest', 'SESSIONID': sid}
        # return s.with_method('post').with_headers(headers).with_params(params)\
        return s.with_method('post').with_params(params).with_url(self.base_url + '/login/ajax').submit()

    @allure.step("Выполняет запрос обновления очереди")
    def renew_queue(self):
        url = self.base_url + Urls.RELOAD.url
        assertion_text = u'Ошибка при выполнении запроса обновления очереди ' + url

        session = self.login(ADMIN.customers_data.mobile_phone, ADMIN.password)
        r = session\
            .with_url(url)\
            .with_method('post')\
            .submit().response
        self.should_see_response_status(r, codes.ok)
        assert_that(r.text, contains_string('Очередь успешно обновлена'), assertion_text)
