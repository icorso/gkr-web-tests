# coding=utf-8
from datetime import datetime, timedelta

import pytest
from krtech.configuration import TestConfig, ConftestOptions

from data.users import CUSTOMER, OPERATOR, LEGAL, ADMIN
from steps.db_steps import GkrDbSteps

tc = TestConfig()
tc.base_url = "http://127.0.0.1"
tc.element_init_timeout = 0.1
tc.element_wait = 10

c = ConftestOptions(tc)


def pytest_addoption(parser):
    parser.addoption("--attempts", action="store", default=3)
    parser.addoption("--tests_root", action="store", default=None)
    parser.addoption("--timeslot_date", action="store",
                     default=(datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'))
    parser.addoption("--threads", action="store", default=1)
    parser.addoption("--mysqldb", action="store", default="qsystem")
    parser.addoption("--mysqlhost", action="store", default="127.0.0.1")
    parser.addoption("--mysqlport", action="store", default="3306")
    parser.addoption("--mysqluser", action="store", default="dbuser")
    parser.addoption("--mysqlpassword", action="store", default="dbpwd")

    c.pytest_addoption(parser)


@pytest.mark.tryfirst
def pytest_runtest_makereport(item, call, __multicall__):
    return c.pytest_runtest_makereport(item, call, __multicall__)


@pytest.yield_fixture(scope='session')
def config(request):
    c.config(request)
    for k, v in request.config.option.__dict__.items():
        setattr(tc, k, v)

    db_user = GkrDbSteps(tc)
    db_user.create_user(CUSTOMER)
    db_user.create_user(OPERATOR)
    db_user.create_user(LEGAL)
    db_user.create_user(ADMIN)

    tc.driver.set_window_size(1280, 900)

    yield tc
    tc.driver.quit()
