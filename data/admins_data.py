from datetime import datetime
from random import randrange

from MySQLdb.constants.FIELD_TYPE import NULL
from krtech.utils import randrus_str, rand_num

from constants.user_types import UserTypes
from db.qsystem import News, Services, Schedule, Break


def random_news():
    return News(
        title=randrus_str(10),
        description=randrus_str(10),
        text=randrus_str(10),
        publish_date=datetime.now(),
        type_of_news='NEWS',
        visible=1
    )


def random_service():
    return Services(
        id=rand_num(10),
        name=randrus_str(10),
        group_id=UserTypes.LEGAL.id,
        calendar_id=1
    )


def random_break(id_=rand_num()):
    return Break(
        id=id_,
        from_time=str(randrange(13, 14, 1)) + ':00:00',
        to_time=str(randrange(15, 16, 1)) + ':00:00',
        duration=str(randrange(30, 60, 10))
    )


def random_schedule():
    return Schedule(
        name=randrus_str(10),
        time_begin_1=str(randrange(8, 12, 1)) + ':00:00',
        time_end_1=str(randrange(17, 19, 1)) + ':00:00',
        breaks_id1=rand_num()
    )
