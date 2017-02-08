# coding=utf-8
from datetime import datetime
from time import sleep

from hamcrest import assert_that, equal_to, contains_string, not_none
from krtech.steps.db_steps import DbSteps
from sqlalchemy import and_
from sqlalchemy import create_engine

from constants.service_groups import ServiceGroups
from data.admins_data import random_break
from data.users import OPERATOR
from db.qsystem import Customers, AclUserRoles, AclUsers, History, Advance, Department, Services, News, NewsImages, \
    ServicesUsers, DepartRegion, DepartServiceGroup, Schedule, Break
from steps import randrus_str, rand_num, allure


class GkrDbSteps(DbSteps):
    def __init__(self, config):
        self.host = config.mysqlhost
        self.user = config.mysqluser
        self.password = config.mysqlpassword
        self.db = config.mysqldb
        self.port = config.mysqlport
        self.engine = create_engine('mysql+mysqldb://' + self.user + ':' + self.password + '@' + self.host + ':'
                                    + self.port + '/' + self.db + '?charset=utf8', echo=False)

    @allure.step("Удаляет запись из таблицы advance по id = '{1}'")
    def delete_advance_by_id(self, *id_):
        for i in id_:
            history_id = None
            if (len(self.query_all(Advance, Advance.id == i))) > 0:
                history_id = self.query_first(Advance, Advance.id == i).history_id
                self.delete(Advance, Advance.id == i)

            if (len(self.query_all(History, History.id == history_id))) > 0:
                self.delete(History, History.id == history_id)

    @allure.step("Удаляет пользователя из базы по номеру телефона '{1}'")
    def delete_user_by_mobile(self, mobile):
        if (len(self.query_all(Customers, Customers.mobile_phone == mobile))) > 0:
            self.delete(Customers, Customers.mobile_phone == mobile)

        if (len(self.query_all(AclUsers, AclUsers.name == mobile))) > 0:
            self.delete(AclUsers, AclUsers.name == mobile)

        if len(self.query_all(History, History.mobile_phone == mobile)) > 0:
            self.delete(History, History.mobile_phone == mobile)

        if len(self.query_all(Advance, Advance.customer_id.is_(None))) > 0:
            self.delete(Advance, Advance.customer_id.is_(None))

    @allure.step('Удаляет предварительные записи за период {1}')
    def delete_advances(self, date, department=None):
        """
        Удаление предварительно записанных за определённую дату и для отделения (если указано)
        :param date: дата в формате 'гггг-мм-дд чч:мм:сс'
        :param department: подразделение из constants/departments.py
        :return: число всех удалённых записей
        """
        if department is not None:
            dep_id = self.query_first(Department, Department.name == department.name).id
            advances = self.query_all(Advance,
                                      and_(Advance.advance_time.like(date + '%'),
                                           Advance.department_id == str(dep_id)))
        else:
            advances = self.query_all(Advance, Advance.advance_time.like(date + '%'))
        l = list(map(lambda x: x.id, advances))
        for i in l:
            self.delete_advance_by_id(i)
        return len(l)

    def creates_tcustomer(self, tcustomer):
        self.add(tcustomer.customers_data)

    def create_user(self, customer):
        c = self.query_first(Customers, Customers.mobile_phone == customer.customers_data.mobile_phone)

        if c is None:
            self.delete_user_by_mobile(customer.customers_data.mobile_phone)
            acl_users = AclUsers(
                name=customer.customers_data.mobile_phone,
                pwd=customer.password
            )
            self.add(acl_users)

            a1 = AclUsers
            customer.customers_data.uid = self.query_first(a1, a1.name == customer.customers_data.mobile_phone).id
            self.add(customer.customers_data)

            acl_user_roles = AclUserRoles(
                user_id=self.query_first(AclUsers, AclUsers.name == customer.customers_data.mobile_phone).id,
            )

            acl_user_roles.role_id = customer.role.id
            self.add(acl_user_roles)

    @allure.step('Заполняет очередь {1} на время {2}, тип объекта недвижимости {3}')
    def fill_advance_queue(self, department, service, adv_time, object_type, operator=OPERATOR,
                           creation_time=str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))):

        operator_id = self.query_first(Customers,
                                       Customers.mobile_phone == operator.customers_data.mobile_phone).id
        dep_id = self.query_first(Department, Department.name == department.name).id

        h = History(
            cid=operator_id,
            created=creation_time,
            issue=randrus_str(15),
            mobile_phone='9777' + rand_num(7),
            name=randrus_str(7),
            surname=randrus_str(7),
            patronymic=randrus_str(7),
            when_at=creation_time,
            no=rand_num(6),
            serial=rand_num(4)
        )
        if operator.customers_data.inn is not None:
            h.inn = operator.customers_data.inn
        self.add(h)
        sleep(1)
        history_id = self.query_first(History, History.mobile_phone == h.mobile_phone).id

        a = Advance(
            service_id=service.id,
            department_id=dep_id,
            customer_id=operator_id,
            advance_time=adv_time,
            objects_count=object_type.id,
            input_data='Посетитель: ' + h.surname + ' ' + h.name + ' ' + h.patronymic + '\nТип объекта недвижимости: '
                       + str(object_type) + '\n\nНедвижимость: ' + randrus_str(10),
            comments='Паспорт: ' + h.serial + ' ' + h.no,
            update_time=creation_time,
            history_id=history_id,
        )
        self.add(a)
        sleep(1)
        advance = self.query_first(Advance, Advance.input_data == a.input_data)
        return advance

    @allure.step('Проверяет group_id {2} у услуги для advance_id = {1}')
    def should_see_service_group_id(self, advance_id, group_id):
        service_id = self.query_first(Advance, Advance.id == advance_id).service_id

        assert_that(self.query_first(Services, Services.id == service_id).group_id, equal_to(group_id),
                    u'Id группы не соответствует ожидаемому')

    @allure.step('Проверяет удалённую услугу {1} в базе данных')
    def should_see_removed_ticket(self, service_id):
        deleted_advance = self.query_first(Advance, Advance.id == service_id)
        now = datetime.now().strftime('%Y-%m-%d %H:%M')
        assert_that(str(deleted_advance.deleted), contains_string(now),
                    u"Услуга id '" + str(service_id) + "' не отмечена в базе как удаленная")
        assert_that(str(deleted_advance.update_time), contains_string(now),
                    u"Услуга id '" + str(service_id) + "' не отмечена в базе как обновлённая")

    @allure.step('Устанавливает блокировку пользователя {1} в базе данных')
    def blocks_user(self, mobile_phone, is_blocked=1):
        user = self.query_first(Customers, Customers.mobile_phone == mobile_phone)
        assert_that(user, not_none, 'Пользователь ' + mobile_phone + ' не найден')
        params = {'blocked': is_blocked}
        self.update(Customers, Customers.mobile_phone == mobile_phone, params)

    @allure.step("Создаёт новость")
    def creates_news(self, news):
        self.add(news)
        return self.query_first(News, News.title == news.title)

    @allure.step("Создаёт услугу")
    def creates_service(self, service):
        self.add(service)
        return self.query_first(Services, Services.name == service.name)

    @allure.step("Удаляет запись из таблицы news по id = '{1}'")
    def delete_news_by_id(self, *id_):
        for i in id_:
            if (len(self.query_all(News, News.news_id == i))) > 0:
                news_id = self.query_first(News, News.news_id == i).news_id
                if (len(self.query_all(NewsImages, NewsImages.news_id == news_id))) > 0:
                    self.delete(NewsImages, NewsImages.news_id == news_id)
                self.delete(News, News.news_id == news_id)

    @allure.step("Удаляет запись из таблицы services по id = '{1}'")
    def delete_service_by_id(self, *id_):
        for i in id_:
            if (len(self.query_all(Services, Services.id == i))) > 0:
                if (len(self.query_all(ServicesUsers, ServicesUsers.service_id == i))) > 0:
                    self.delete(ServicesUsers, ServicesUsers.service_id == i)

                self.delete(Services, Services.id == i)

    @allure.step("Удаляет запись из таблицы departments по имени = '{1}'")
    def delete_department_by_name(self, *name):
        for i in name:
            if len(self.query_all(Department, Department.name == i)) > 0:
                self.delete(Department, Department.name == i)

    @allure.step("Создаёт департамент {1}, {2}")
    def creates_department(self, department, *location, phys_percent=None, legal_percent=None):
        self.add(department)
        department = self.query_first(Department, Department.name == department.name)

        for i in location:
            self.add(
                    DepartRegion(
                            region_code=i.id,
                            depart_id=department.id
                    )
            )

        if phys_percent:
            self.add(
                DepartServiceGroup(
                    department_id=department.id,
                    sevice_group_id=ServiceGroups.PHYS_PERSON.id,
                    percent=phys_percent
                )
            )

        if legal_percent:
            self.add(
                DepartServiceGroup(
                    department_id=department.id,
                    sevice_group_id=ServiceGroups.LEGAL_PERSON.id,
                    percent=legal_percent
                )
            )

        return department

    @allure.step("Удаляет запись из таблицы break по id = '{1}'")
    def delete_break_by_id(self, breaks_ids):

        for i in breaks_ids:
            if len(self.query_all(Break, Break.id == i)) > 0:
                self.delete(Break, Break.id == i)

    @allure.step("Удаляет запись из таблицы schedule по имени = '{1}'")
    def delete_schedule_by_name(self, name):
        schedule = self.query_first(Schedule, Schedule.name == name)
        breaks = []
        for i in range(1, 7):
            break_id = schedule.__getattribute__('breaks_id' + str(i))
            if break_id is not None:
                breaks.append(break_id)

        self.delete(Schedule, Schedule.name == name)
        self.delete_break_by_id(breaks)

    @allure.step("Создаёт расписание")
    def creates_schedule(self, schedule):
        break1 = random_break(schedule.breaks_id1)
        self.add(break1)
        self.add(schedule)
        return self.query_first(Schedule, Schedule.name == schedule.name)

