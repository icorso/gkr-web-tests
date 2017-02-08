import logging

from krtech.elements.link import Link

from elements import BaseElement, By


class AdminDepartmentsRow:

    __name = None
    __delete = None

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    def __str__(self):
        return self.name


class AdminDepartmentsTable(BaseElement):

    @property
    def elements(self):
        return self.element.find_elements(By.XPATH, ".//tbody/tr")

    @property
    def rows(self):
        r = list()
        for i in range(1, len(self.elements)):
            row = AdminDepartmentsRow()
            row.name = BaseElement(u"Название подразделения в строке #" + str(i),
                                   By.XPATH, './/tr[' + str(i) + ']/td[1]').__get__(self)
            row.delete = Link(u"Кнопка 'Delete' в строке #" + str(i),
                              By.XPATH, './/tr[' + str(i) + ']/td[2]/a').__get__(self)
            r.append(row)
        return r

    def get_row_by_name(self, name):
        a = list(filter(lambda AdminDepartmentsRow: AdminDepartmentsRow.name.text == name, self.rows))
        try:
            return a[0]
        except IndexError:
            logging.getLogger().warning(u"Не найдена строка с title='" + name + "'")
            return None

