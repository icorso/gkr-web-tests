# coding=utf-8
from enum import Enum

from constants.calendars import Calendars
from constants.schedules import Schedules


class Departments(Enum):
    BEL_DEP = ('Белогорский районный отдел. РФ, Республика Крым, г. Белогорск, ул. Чобан-Заде/Мирошниченко, 24/10',
               'р-н. Белогорский',
               Schedules.BEL_SCHEDULE.id, Calendars.BEL_CALENDAR.id)
    FEO_DEP = ('Феодосийский городской отдел. РФ, Республика Крым, г. Феодосия, ул. Галерейная, 7а', 'г. Феодосия',
               Schedules.FEO_SCHEDULE.id, Calendars.FEO_CALENDAR.id)
    SUDAK_DEP = ('Судакский городской  отдел. РФ, Республика Крым, г. Судак, ул. Ленина, 85а', 'г. Судак',
                 Schedules.PROD_SCHEDULE.id, Calendars.PROD_CALENDAR.id)
    SIMF_DEP = ('Симферопольский отдел приема-выдачи документов Госкомрегистра. РФ, Республика Крым, г. Симферополь, '
                'пр. Победы, 165/1', 'г. Симферополь',
                 Schedules.PROD_SCHEDULE.id, Calendars.PROD_CALENDAR.id)

    def __init__(self, name, short_name, schedule_id, calendar_id):
        self.name = name
        self.short_name = short_name
        self.schedule_id = schedule_id
        self.calendar_id = calendar_id

    def __repr__(self):
        return "<Department (name='%s', schedule_id='%s', calendar_id='%s')>" \
               % (self.name, self.schedule_id, self.calendar_id)

    def __str__(self):
        return self.__repr__()

    def name(self):
        return self.name

    def short_name(self):
        return self.short_name

    def schedule_id(self):
        return self.schedule_id

    def calendar_id(self):
        return self.calendar_id
