import logging

from elements import BaseElement, By


class AdminScheduleRow:
    __name = None
    __time_from = None
    __time_to = None
    __break_from = None
    __break_to = None
    __duration = None

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def time_from(self):
        return self.__time_from

    @time_from.setter
    def time_from(self, value):
        self.__time_from = value

    @property
    def time_to(self):
        return self.__time_to

    @time_to.setter
    def time_to(self, value):
        self.__time_to = value

    @property
    def break_from(self):
        return self.__break_from

    @break_from.setter
    def break_from(self, value):
        self.__break_from = value

    @property
    def break_to(self):
        return self.__break_to

    @break_to.setter
    def break_to(self, value):
        self.__break_to = value

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, value):
        self.__duration = value

    def __str__(self):
        return self.name


class AdminScheduleTable(BaseElement):
    @property
    def elements(self):
        return self.element.find_elements(By.XPATH, ".//tr")

    @property
    def rows(self):
        r = list()
        for i in range(2, len(self.elements)):
            row = AdminScheduleRow()
            row.name = BaseElement(u"Название дня недели #" + str(i),
                                   By.XPATH, ".//tr[" + str(i) + "]/td[1]").__get__(self)
            row.time_from = BaseElement(u"Время работы 'c'", By.XPATH,
                                        ".//tr[" + str(i) + "]//input[contains(@ng-model,'timeBegin')]").__get__(self)
            row.time_to = BaseElement(u"Время работы 'по'", By.XPATH,
                                      ".//tr[" + str(i) + "]//input[contains(@ng-model,'timeEnd')]").__get__(self)
            row.break_from = BaseElement(u"Период доступный для перерыва 'с'", By.XPATH,
                                         ".//tr[" + str(i) + "]//input[contains(@ng-model,'fromTime')]").__get__(self)
            row.break_to = BaseElement(u"Период доступный для перерыва 'по'", By.XPATH,
                                       ".//tr[" + str(i) + "]//input[contains(@ng-model,'toTime')]").__get__(self)
            row.duration = BaseElement(u"Длительность перерыва", By.XPATH,
                                       ".//tr[" + str(i) + "]//input[contains(@ng-model,'duration')]").__get__(self)
            r.append(row)
        return r

    def get_row_by_name(self, name):
        a = list(filter(lambda AdminScheduleRow: AdminScheduleRow.name.text == name, self.rows))
        try:
            return a[0]
        except IndexError:
            logging.getLogger().warning(u"Не найдена строка '" + name + "'")
            return None
