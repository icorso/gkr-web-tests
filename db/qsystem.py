# coding=utf-8

from sqlalchemy import Column, DateTime, Integer, BigInteger, String, SmallInteger, Enum, Float, Date, Time
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Customers(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Integer, nullable=True)
    name = Column(String(30))
    no = Column(Integer)  # int(6)
    surname = Column(String(30))
    patronymic = Column(String(30))
    birthday = Column(DateTime, nullable=True)
    email = Column(String(255))
    mobile_phone = Column(String(15))
    home_phone = Column(String(14), nullable=True)
    created = Column(DateTime)
    validated = Column(DateTime, nullable=True)
    code = Column(String(32))
    serial = Column(Integer)  # int(4)
    issue = Column(String(255))
    when_at = Column(DateTime, default='0000-00-00 00:00:00')
    last_login = Column(DateTime, nullable=True)
    schedule = Column(Integer, nullable=True)
    inn = Column(String(12), nullable=True)
    blocked = Column(Integer, default=0)

    def __repr__(self):
        return "<Customers(id='%s', mobile_phone='%s', name='%s', surname='%s')>" \
               % (self.id, self.mobile_phone, self.name, self.surname)

    def __str__(self):
        return self.__repr__()


class TCustomers(Base):
    __tablename__ = 'tcustomers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    birthday = Column(DateTime, nullable=False)
    code = Column(String(32))
    created = Column(DateTime)
    name = Column(String(30))
    no = Column(Integer)  # int(6)
    surname = Column(String(30))
    patronymic = Column(String(30))
    email = Column(String(255))
    mobile_phone = Column(String(15))
    home_phone = Column(String(14), nullable=True)
    serial = Column(Integer)  # int(4)
    issue = Column(String(255))
    when_at = Column(DateTime, default='0000-00-00 00:00:00')

    def __repr__(self):
        return "<TCustomers(id='%s', mobile_phone='%s', name='%s', surname='%s')>" \
               % (self.id, self.mobile_phone, self.name, self.surname)

    def __str__(self):
        return self.__repr__()


class AclUsers(Base):
    __tablename__ = 'acl_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True)
    pwd = Column(String(30))
    enabled = Column(Integer, default=1)  # int(1)

    def __repr__(self):
        return "<AclUsers(id='%s', name='%s', pwd='%s', enabled='%s')>" % (self.id, self.name, self.pwd, self.enabled)

    def __str__(self):
        return self.__repr__()


class AclUserRoles(Base):
    __tablename__ = 'acl_user_roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    role_id = Column(Integer)

    def __repr__(self):
        return "<AclUserRoles(id='%s', user_id='%s', role_id='%s')>" % (self.id, self.user_id, self.role_id)

    def __str__(self):
        return self.__repr__()


class History(Base):
    __tablename__ = 'history'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    cid = Column(BigInteger, nullable=True)
    created = Column(DateTime, nullable=True)
    email = Column(String(255), nullable=True)
    home_phone = Column(String(14), nullable=True)
    issue = Column(String(255))
    mobile_phone = Column(String(14), nullable=False)
    name = Column(String(255), nullable=False)
    no = Column(Integer)  # int(6)
    patronymic = Column(String(255), nullable=False)
    rid = Column(BigInteger)  # bigint(20)
    serial = Column(Integer)  # int(11)
    department_id = Column(BigInteger)  # bigint(20)
    service_id = Column(BigInteger)  # bigint(20)
    surname = Column(String(255), nullable=True)
    when_at = Column(DateTime)
    inn = Column(String(12))

    def __repr__(self):
        return "<History(id='%s', mobile_phone='%s', name='%s', surname='%s')>" \
               % (self.id, self.mobile_phone, self.name, self.surname)

    def __str__(self):
        return self.__repr__()


class Advance(Base):
    __tablename__ = 'advance'

    id = Column(BigInteger, primary_key=True, autoincrement=True)  # bigint(20)
    service_id = Column(BigInteger)  # bigint(20)
    department_id = Column(BigInteger, nullable=True)  # bigint(20)
    customer_id = Column(Integer, nullable=True)  # int(11)
    advance_time = Column(DateTime)
    objects_count = Column(Integer, nullable=False, default=1)  # int(11)
    priority = Column(Integer, nullable=False, default=2)  # int(11)
    clients_authorization_id = Column(BigInteger, nullable=True)  # bigint(20)
    input_data = Column(String(500), nullable=True)
    comments = Column(String(345), nullable=True)
    update_time = Column(DateTime)
    history_id = Column(BigInteger)  # bigint(20)
    code = Column(Integer, nullable=True)  # int(11)
    deleted = Column(DateTime, nullable=True)

    def __repr__(self):
        return "<Advance(id='%s', customer_id='%s', input_data='%s')>" % (self.id, self.customer_id, self.input_data)

    def __str__(self):
        return self.__repr__()


