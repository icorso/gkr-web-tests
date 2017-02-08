# coding=utf-8
from enum import Enum


class Calendars(Enum):
    TEST_CALENDAR = ('Тестовый календарь', '1442476554664')
    PROD_CALENDAR = ('Общий календарь', '1')
    BEL_CALENDAR = ('белогорск', '5')
    FEO_CALENDAR = ('феодосия', '34')

    def __init__(self, name, id_):
        self.name = name
        self.id = id_

    def __str__(self):
        return self.name.__repr__()

    def name(self):
        return self.name

    def id(self):
        return self.id
