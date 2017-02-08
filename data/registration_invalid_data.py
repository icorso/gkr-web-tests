# coding=utf-8
from constants.messages import ErrorMessages

password = [
    ('87654321', '21312312', ErrorMessages.PASSWORD_MISMATCH),
    ('123', '123', ErrorMessages.PASSWORD_LENGTH)
]

fio = [
    '  '
]

email = [
    (' ', ErrorMessages.EMAIL_MALFORMED),
    ('a', ErrorMessages.EMAIL_MALFORMED),
    ('a@a.', ErrorMessages.EMAIL_MALFORMED),
    ('@', ErrorMessages.EMAIL_MALFORMED),
    (' @ ', ErrorMessages.EMAIL_MALFORMED),
    ('.@.', ErrorMessages.EMAIL_MALFORMED),
    ('addr@domain,com', ErrorMessages.EMAIL_MALFORMED),
    ('<script>alert(\'addr@domain.com\')</script>', ErrorMessages.EMAIL_MALFORMED)
]

mobile = [
    ' ',
    ' 1234567 ',
    '1234567',
    '+123',
    'телефон123',
    '+0(0)',
]

passport = [
    '1',
    '23',
    '   '
]

issue = [
    ('   ', ErrorMessages.ISSUE_EMPTY)
]

birthday = [
    ('', ErrorMessages.ISSUE_EMPTY),
    ('абвгдабвгдабвг', ErrorMessages.ISSUE_LENGTH)
]

inn = [
    ('  ', ErrorMessages.INN),
    ('абвгдабвгд', ErrorMessages.INN),
    ('1231231231231', ErrorMessages.INN),
    ('123123123', ErrorMessages.INN)
]
