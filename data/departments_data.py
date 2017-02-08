from datetime import datetime, timedelta

from krtech.utils import randrus_str

from db.qsystem import Department


def rand_department():
        return Department(
            name=randrus_str(10),
            description=randrus_str(20),
            calendar_id=5,
            schedule_id=5,
            advanceLimitPeriod=10,
            sync_time=datetime.now().strftime('%Y-%m-%d') + ' 00:00:00',
            finish_advance_date=(datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d') + ' 00:00:00'
        )
