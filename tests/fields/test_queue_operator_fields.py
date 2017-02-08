# coding=utf-8

import allure
import pytest

from constants.departments import Departments
from constants.messages import ErrorMessages
from constants.user_roles import UserRoles
from data.registration_invalid_data import mobile, passport, fio
from data.users import random_user
from pages.queue_page import QueuePage
from steps.db_steps import GkrDbSteps
from steps.user_steps import GkrUserSteps


@pytest.mark.usefixtures('config')
@allure.feature('Queue')
@allure.story('Validation')
class TestQueueFieldsValidation:

    def test_queue_operator_empty_fields(self, config, setup, teardown):
        user = GkrUserSteps(config)
        queue_page = QueuePage(config)
        user.clicks(queue_page.SUBMIT)
        user.waits_for_element_displayed(queue_page.ERROR_TEXT)
        user.should_see_text_in_list(queue_page.ERROR_TEXT, ErrorMessages.ADDRESS_MISMATCH.text)
        user.should_see_text_in_list(queue_page.ERROR_TEXT, ErrorMessages.DATE_NOT_SPECIFIED.text)
        user.should_see_text_in_list(queue_page.ERROR_TEXT,
                                     ErrorMessages.PASSPORT_NUMBER_ONLY_DIGITS.text,
                                     ErrorMessages.PASSPORT_NUMBER.text)
        user.should_see_text_in_list(queue_page.ERROR_TEXT, ErrorMessages.PASSPORT_SERIAL.text,
                                     ErrorMessages.PASSPORT_SERIAL_ONLY_DIGITS.text)
        user.should_see_text_in_list(queue_page.ERROR_TEXT, ErrorMessages.NAME_EMPTY.text,
                                     ErrorMessages.NAME_LENGTH.text)
        user.should_see_text_in_list(queue_page.ERROR_TEXT, ErrorMessages.SURNAME_EMPTY.text,
                                     ErrorMessages.SURNAME_LENGTH.text)

    @pytest.mark.parametrize('mobile', mobile)
    def test_queue_operator_mobile_field(self, config, mobile, setup, teardown):
        user = GkrUserSteps(config)
        queue_page = QueuePage(config)
        user.enters_text(queue_page.MOBILE, mobile)
        user.clicks(queue_page.SUBMIT)
        user.waits_for_element_displayed(queue_page.ERROR_TEXT)
        user.should_see_text_in_list(queue_page.ERROR_TEXT, ErrorMessages.MOBILE_QUEUE.text)

    @pytest.mark.parametrize('passport', passport)
    def test_queue_operator_passport_serial_field(self, config, passport, setup, teardown):
        user = GkrUserSteps(config)
        queue_page = QueuePage(config)
        user.enters_text(queue_page.PASSPORT_SERIAL, passport)
        user.enters_text(queue_page.PASSPORT_NUMBER, passport)
        user.clicks(queue_page.SUBMIT)
        user.waits_for_element_displayed(queue_page.ERROR_TEXT)
        user.should_see_text_in_list(queue_page.ERROR_TEXT,
                                     ErrorMessages.PASSPORT_SERIAL.text, ErrorMessages.PASSPORT_SERIAL_ONLY_DIGITS.text)
        user.should_see_text_in_list(queue_page.ERROR_TEXT,
                                     ErrorMessages.PASSPORT_NUMBER.text, ErrorMessages.PASSPORT_NUMBER_ONLY_DIGITS.text)

    @pytest.mark.parametrize('fio', fio)
    def test_queue_operator_fio_field(self, config, fio, setup, teardown):
        user = GkrUserSteps(config)
        queue_page = QueuePage(config)
        user.enters_text(queue_page.SURNAME, fio)
        user.enters_text(queue_page.NAME, fio)
        user.enters_text(queue_page.PATRONYMIC, fio)
        user.clicks(queue_page.SUBMIT)
        user.waits_for_element_displayed(queue_page.ERROR_TEXT)
        user.should_see_text_in_list(queue_page.ERROR_TEXT, ErrorMessages.NAME_EMPTY.text,
                                     ErrorMessages.NAME_LENGTH.text)
        user.should_see_text_in_list(queue_page.ERROR_TEXT, ErrorMessages.SURNAME_EMPTY.text,
                                     ErrorMessages.SURNAME_LENGTH.text)

    def test_queue_operator_empty_locality_field(self, config, setup, teardown):
        user = GkrUserSteps(config)
        queue_page = QueuePage(config)
        user.chooses_from_select(queue_page.CITY, Departments.BEL_DEP.short_name)
        user.clicks(queue_page.SUBMIT)
        user.waits_for_element_displayed(queue_page.ERROR_TEXT)
        user.should_see_text_in_list(queue_page.ERROR_TEXT, ErrorMessages.ADDRESS_MISMATCH.text)

    def test_queue_operator_empty_street_field(self, config, setup, teardown):
        user = GkrUserSteps(config)
        queue_page = QueuePage(config)
        user.chooses_from_select(queue_page.CITY, Departments.BEL_DEP.short_name)
        user.enters_suggest(queue_page.LOCALITY, 'с. Александровка')

        user.clicks(queue_page.SUBMIT)
        user.waits_for_element_displayed(queue_page.ERROR_TEXT)
        user.should_see_text_in_list(queue_page.ERROR_TEXT, ErrorMessages.ADDRESS_MISMATCH.text)

    def test_queue_operator_empty_house_field(self, config, setup, teardown):
        user = GkrUserSteps(config)
        queue_page = QueuePage(config)
        user.chooses_from_select(queue_page.CITY, Departments.BEL_DEP.short_name)
        user.enters_suggest(queue_page.LOCALITY, 'с. Александровка')
        user.enters_suggest(queue_page.STREET, 'ул. Павлова')

        user.clicks(queue_page.SUBMIT)
        user.waits_for_element_displayed(queue_page.ERROR_TEXT)
        user.should_see_text_in_list(queue_page.ERROR_TEXT, ErrorMessages.ADDRESS_MISMATCH.text)


@pytest.fixture(scope='function')
def setup(request):
    global fields_operator
    config = getattr(request, '_funcargs')['config']

    db_user = GkrDbSteps(config)
    queue_page = QueuePage(config)

    fields_operator = random_user(UserRoles.OPERATOR)
    db_user.create_user(fields_operator)

    user = GkrUserSteps(config)
    user.login(fields_operator.customers_data.mobile_phone, fields_operator.password)

    user.waits_for_element_displayed(queue_page)


@pytest.fixture(scope='function')
def teardown(request):
    def fin():
        config = getattr(request, '_funcargs')['config']
        db_user = GkrDbSteps(config)
        db_user.delete_user_by_mobile(fields_operator.customers_data.mobile_phone)
    request.addfinalizer(fin)
