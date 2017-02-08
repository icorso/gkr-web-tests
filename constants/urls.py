# coding=utf-8
from enum import Enum


class Urls(Enum):
    MAIN = '/'
    LOGIN = '/login'
    LOGOUT = '/logout'
    FORGOT = '/forgot'
    REGISTRATION = '/registration'
    REGISTRATOR = '/registrator'
    PROFILE = '/customer/profile'
    QUEUE = '/customer/queue'
    TICKET = '/customer/ticket'
    RELOAD = '/administrator/queue/reload'

    ADMIN_BLOCKING = '/administrator/blocking'
    ADMIN_DEPS = '/administrator/department/'
    ADMIN_IMPORT = '/administrator/registrator/import'
    ADMIN_CUSTOMERS = '/administrator/registrator/list'
    ADMIN_CUSTOMER_EDIT = '/administrator/registrator/edit?id=%s'
    ADMIN_GROUP_ROLES = '/administrator/group-roles/'
    ADMIN_NEWS = '/administrator/news'
    ADMIN_TICKED_EDIT = '/administrator/registrator/aedit?id=%s'
    ADMIN_TCUSTOMER_EDIT = '/administrator/registrator/edit?tid=%s'
    ADMIN_SCHEDULE = '/administrator/schedule'
    ADMIN_STANDARDS = '/administrator/standard'
    ADMIN_SERVICES = '/administrator/ServiceManagement'
    ADMIN_STATISTIC = '/administrator/statistic'
    ADMIN_UNCONFIRMED_CUSTOMERS = '/administrator/registrator/tlist'

    def __init__(self, url):
        self.url = url

    def __str__(self):
        return self.url

    def url(self):
        return self.url
