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


class TableRow:

    __department = None
    __time = None
    __quantity = None
    __physic = None
    __juristic = None
    __internet = None
    __registrators = None
    __rnkb = None
    __genbank = None
    __selsovet = None

    @property
    def department(self):
        return self.__department

    @property
    def time(self):
        return self.__time

    @property
    def quantity(self):
        return self.__quantity

    @property
    def physic(self):
        return self.__physic

    @property
    def juristic(self):
        return self.__juristic

    @property
    def internet(self):
        return self.__internet

    @property
    def registrators(self):
        return self.__registrators

    @property
    def rnkb(self):
        return self.__rnkb

    @property
    def genbank(self):
        return self.__genbank

    @property
    def selsovet(self):
        return self.__selsovet

    @department.setter
    def department(self, value):
        self.__department = value

    @time.setter
    def time(self, value):
        self.__time = value

    @quantity.setter
    def quantity(self, value):
        self.__quantity = value

    @physic.setter
    def physic(self, value):
        self.__physic = value

    @juristic.setter
    def juristic(self, value):
        self.__juristic = value

    @internet.setter
    def internet(self, value):
        self.__internet = value

    @registrators.setter
    def registrators(self, value):
        self.__registrators = value

    @rnkb.setter
    def rnkb(self, value):
        self.__rnkb = value

    @genbank.setter
    def genbank(self, value):
        self.__genbank = value

    @selsovet.setter
    def selsovet(self, value):
        self.__selsovet = value

    def __repr__(self):
        return '<TableRow (time=%s, quantity=%s, physic=%s)>' % (self.time, self.quantity, self.physic)


class StatisticTable(BaseElement):

    @property
    def elements(self):
        return self.element.find_elements(By.XPATH, ".//tbody/tr")

    @property
    def rows(self):
        r = list()
        for i in range(1, len(self.elements) + 1):
            row = TableRow()
            if len(self.element.find_elements(By.XPATH, './/tr[' + str(i) + ']/td')) > 1:
                row.time = BaseElement(u"Время (строка #" + str(i) + ')', By.XPATH, './/tr[' + str(i) + ']/td[1]').__get__(self)
                row.quantity = BaseElement(u"Количество (строка #" + str(i) + ')', By.XPATH, './/tr[' + str(i) + ']/td[2]').__get__(self)
                row.physic = BaseElement(u"Физлица (строка #" + str(i) + ')', By.XPATH, './/tr[' + str(i) + ']/td[3]').__get__(self)
                row.juristic = BaseElement(u"Юрлица (строка #" + str(i) + ')', By.XPATH, './/tr[' + str(i) + ']/td[4]').__get__(self)
                row.internet = BaseElement(u"Интернет (строка #" + str(i) + ')', By.XPATH, './/tr[' + str(i) + ']/td[5]').__get__(self)
                row.registrators = BaseElement(u"Регистраторы (строка #" + str(i) + ')', By.XPATH, './/tr[' + str(i) + ']/td[6]').__get__(self)
                row.rnkb = BaseElement(u"РНКБ (строка #" + str(i) + ')', By.XPATH, './/tr[' + str(i) + ']/td[7]').__get__(self)
                row.genbank = BaseElement(u"Генбанк (строка #" + str(i) + ')', By.XPATH, './/tr[' + str(i) + ']/td[8]').__get__(self)
                row.selsovet = BaseElement(u"Сельсоветы (строка #" + str(i) + ')', By.XPATH, './/tr[' + str(i) + ']/td[9]').__get__(self)
            else:
                row.department = BaseElement(u"Название отделения (строка #" + str(i) + ')', By.XPATH, './/tr[' + str(i) + ']/td[1]').__get__(self)
            r.append(row)
        return r

    def get_row_by_index(self, index):
        try:
            return self.rows[index]
        except IndexError:
            raise IndexError(u'Строки с индексом ' + str(index) + ' не существует. Максимальный индекс = ' + str(len(self.rows) - 1))


