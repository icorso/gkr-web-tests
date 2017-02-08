# coding=utf-8


class User:
    def __init__(self, customers_data, password, role):
        self._customers_data = customers_data
        self._password = password
        self._role = role

    def __str__(self):
        return '%s %s %s' % (self._customers_data.mobile_phone, self._customers_data.name, self._customers_data.surname)

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        self._role = value

    @property
    def login(self):
        return self._customers_data.mobile_phone

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def customers_data(self):
        return self._customers_data

    @customers_data.setter
    def customers_data(self, value):
        self._customers_data = value
