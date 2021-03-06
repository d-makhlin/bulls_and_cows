from enum import Enum, unique


@unique
class GameState(Enum):
    INITIALIZATION = 'INITIALIZATION'
    IN_PROGRESS = 'IN_PROGRESS'
    FINISHED = 'FINISHED'


@unique
class GameType(Enum):
    WORDS = 'WORDS'
    NUMBERS = 'NUMBERS'
