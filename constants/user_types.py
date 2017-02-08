# coding=utf-8
from enum import Enum


class UserTypes(Enum):
    CUSTOMER = (1, 'Физические лица', 0.3)
    LEGAL = (2, 'Юридические лица', 0.7)
    ADVANCE = (3, 'Порядковая очередь', 0)

    def __init__(self, id_, name, advance_time):
        self.id = id_
        self.name = name
        self.advance_time = advance_time

    def __repr__(self):
        return "<UserType (id='%s', name='%s', advance_time='%s')>" % (self.id, self.name, self.advance_time)

    def __str__(self):
        return self.__repr__()

    def id(self):
        return self.id

    def name(self):
        return self.name

    def advance_time(self):
        return self.advance_time
