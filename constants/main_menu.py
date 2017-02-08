# coding=utf-8
from enum import Enum


class MainMenu(Enum):
    HOME = 'ГЛАВНАЯ'
    QUEUE = 'ПОСТАНОВКА В ОЧЕРЕДЬ'
    HISTORY = 'ИСТОРИЯ'
    CONTACTS = 'ОБРАТНАЯ СВЯЗЬ'
    PHYS = 'ФИЗИЧЕСКИМ ЛИЦАМ'
    FAQ = 'ЧАСТЫЕ ВОПРОСЫ'
    JUR = 'ЮРИДИЧЕСКИМ ЛИЦАМ'

    def __init__(self, item):
        self.item = item

    def __repr__(self):
        return "<MainMenu (item='%s')>" % self.item

    def __str__(self):
        return str(self.item)

    def item(self):
        return self.item
