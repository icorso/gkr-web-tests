# coding=utf-8
from enum import Enum


class ObjectTypes(Enum):
    STROI_OBJECT = ('Объект капитального строительства', 1)
    ZEM_UCHASTOK = ('Земельный участок', 2)
    DOMOVLADENIE = ('Домовладение', 3)
    ZEMLI_SH_NAZNACHENIYA = ('Земли сельхоз назначения', 4)

    def __init__(self, name, id_):
        self.name = name
        self.id = id_

    def __repr__(self):
        return "<ObjectType (name='%s', id='%s')>" \
               % (self.name, self.id)

    def __str__(self):
        return self.name

    def name(self):
        return self.name

    def id(self):
        return self.id
