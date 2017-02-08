# coding=utf-8
from enum import Enum


class Services(Enum):
    GKN = ('Постановка на государственный кадастровый учет (внесение сведений в ГКН)', '1438757336230', 15, 0.3)
    SINGLE_WINDOW = ('Кадастровый учет и регистрация прав в режиме единого окна', '1438757345406', 25, 0.4)
    DEAL_REGISTER = ('Регистрация прав, сделок (переход права)', '1441100935734', 25, 0.3)

    def __init__(self, name, id_, duration, percent):
        self.duration = duration
        self.percent = percent
        self.name = name
        self.id = id_

    def __str__(self):
        return self.name.__repr__()

    def name(self):
        return self.name

    def id(self):
        return self.id

    def duration(self):
        return self.duration

    def percent(self):
        return self.percent
