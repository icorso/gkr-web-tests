# coding=utf-8
from enum import Enum


class UserRoles(Enum):
    CUSTOMER = (1, 'ROLE_CUSTOMER')
    OPERATOR = (4, 'ROLE_REGISTRATOR')
    ADMIN = (10, 'ROLE_ADMINISTRATOR')

    def __init__(self, id_, name):
        self.id = id_
        self.name = name

    def __repr__(self):
        return "<UserRole (id='%s', name='%s')>" % (self.id, self.name)

    def __str__(self):
        return self.__repr__()

    def id(self):
        return self.id

    def name(self):
        return self.name
