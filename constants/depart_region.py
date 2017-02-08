from enum import Enum


class DepartRegion(Enum):
    ALUSHTA = ('91000011', 'г Алушта')
    ARMYANSK = ('91000002', 'г Армянск')
    BELOGORSKI = ('91002000', 'р-н Белогорский')
    PERVOMAYSKI = ('91009000', 'р-н Первомайский')

    def __init__(self, id_, location):
        self.id = id_
        self.location = location

    def __str__(self):
        return self.id + " " + self.location

    def id(self):
        return self.id

    def location(self):
        return self.location
