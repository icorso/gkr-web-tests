# coding=utf-8
from constants.object_types import ObjectTypes
from constants.services import Services

operator_timeslot_data = [
    (ObjectTypes.STROI_OBJECT.name, '1%'),
    (ObjectTypes.ZEM_UCHASTOK.name, '3%'),
    (ObjectTypes.DOMOVLADENIE.name, '5%'),
    (ObjectTypes.ZEMLI_SH_NAZNACHENIYA.name, '7%')
]

legal_timeslot_data = [
    (Services.GKN.name, '2%'),
    (Services.SINGLE_WINDOW.name, '6%'),
    (Services.DEAL_REGISTER.name, '10%')
]
