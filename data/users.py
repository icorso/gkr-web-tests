from datetime import datetime, timedelta
import uuid

from krtech.utils import randrus_str, rand_str, rand_num

from constants.user import User
from constants.user_roles import UserRoles
from db.qsystem import Customers, TCustomers


def random_user(role, is_legal=False):
    c = Customers(
        name=randrus_str(15),
        surname=randrus_str(15),
        patronymic=randrus_str(15),
        email=rand_str() + '@' + rand_str() + '.com',
        birthday=datetime.now() - timedelta(weeks=int(rand_num(4))),
        mobile_phone='9777' + rand_num(7),
        home_phone='',
        code=uuid.uuid4().hex,
        no=rand_num(6),
        serial=rand_num(4),
        issue=randrus_str(15),
        when_at=datetime.now() - timedelta(weeks=int(rand_num(3))),
        created=datetime.now().strftime('%Y-%m-%d 00:00:00'),
        validated=datetime.now().strftime('%Y-%m-%d 00:00:00')
    )
    if is_legal:
        c.inn = '1' + rand_num(10)
    user = User(c, '12345678', role)
    return user


def random_tcustomer(role=UserRoles.CUSTOMER, is_legal=False):
    c = TCustomers(
        name=randrus_str(15),
        surname=randrus_str(15),
        patronymic=randrus_str(15),
        email=rand_str() + '@' + rand_str() + '.com',
        birthday=datetime.now() - timedelta(weeks=int(rand_num(4))),
        mobile_phone='9777' + rand_num(7),
        home_phone='',
        code=uuid.uuid4().hex,
        no=rand_num(6),
        serial=rand_num(4),
        issue=randrus_str(15),
        when_at=datetime.now() - timedelta(weeks=int(rand_num(3))),
        created=datetime.now().strftime('%Y-%m-%d 00:00:00'),
    )
    if is_legal:
        c.inn = '1' + rand_num(10)
    user = User(c, '12345678', role)
    return user

OPERATOR = User(
    Customers(
        name=u'ИмяОператора',
        surname='ФамилияОператора',
        patronymic='ОтчествоОператора',
        email='ooo@ooo.oo',
        birthday=datetime.now() - timedelta(weeks=1200),
        mobile_phone='79907777777',
        home_phone='',
        code=uuid.uuid4().hex,
        no=777777,
        serial=7777,
        issue=randrus_str(15),
        when_at=datetime.now() - timedelta(weeks=600),
        created=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        validated=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ),
    '12345678',
    UserRoles.OPERATOR
)

CUSTOMER = User(
    Customers(
        name=u'ИмяКастомера',
        surname='ФамилияКастомера',
        patronymic='ОтчествоКастомера',
        birthday=datetime.now() - timedelta(weeks=1100),
        email='ccc@ccc.cc',
        mobile_phone='79902222222',
        home_phone='',
        code=uuid.uuid4().hex,
        no=222222,
        serial=2222,
        issue=randrus_str(15),
        when_at=datetime.now() - timedelta(weeks=500),
        created=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        validated=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    ),
    '12345678',
    UserRoles.CUSTOMER
)

LEGAL = User(
    Customers(
        name='ИмяЮр',
        surname='ФамилияЮр',
        patronymic='ОтчествоЮр',
        birthday=datetime.now(),
        email='uuu@uuu.uu',
        mobile_phone='79903333333',
        inn='6357826734',
        code=uuid.uuid4().hex,
        created=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        validated=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    ),
    '12345678',
    UserRoles.CUSTOMER
)

ADMIN = User(
    Customers(
        name=u'ИмяАдмин',
        surname='ФамилияАдмин',
        patronymic='ОтчествоАдмин',
        birthday=datetime.now() - timedelta(weeks=2000),
        email='aaa@aaa.aa',
        mobile_phone='79908888888',
        home_phone='',
        code=uuid.uuid4().hex,
        no=888888,
        serial=8888,
        issue=randrus_str(15),
        when_at=datetime.now() - timedelta(weeks=1500),
        created=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        validated=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    ),
    '12345678',
    UserRoles.ADMIN
)

LEGAL_REG = User(
    Customers(
        name=randrus_str(15),
        surname=randrus_str(15),
        patronymic=randrus_str(15),
        email=rand_str() + '@' + rand_str() + '.com',
        mobile_phone='9777' + rand_num(7),
        inn=rand_num(10),
    ),
    '12345678',
    UserRoles.CUSTOMER
)