class Department(Base):
    __tablename__ = 'department'
    id = Column(BigInteger, primary_key=True, autoincrement=True)  # bigint(20)
    name = Column(String(2000))
    sync_time = Column(DateTime)
    schedule_id = Column(BigInteger)  # bigint(20)
    calendar_id = Column(BigInteger)  # bigint(20)
    advanceLimitPeriod = Column(Integer, nullable=True)  # int(11)
    description = Column(String(255), nullable=True)
    finish_advance_date = Column(Date, nullable=True)

    def __repr__(self):
        return "<Department(id='%s', name='%s', schedule_id='%s', calendar_id='%s')>" \
               % (self.id, self.name, self.schedule_id, self.calendar_id)

    def __str__(self):
        return self.__repr__()


class DepartRegion(Base):
    __tablename__ = 'depart_region'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    region_code = Column(String(255))
    depart_id = Column(Integer)

    def __repr__(self):
        return "<Department Region(id='%s', region_code='%s', depart_id='%s')>" \
               % (self.id, self.region_code, self.depart_id)

    def __str__(self):
        return self.__repr__()


class DepartServiceGroup(Base):
    __tablename__ = 'department_service_group'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    department_id = Column(BigInteger)
    sevice_group_id = Column(BigInteger)
    percent = Column(Float)

    def __repr__(self):
        return "<Department Region(id='%s', region_code='%s', depart_id='%s')>" \
               % (self.id, self.region_code, self.depart_id)

    def __str__(self):
        return self.__repr__()


class Schedule(Base):
    __tablename__ = 'schedule'
    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)  # bigint(20)
    name = Column(String(150), nullable=False, default='')
    type = Column(Integer, nullable=False, default=0)  # int(11)
    time_begin_1 = Column(DateTime, nullable=True)
    time_end_1 = Column(DateTime, nullable=True)
    time_begin_2 = Column(DateTime, nullable=True)
    time_end_2 = Column(DateTime, nullable=True)
    time_begin_3 = Column(DateTime, nullable=True)
    time_end_3 = Column(DateTime, nullable=True)
    time_begin_4 = Column(DateTime, nullable=True)
    time_end_4 = Column(DateTime, nullable=True)
    time_begin_5 = Column(DateTime, nullable=True)
    time_end_5 = Column(DateTime, nullable=True)
    time_begin_6 = Column(DateTime, nullable=True)
    time_end_6 = Column(DateTime, nullable=True)
    time_begin_7 = Column(DateTime, nullable=True)
    time_end_7 = Column(DateTime, nullable=True)
    breaks_id1 = Column(Integer, nullable=True)
    breaks_id2 = Column(Integer, nullable=True)
    breaks_id3 = Column(Integer, nullable=True)
    breaks_id4 = Column(Integer, nullable=True)
    breaks_id5 = Column(Integer, nullable=True)
    breaks_id6 = Column(Integer, nullable=True)
    breaks_id7 = Column(Integer, nullable=True)

    def __repr__(self):
        return "<Schedule(id='%s', name='%s')>" \
               % (self.id, self.name)

    def __str__(self):
        return self.__repr__()


class Break(Base):
    __tablename__ = 'break'
    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    breaks_id = Column(BigInteger, nullable=True, default=None)
    from_time = Column(Time, nullable=False, default=0)
    to_time = Column(Time, nullable=True)
    duration = Column(BigInteger, nullable=True)

    def __repr__(self):
        return "<Break(id='%s', breaks_id='%s', from_time='%s', to_time='%s', duration='%s')>" \
               % (self.id, self.breaks_id, self.from_time, self.to_time, self.duration)

    def __str__(self):
        return self.__repr__()


