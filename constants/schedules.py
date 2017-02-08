# coding=utf-8
from enum import Enum


class Schedules(Enum):
    TEST_SCHEDULE = ('Тестовое расписание', '1442476523109', '09:00:00', '16:00:00')
    PROD_SCHEDULE = ('План работы с 8.00 до 17.00', '1', '09:00:00', '16:00:00')
    BEL_SCHEDULE = ('белогорск', '5', '09:00:00', '19:00:00')
    FEO_SCHEDULE = ('феодосия', '34', '09:00:00', '19:00:00')

    def __init__(self, name, id_, start, end):
        self.name = name
        self.id = id_
        self.start = start
        self.end = end

    def __str__(self):
        return self.name.__repr__()

    def name(self):
        return self.name

    def id(self):
        return self.id

    def start(self):
        return self.start

    def end(self):
        return self.end
