from typing import Optional

from pydantic import BaseModel
from datetime import datetime

from static.constants import GameType, GameState


class Game(BaseModel):
    chat_id: str
    state: GameState
    word_type: Optional[GameType] = None
    answer: Optional[str] = None
    length: Optional[int]
    rounds: int
    start_date: datetime
    end_date: Optional[datetime] = None


class GameBaseResponse(BaseModel):
    success: bool


class GameActionResponse(GameBaseResponse):
    message: Optional[str] = None

    def update(self, success: bool, message: str):
        self.success = success
        self.message = message


class GameRoundActionResponse(GameBaseResponse):
    message: Optional[str] = None
    bulls: Optional[int] = None
    cows: Optional[int] = None


class GameStatisticsResponse(GameBaseResponse):
    games_count: int
    avg_time: float
