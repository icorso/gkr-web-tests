import logging

from elements import BaseElement, By


class AdminServicesRow:

    __id = None
    __title = None
    __group = None
    __edit = None
    __delete = None

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        self.__title = value

    @property
    def group(self):
        return self.__group

    @group.setter
    def group(self, value):
        self.__group = value

    @property
    def edit(self):
        return self.__edit

    @edit.setter
    def edit(self, value):
        self.__edit = value

    def __str__(self):
        return self.id + " " + self.title + " " + self.group


class AdminServicesTable(BaseElement):

    @property
    def elements(self):
        return self.element.find_elements(By.XPATH, "//tbody/tr")

    @property
    def rows(self):
        r = list()
        for i in range(1, len(self.element.find_elements(By.XPATH, "//tbody/tr"))):
            row = AdminServicesRow()
            row.id = BaseElement(u"ID услуги в строке #" + str(i),
                                 By.XPATH, './/tr[' + str(i) + ']/td[1]').__get__(self)
            row.title = BaseElement(u"Название услуги в строке #" + str(i),
                                    By.XPATH, './/tr[' + str(i) + ']/td[2]').__get__(self)
            row.group = BaseElement(u"Группа услуги в строке #" + str(i),
                                    By.XPATH, './/tr[' + str(i) + ']/td[3]').__get__(self)
            row.edit = BaseElement(u"Кнопка 'Edit' в строке #" + str(i),
                                   By.XPATH, './/tr[' + str(i) + ']//button[1]').__get__(self)
            row.delete = BaseElement(u"Кнопка 'Delete' в строке #" + str(i),
                                     By.XPATH, './/tr[' + str(i) + ']//button[2]').__get__(self)
            r.append(row)
        return r

    def get_row_by_title(self, title):
        a = list(filter(lambda AdminServicesRow: AdminServicesRow.title.text == title, self.rows))
        try:
            return a[0]
        except IndexError:
            logging.getLogger().warning(u"Не найдена строка с title='" + title + "'")
            return None