class Services(Base):
    __tablename__ = 'services'
    id = Column(BigInteger, nullable=False, primary_key=True)
    name = Column(String(2000))
    description = Column(String(2000), nullable=True)
    service_prefix = Column(String(10), nullable=True)
    button_text = Column(String(2500), nullable=False, default='')
    status = Column(Integer, nullable=False, default=1)
    visible_in_web = Column(Integer, nullable=False, default=1)
    enable = Column(Integer, nullable=False, default=1)
    prent_id = Column(Integer, nullable=True)
    day_limit = Column(Integer, nullable=False, default=0)
    person_day_limit = Column(Integer, nullable=False, default=0)
    advance_limit = Column(Integer, nullable=False, default=1)
    advance_limit_period = Column(Integer, nullable=True, default=14)
    advance_time_period = Column(Integer, nullable=False, default=60)
    schedule_id = Column(BigInteger, nullable=True, default=None)
    input_required = Column(Integer, nullable=False, default=1)
    input_caption = Column(String, nullable=False, default='Введите номер документа')
    result_required = Column(Integer, nullable=False, default=0)
    calendar_id = Column(BigInteger, nullable=True, default=None)
    pre_info_html = Column(String(2500), nullable=False, default='')
    pre_info_print_text = Column(String(2500), nullable=False, default='')
    point = Column(Integer, nullable=False, default=0)
    ticket_text = Column(String(2500), nullable=True, default=None)
    seq_id = Column(Integer, nullable=False, default=0)
    but_x = Column(Integer, nullable=False, default=0)
    but_y = Column(Integer, nullable=False, default=0)
    but_b = Column(Integer, nullable=False, default=0)
    but_h = Column(Integer, nullable=False, default=0)
    duration = Column(Integer, nullable=False, default=1)
    aditional_duration = Column(Integer, nullable=False, default=0)
    precent_records = Column(Float, nullable=False, default=1)
    precent_records_advance = Column(Float, nullable=False, default=1)
    group_id = Column(BigInteger, nullable=True, default=None)
    exterritorial = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return "<Services(id='%s', name='%s', group_id='%s')>" % (self.id, self.name, self.group_id)

    def __str__(self):
        return self.__repr__()


class ServicesUsers(Base):
    __tablename__ = 'services_users'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    service_id = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    coefficient = Column(Integer, nullable=False, default=1)
    flexible_coef = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return "<ServicesUsers(id='%s', service_id='%s', user_id='%s')>" % (self.id, self.service_id, self.user_id)

    def __str__(self):
        return self.__repr__()


class Clients(Base):
    __tablename__ = 'clients'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    service_id = Column(BigInteger, autoincrement=True)
    user_id = Column(BigInteger, nullable=True)
    service_prefix = Column(String, nullable=False)
    number = Column(Integer, nullable=False)
    stand_time = Column(DateTime, nullable=False)
    call_time = Column(DateTime, nullable=True, default=None)
    start_time = Column(DateTime, nullable=True, default=None)
    finish_time = Column(DateTime, nullable=True, default=None)
    clients_authorization_id = Column(BigInteger, nullable=True, default=None)
    result_id = Column(BigInteger, nullable=True, default=None)
    input_data = Column(String, nullable=True, default=None)
    state_in = Column(Integer, nullable=False, default=0)
    advance_id = Column(BigInteger, nullable=True, default=None)


class Users(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(150))
    password = Column(String(45))
    point = Column(String(45))
    adress_rs = Column(SmallInteger, default=0)
    department_id = Column(BigInteger, nullable=True)
    enable = Column(Integer, default=1)
    admin_access = Column(SmallInteger, default=0)
    report_access = Column(SmallInteger, default=0)
    point_ext = Column(String(1045), default='')
    deleted = Column(DateTime, nullable=True)


class News(Base):
    __tablename__ = 'news'
    news_id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(256), nullable=True, default=None)
    description = Column(String(512), nullable=True, default=None)
    text = Column(String, nullable=True, default=None)
    publish_date = Column(DateTime, nullable=True)
    type_of_news = Column(Enum('NEWS', 'PHOTOS'))
    visible = Column(Integer, nullable=False)
    view_counter = Column(BigInteger, nullable=False, default=0)

    def __repr__(self):
        return "<News(news_id='%s', title='%s', description='%s')>" % (self.news_id, self.title, self.description)

    def __str__(self):
        return self.__repr__()


class NewsImages(Base):
    __tablename__ = 'news_images'
    news_id = Column(BigInteger, primary_key=True)
    images_id = Column(BigInteger, primary_key=True)


class Standards(Base):
    __tablename__ = 'standards'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    wait_max_advance = Column(Integer, nullable=False, default=20)
    next_opening_date = Column(DateTime, nullable=True)

    def __repr__(self):
        return "<Standards(id='%s', next_opening_date='%s')>" % (self.id, self.next_opening_date)

    def __str__(self):
        return self.__repr__()

