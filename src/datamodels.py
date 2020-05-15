from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Game(BaseModel):
    """
    Dataclass that collects all necessary information about a game
    """
    chat_id: str
    state: str
    word_type: Optional[str] = None
    answer: Optional[str] = None
    length: Optional[int]
    rounds: int
    start_date: datetime
    end_date: Optional[datetime] = None


class GameBaseResponse(BaseModel):
    """
    Dataclass with base response for all possible actions in the game
    """
    success: bool


class GameActionResponse(GameBaseResponse):
    """
    Dataclass that collects information whether an action went successful and what message has to be sent to user
    """
    message: Optional[str] = None

    def update(self, success: bool, message: str):
        """
        Updates GameActionResponse object with it's message and success fields
        :param success: was the action succeed
        :param message: message text that has to be sent to user
        :return:
        """
        self.success = success
        self.message = message


class GameRoundActionResponse(GameBaseResponse):
    """
    Dataclass that collects information about user result depending on his/her guess and actual correct answer
    """
    message: Optional[str] = None
    bulls: Optional[int] = None
    cows: Optional[int] = None


class GameStatisticsResponse(GameBaseResponse):
    """
    Dataclass that collects plain user's statistics
    """
    games_count: int
    avg_time: float
