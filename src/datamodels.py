from pydantic import BaseModel


class GameBaseResponse(BaseModel):
    success: bool


class GameActionResponse(GameBaseResponse):
    message: str


class GameStatisticsResponse(GameBaseResponse):
    games_count: int
    avg_time: float
