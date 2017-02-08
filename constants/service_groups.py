# coding=utf-8
from enum import Enum


class ServiceGroups(Enum):
    PHYS_PERSON = (1, u'Физические лица', 0.7, 'FIZ_ALG')
    LEGAL_PERSON = (2, u'Юридические лица', 0.3, 'UR_ALG')
    QUEUE = (3, u'Порядковая очередь', 0, '')

    def __init__(self, id_, name, percent, algorithm):
        self.id = id_
        self.name = name
        self.percent = percent
        self.algorithm = algorithm

    def __str__(self):
        return self.id.__repr__() + " " + self.name.__repr__() + " " + self.percent.__repr__()

    def id(self):
        return self.id

    def name(self):
        return self.name

    def percent(self):
        return self.percent

    def algorithm(self):
        return self.algorithm
