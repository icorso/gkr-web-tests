# coding=utf-8
from subprocess import call
from time import sleep

from hamcrest import *
from krtech.steps.user_steps import UserSteps

from constants.urls import Urls
from db.qsystem import Customers
from pages.admin.news_page import NewsAdminPage
from pages.common_blocks import LoginForm, TopMenu, MainMenu
from pages.history_page import HistoryPage
from pages.queue_page import QueuePage
from pages.registration_page import RegistrationPage
from steps import randrus_str, rand_num, rand_str, allure


class GkrUserSteps(UserSteps):
    def __init__(self, config):
        super().__init__(config)
        self.mysqlhost = config.mysqlhost
        self.login_form = LoginForm(config)
        self.main_menu = MainMenu(config)
        self.top_menu = TopMenu(config)
        self.reg_page = RegistrationPage(config)
        self.queue_page = QueuePage(config)
        self.news_page = NewsAdminPage(config)

    @allure.step("Открывает страницу '{1}'")
    def opens(self, url, timeout=5):
        self.driver.get(str(url))
        self.waits_for_ajax(timeout)

    @allure.step("Перегружает текущую страницу")
    def reloads_page(self, timeout=5):
        self.config.driver.refresh()
        self.waits_for_ajax(timeout)

    @allure.step("Авторизует пользователя '{1}'")
    def login(self, username, password):
        self.opens(Urls.LOGOUT.url)
        self.should_see_element(self.top_menu.LOGIN_LINK)
        self.clicks(self.top_menu.LOGIN_LINK)
        self.waits_for_element_displayed(self.login_form)
        self.enters_text(self.login_form.LOGIN, username)
        self.enters_text(self.login_form.PASSWORD, password)
        self.clicks(self.login_form.SUBMIT)
        self.waits_for_ajax(10)

    @allure.step("Деавторизует текущего пользователя")
    def logout(self):
        self.opens(Urls.LOGOUT.url)

    @allure.step("Выбирает пункт '{1}' из главного меню'")
    def selects_from_main_menu(self, main_menu_item):
        item = self.main_menu.MENU.get_element_contains_text(main_menu_item.item)
        assert_that(item, not_none(), u"В главном меню пункт '" + main_menu_item.item + "' отсутствует")
        item.element.click()
        self.waits_for_ajax()

    @allure.step("Ищет в истории оператора по критерию '{1}'")
    def search_history(self, search_criteria):
        history_page = HistoryPage(self.config)
        self.should_see_element(history_page)
        self.enters_text(history_page.SEARCH_FIELD, search_criteria)
        self.clicks(history_page.SEARCH_BUTTON)
        self.waits_for_ajax()

    @allure.step("Вводит текст '{2}' в '{1}' с саджестом")
    def enters_suggest(self, input_, text):
        self.waits_for_element_enabled(input_)
        input_.input.clear()
        input_.input.send_keys(text)
        self.waits_for_ajax()
        sleep(1)
        self.selects_from_list_by_text(self.queue_page.SUGGEST, text)

    @allure.step("Перезагружает веб-сервер")
    def restarts_server(self):
        call(["ssh", "root@" + self.mysqlhost, "/opt/tomcat/bin/shutdown.sh"])
        sleep(1)
        call(["ssh", "root@" + self.mysqlhost, "/opt/tomcat/bin/startup.sh"])
        sleep(30)

    @allure.step("Заполняет форму регистрации физ.лица данными: {1}")
    def fill_registration_form(self, customer):
        self.should_see_element(self.reg_page)
        self.enters_text(self.reg_page.SURNAME, customer.customers_data.surname)
        self.enters_text(self.reg_page.NAME, customer.customers_data.name)
        self.enters_text(self.reg_page.PATRONYMIC, customer.customers_data.patronymic)
        if self.is_element_present(self.reg_page.BIRTHDAY):
            self.enters_text(self.reg_page.BIRTHDAY, customer.customers_data.birthday.strftime('%d.%m.%Y'))
        self.enters_text(self.reg_page.PASSPORT_SERIAL, customer.customers_data.serial)
        self.enters_text(self.reg_page.PASSPORT_NUMBER, customer.customers_data.no)
        self.enters_text(self.reg_page.ISSUE, customer.customers_data.issue)
        self.enters_text(self.reg_page.ISSUE_DATE, customer.customers_data.when_at.strftime('%d.%m.%Y'))
        self.enters_text(self.reg_page.MOBILE, customer.customers_data.mobile_phone)
        self.enters_text(self.reg_page.EMAIL, customer.customers_data.email)

        self.clicks(self.reg_page.SUBMIT)

    @allure.step("Заполняет форму регистрации юр.лица данными: {1}")
    def fill_legal_registration_form(self, customer):
        self.enters_text(self.reg_page.SURNAME, customer.customers_data.surname)
        self.enters_text(self.reg_page.NAME, customer.customers_data.name)
        self.enters_text(self.reg_page.PATRONYMIC, customer.customers_data.patronymic)
        self.enters_text(self.reg_page.INN, customer.customers_data.inn)
        self.enters_text(self.reg_page.MOBILE, customer.customers_data.mobile_phone)
        self.enters_text(self.reg_page.EMAIL, customer.customers_data.email)

        self.clicks(self.reg_page.SUBMIT)

    @allure.step("Заполняет форму постановки в очередь произвольными данными")
    def fill_random_operator_queue(self):
        queue_page = QueuePage(self.config)
        customer = Customers
        customer.name = randrus_str(10)
        customer.surname = randrus_str(10)
        customer.patronymic = randrus_str(10)
        customer.mobile_phone = '9777' + rand_num(6)
        customer.email = rand_num(6) + '@' + rand_str(5) + '.com'
        customer.no = rand_num(6)
        customer.serial = rand_num(4)
        customer.issue = randrus_str(25)
        customer.when_at = '09/01/2015'

        self.enters_text(queue_page.SURNAME, customer.surname)
        self.enters_text(queue_page.NAME, customer.name)
        self.enters_text(queue_page.PATRONYMIC, customer.patronymic)
        self.enters_text(queue_page.MOBILE, customer.mobile_phone)
        self.enters_text(queue_page.PASSPORT_SERIAL, customer.serial)
        self.enters_text(queue_page.PASSPORT_NUMBER, customer.no)
        self.enters_text(queue_page.ISSUE, customer.issue)
        self.enters_text(queue_page.ISSUE_DATE, customer.when_at)
        return customer

    @allure.step('Подтверждает форму регистрации кастомером')
    def submit_regform(self):
        self.should_see_element(self.reg_page)
        self.clicks(self.reg_page.CHECKBOX)
        self.clicks(self.reg_page.SUBMIT)
        self.clicks_dialog_button(self.reg_page.dialogs.REG_CONFIRM_DIALOG, 'Зарегистрироваться')

    def scrolls_to_element(self, element):
        self.driver.execute_script('return arguments[0].scrollIntoView();', element)

    @allure.step("Проверяет текст '{2}' в '{1}'")
    def should_see_dialog_text(self, dialog, text):
        assert_that(dialog.content.text, equal_to(str(text)), u'Текст в диалоговом окне не соответствует ожидаемому')

    @allure.step("Нажимает кнопку '{2}' в '{1}'")
    def clicks_dialog_button(self, dialog, button_text):
        self.waits_for_element_displayed(dialog)
        dialog.get_button_by_text(button_text).click()

    @allure.step("Закрывает '{1}'")
    def close(self, dialog):
        dialog.close.click()

    @allure.step("Раскрывает окно браузера на весь экран")
    def browser_maximize(self):
        self.driver.maximize_window()

    @allure.step("Проверяет значения {2},{3},{4} в списке истории услуг")
    def should_see_history_services(self, history_item, header, info, time):
        assert_that(history_item.header, equal_to(header))
        assert_that(history_item.info, equal_to(info))
        assert_that(history_item.time, equal_to(time))

    @allure.step("Проверяет is_published = '{2}' для новости с id = '{1}'")
    def should_see_news_published(self, news_id, is_published):
        news_row = self.news_page.NEWS_LIST.get_row_by_news_id(news_id)
        if is_published:
            assert_that(news_row.element.get_attribute('style'), not_(contains_string('line-through')),
                        u'Новость отмечена как не опубликованная')
        else:
            assert_that(news_row.element.get_attribute('style'), contains_string('line-through'),
                        u'Новость отмечена как опубликованная')

    @allure.step("Проверяет запись {2}:{3} в таблице '{1}'")
    def should_see_table_entry_value(self, entry, column_name, value):
        assert_that(str(entry.__getattribute__(column_name)), equal_to(str(value)), u'Значение атрибута \"'
                    + column_name + '\" для \"' + str(entry) + '\" не соответствует ожидаемому')

    @allure.step("Проверяет отсутствие элемента отображения ошибки у поля {1}")
    def should_not_see_field_error(self, input):
        has_error_field = False
        try:
            input.error
            has_error_field = True
        except:
            pass

        assert_that(has_error_field, is_(False), "Поле не должно содержать элемент отображения ошибки")
