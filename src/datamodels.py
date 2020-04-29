from typing import Optional

from pydantic import BaseModel
from datetime import datetime

from static.constants import GameType, GameState


class Game(BaseModel):
    chat_id: str
    state: GameState
    word_type: Optional[GameType] = None
    answer: Optional[str] = None
    rounds: int
    start_date: datetime
    end_date: Optional[datetime] = None


class GameBaseResponse(BaseModel):
    success: bool


class GameActionResponse(GameBaseResponse):
    message: str


class GameStatisticsResponse(GameBaseResponse):
    games_count: int
    avg_time: float
