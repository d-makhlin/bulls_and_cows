from typing import Optional

from src.datamodels import GameStatisticsResponse, GameActionResponse, Game, GameRoundActionResponse
from static.constants import GameType, GameState
from datetime import datetime


class GameService:
    @classmethod
    def get_statistics(cls, chat_id) -> GameStatisticsResponse:
        response = GameStatisticsResponse()
        return response

    @classmethod
    def start_game(cls, chat_id) -> GameActionResponse:
        response = GameActionResponse(success=True)
        if not cls._check_if_game_exists(chat_id)[0]:
            Game(chat_id=chat_id, state=GameState.INITIALIZATION, rounds=0, start_date=datetime.now())
            # todo: put Game to DB
        else:
            response.success = False
            response.message = 'Существует незаконченная игра!'
        return response

    @classmethod
    def set_word_type(cls, chat_id, word_type) -> GameActionResponse:
        response = GameActionResponse(success=True)
        exists, game = cls._check_if_game_exists(chat_id)
        if not exists:
            response.success = False
            response.message = 'Не существует текущей игры!'
        else:
            # todo: update Game in DB
            pass
        return response

    @classmethod
    def set_word_length(cls, chat_id, length) -> GameActionResponse:
        response = GameActionResponse(success=True)
        exists, game = cls._check_if_game_exists(chat_id)
        if not exists:
            response.success = False
            response.message = 'Не существует текущей игры!'
        else:
            # todo: update Game in DB
            pass
        return response

    @classmethod
    def play_round(cls, chat_id, text) -> GameRoundActionResponse:
        response = GameRoundActionResponse(success=True)
        exists, game = cls._check_if_game_exists(chat_id)
        if not exists:
            response.success = False
            response.message = 'Не существует текущей игры!'
        else:
            # todo: update Game in DB
            # cls._check_if_question_is_ok(text, )
            # cls._get_bulls_and_cows()
            pass
        return response

    @classmethod
    def _check_if_game_exists(cls, chat_id) -> (bool, Optional[Game]):
        return False, None

    @classmethod
    def _check_if_question_is_ok(cls, question: str, word_type: GameType, length: int) -> GameActionResponse:
        result = GameActionResponse(success=False)
        set_question = set(question)

        if len(question) != length:
            result.message = f'Строка должна иметь длину {length}!'
        if len(question) != len(set_question):
            result.message = f'Все символы строки должны быть разными!'
        if word_type == GameType.WORDS:
            if not question.isalpha():
                result.message = f'Все символы должны быть буквами!'
        else:
            if not question.isnumeric():
                result.message = f'Все символы должны быть цифрами!'
        if not result.message:
            result.success = True
        return result

    @classmethod
    def _get_bulls_and_cows(cls, question: str, answer: str) -> (int, int):
        bulls, cows = 0, 0
        for ind in range(len(question)):
            if question[ind] == answer[ind]:
                bulls += 1
            elif question[ind] in answer:
                cows += 1
        return bulls, cows

