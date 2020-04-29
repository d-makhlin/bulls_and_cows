from src.datamodels import GameStatisticsResponse, GameActionResponse, Game
from static.constants import GameType, GameState
from datetime import datetime


class GameService:
    @classmethod
    def get_statistics(cls, chat_id) -> GameStatisticsResponse:
        response = GameStatisticsResponse()
        return response

    @classmethod
    def start_game(cls, chat_id) -> GameActionResponse:
        if not cls._check_if_game_exists(chat_id):
            Game(chat_id=chat_id, state=GameState.INITIALIZATION, rounds=0, start_date=datetime.now())
        # todo: put Game to DB
        response = GameActionResponse()
        return response

    @classmethod
    def set_word_type(cls, chat_id, word_type) -> GameActionResponse:
        cls._check_if_game_exists(chat_id)
        response = GameActionResponse()
        return response

    @classmethod
    def set_word_length(cls, chat_id, length) -> GameActionResponse:
        cls._check_if_game_exists(chat_id)
        response = GameActionResponse()
        return response

    @classmethod
    def play_round(cls, chat_id, text) -> GameActionResponse:
        cls._check_if_game_exists(chat_id)
        response = GameActionResponse()
        return response

    @classmethod
    def _check_if_game_exists(cls, chat_id) -> bool:
        pass

    @classmethod
    def _check_if_question_is_ok(cls, question: str, word_type: GameType, length: int) -> GameActionResponse:
        result = GameActionResponse(success=False, message='')
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

