# coding=utf-8
import ast
from datetime import datetime, timedelta

import pytest
from hamcrest import assert_that, equal_to
from sqlalchemy import create_engine, and_
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.functions import count
from tabulate import tabulate

from db.qsystem import Advance, Department, Users, Clients

departments = list(ast.literal_eval(getattr(pytest, 'config').option.data))
db_login = 'gluser'
gl_db = 'gldb'
gl_host = 'glhost'
gl_password = 'dbpwd'
dep_password = 'deppwd'
date_from = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
date_to = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')


@pytest.mark.parametrize("name, host, db", departments)
def test_advances_sync(name, host, db):
    advances = advances_sync(name, host, db)
    assert_that(advances[0], equal_to(advances[1]), advances[2].format(name))


@pytest.mark.parametrize("name, host, db", departments)
def test_clients_sync(name, host, db):
    test_data = " c " + date_from + " по " + date_to
    clients = clients_sync(name, host, db)
    assert_that(clients[0], equal_to(clients[1]), u"Данные в таблице clients подразделения '" + name +
                "' за период" + test_data + " не соответствуют данным глобального сервера")


def advances_sync(name, host, db):
    gl_session = init_db(gl_host, gl_db, db_login, gl_password)
    dep_session = init_db(host, db, db_login, dep_password)

    # Выбирает из advance все записи с advance_time >= "сегодня + 1 день" и до последней даты
    start_day = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    did = gl_session.query(Department).filter(Department.name.like('%' + name + '%')).first().id
    filter_ = and_(Advance.department_id == did, Advance.advance_time >= start_day)
    gl_advances = gl_session.query(Advance.id, Advance.advance_time).filter(filter_).all()
    dep_advances = dep_session.query(Advance.id, Advance.advance_time).filter(filter_).all()

    advances_text = ""
    gl_dep_advances = ""
    dep_gl_advances = ""

    if len(gl_advances) != len(dep_advances):
        diff_gl_dep = list(set(gl_advances) - set(dep_advances))
        diff_dep_gl = list(set(dep_advances) - set(gl_advances))

        advances_text = u"Всего талонов на сервере отделения '{0}' : " + str(len(dep_advances)) + " шт.\n" + \
                        u"Всего талонов на глобальном сервере для отделения '{0}' : " + str(len(gl_advances)) + " шт.\n"

        if len(diff_gl_dep) != 0:
            gl_dep_advances = u"В базе отделения '{0}' отсутствуют талоны из базы глобального, " + \
                              str(len(diff_gl_dep)) + " шт.\n" + \
                              tabulate(diff_gl_dep, ["Id талона", "Дата записи"], tablefmt="fancy_grid")

        if len(diff_dep_gl) != 0:
            dep_gl_advances = u"В базе глобального сервера отсутствуют талоны из базы локального '{0}', " + \
                              str(len(diff_dep_gl)) + " шт.\n" + \
                              tabulate(diff_dep_gl, ["Id талона", "Дата записи"], tablefmt="fancy_grid")

        advances_text = advances_text + gl_dep_advances + "\n" + dep_gl_advances

    gl_session.close()
    dep_session.close()

    return [len(dep_advances), len(gl_advances), advances_text]


def clients_sync(name, host, db):
    gl_session = init_db(gl_host, gl_db, db_login, gl_password)
    dep_session = init_db(host, db, db_login, dep_password)

    # Подсчитывает количество записей в clients за предыдущие date_to - date_from дней.
    did = gl_session.query(Department).filter(Department.name.like('%' + name + '%')).first().id
    dep_users_id = list(map(lambda Users: Users.id, gl_session.query(Users).filter(Users.department_id == did).all()))
    clients_filter = and_(
        Clients.user_id.in_(dep_users_id),
        Clients.stand_time.between(date_from, date_to)
    )
    gl_clients_count = gl_session.query(count(Clients.id)).filter(clients_filter).first()[0]
    dep_clients_count = dep_session.query(count(Clients.id)).filter(clients_filter).first()[0]

    gl_session.close()
    dep_session.close()

    return [dep_clients_count, gl_clients_count]


def init_db(host, db, user, password):
    try:
        engine = create_engine('mysql+mysqldb://' + user + ':' + password + '@' + host +
                               '/' + db + '?charset=utf8', echo=False, connect_args={'connect_timeout': 15})
        engine.connect()
        return sessionmaker(bind=engine)()
    except OperationalError as exception:
        assert_that(None, u"Ошибка при соединении с базой данных '" + host + "\nОшибка : " + str(exception))
