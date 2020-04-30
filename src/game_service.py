from typing import Optional, List
import random
from src.datamodels import GameStatisticsResponse, GameActionResponse, Game, GameRoundActionResponse
from static.constants import GameType, GameState
from datetime import datetime


class GameService:
    @classmethod
    def get_statistics(cls, chat_id) -> GameStatisticsResponse:
        from src.main import db
        games = db.find({'chat_id': chat_id, 'state': GameState.FINISHED})
        rounds = 0
        time = 0.0
        if games:
            rounds = len(games)
            for game in games:
                diff = game.end_date - game.start_date
                time += diff.seconds
            time = time / rounds
        response = GameStatisticsResponse(success=True, game_rounds=rounds, avg_time=time)
        return response

    @classmethod
    def start_game(cls, chat_id) -> GameActionResponse:
        response = GameActionResponse(success=True)
        if not cls.check_if_game_exists(chat_id, [GameState.IN_PROGRESS, GameState.INITIALIZATION])[0]:
            game = Game(chat_id=chat_id, state=GameState.INITIALIZATION, rounds=0, start_date=datetime.now())
            from src.main import db
            db.insert_one(game.dict())
        else:
            response.update(False, 'Существует незаконченная игра!')
        return response

    @classmethod
    def set_word_type(cls, chat_id, word_type) -> GameActionResponse:
        response = GameActionResponse(success=True)
        exists, game = cls.check_if_game_exists(chat_id, [GameState.INITIALIZATION])
        if not exists:
            response.success = False
            response.message = 'Не существует текущей игры!'
        else:
            from src.main import db
            db.update_one({'chat_id': chat_id, 'state': GameState.INITIALIZATION}, {'word_type': word_type})
        return response

    @classmethod
    def set_word_length(cls, chat_id, length) -> GameActionResponse:
        response = GameActionResponse(success=True)
        exists, game = cls.check_if_game_exists(chat_id, [GameState.INITIALIZATION])
        if not exists:
            response.update(False, 'Не существует текущей игры!')
        else:
            answer = cls._generate_word(game.word_type, game.length)
            from src.main import db
            db.update_one(
                {'chat_id': chat_id, 'state': GameState.INITIALIZATION},
                {'length': length, 'state': GameState.IN_PROGRESS, 'answer': answer},
            )
        return response

    @classmethod
    def play_round(cls, chat_id, text) -> GameRoundActionResponse:
        response = GameRoundActionResponse(success=True)
        exists, game = cls.check_if_game_exists(chat_id, [GameState.IN_PROGRESS])
        if not exists:
            response.success = False
            response.message = 'Не существует текущей игры!'
        else:
            cls._check_if_question_is_ok(text, game.word_type, game.length)
            response.bulls, response.cows = cls._get_bulls_and_cows(text, game.answer)
            if response.bulls == game.length:
                response.message = f'Поздравляю, ты выиграл!, я загадывал {game.answer}'
                from src.main import db
                db.update_one(
                    {'chat_id': chat_id, 'state': GameState.IN_PROGRESS},
                    {'rounds': game.rounds + 1, 'end_time': datetime.now(), 'state': GameState.FINISHED},
                )
            else:
                response.message = f'{response.bulls} быков, {response.cows} коров'
                from src.main import db
                db.update_one({'chat_id': chat_id, 'state': GameState.IN_PROGRESS}, {'rounds': game.rounds + 1})
        return response

    @classmethod
    def check_if_game_exists(cls, chat_id, states: List[GameState]) -> (bool, Optional[Game]):
        state = states[0]  # todo: make loop
        from src.main import db
        games = db.find({'chat_id': chat_id, 'state': state})
        if games:
            return True, Game.parse_obj(games[0])
        return False, None

    @classmethod
    def _generate_word(cls, word_type: GameType, length: int) -> str:
        answer = ''
        while len(answer) < length:
            if word_type == GameType.WORDS:
                raise NotImplementedError  # todo: connect to dictionary
            else:
                n = random.randint(0, 9)
                if str(n) not in answer:
                    answer = answer + str(n)
        return answer

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
