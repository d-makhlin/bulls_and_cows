import re
import codecs
import logging
import json

from pymongo import MongoClient
from typing import Optional, List
import random
from src.datamodels import GameStatisticsResponse, GameActionResponse, Game, GameRoundActionResponse
from static.constants import GameType, GameState
from datetime import datetime

from static.settings import MONGODB_NAME


class GameService:

    con = MongoClient()[MONGODB_NAME]
    db = con['bulls_and_cows']
    logging.info('Connected to db')

    file = codecs.open('static/dictionary.txt', 'r+', encoding='utf-8')
    words_dict = json.load(file)

    @classmethod
    def get_statistics(cls, chat_id) -> GameStatisticsResponse:
        games_query = GameService.db.find({'chat_id': str(chat_id), 'state': str(GameState.FINISHED.value)})
        rounds = 0
        time = 0.0
        games = [Game.parse_obj(g) for g in games_query]
        if games:
            rounds = len(games)
            for game in games:
                diff = game.end_date - game.start_date
                time += diff.seconds
            time = time / rounds
        response = GameStatisticsResponse(success=True, games_count=rounds, avg_time=time)
        return response

    @classmethod
    def start_game(cls, chat_id) -> GameActionResponse:
        response = GameActionResponse(success=True)
        if not cls.check_if_game_exists(chat_id, [GameState.IN_PROGRESS, GameState.INITIALIZATION])[0]:
            game = Game(chat_id=chat_id, state=str(GameState.INITIALIZATION.value), rounds=0, start_date=datetime.now())
            GameService.db.insert_one(game.dict())
        else:
            GameService.db.update_one(
                {'chat_id': str(chat_id), 'state': str(GameState.IN_PROGRESS.value)},
                {'$set': {'state': str(GameState.IN_PROGRESS.value), 'end_date': datetime.now()}},
            )
            game = Game(chat_id=chat_id, state=str(GameState.INITIALIZATION.value), rounds=0, start_date=datetime.now())
            GameService.db.insert_one(game.dict())
        return response

    @classmethod
    def set_word_type(cls, chat_id, text) -> GameActionResponse:
        response = GameActionResponse(success=True)
        if text == 'числа':
            word_type = GameType.NUMBERS
        else:
            word_type = GameType.WORDS
        exists, game = cls.check_if_game_exists(chat_id, [GameState.INITIALIZATION])
        if not exists:
            response.success = False
            response.message = 'Не существует текущей игры!'
        else:
            GameService.db.update_one(
                {'chat_id': str(chat_id), 'state': str(GameState.INITIALIZATION.value)},
                {'$set': {'word_type': str(word_type.value)}},
            )
        return response

    @classmethod
    def set_word_length(cls, chat_id, length) -> GameActionResponse:
        response = GameActionResponse(success=True)
        exists, game = cls.check_if_game_exists(chat_id, [GameState.INITIALIZATION])
        if not exists:
            response.update(False, 'Не существует текущей игры!')
        else:
            answer = cls._generate_word(game.word_type, length)
            GameService.db.update_one(
                {'chat_id': str(chat_id), 'state': str(GameState.INITIALIZATION.value)},
                {'$set': {'length': length, 'state': str(GameState.IN_PROGRESS.value), 'answer': answer}},
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
            response_action = cls._check_if_question_is_ok(text, game.word_type, game.length)
            if not response_action.success:
                response.message = response_action.message
                return response
            response.bulls, response.cows = cls._get_bulls_and_cows(text, game.answer)
            if response.bulls == game.length:
                response.message = f'Поздравляю, ты выиграл! Я загадывал {game.answer}'
                GameService.db.update_one(
                    {'chat_id': str(chat_id), 'state': str(GameState.IN_PROGRESS.value)},
                    {
                        '$set': {
                            'rounds': game.rounds + 1,
                            'end_date': datetime.now(),
                            'state': str(GameState.FINISHED.value),
                        }
                    },
                )
            else:
                response.message = f'{response.bulls} быков, {response.cows} коров'
                GameService.db.update_one(
                    {'chat_id': str(chat_id), 'state': str(GameState.IN_PROGRESS.value)},
                    {'$set': {'rounds': game.rounds + 1}},
                )
        return response

    @classmethod
    def check_if_game_exists(cls, chat_id, states: List[GameState]) -> (bool, Optional[Game]):
        str_states = [str(state.value) for state in states]
        game = GameService.db.find_one({'chat_id': str(chat_id), 'state': {'$in': str_states}})
        if game:
            return True, Game.parse_obj(game)
        return False, None

    @classmethod
    def _generate_word(cls, word_type: GameType, length: int) -> str:
        answer = ''
        length = int(length)
        if word_type == GameType.NUMBERS.value:
            while len(answer) < length:
                n = random.randint(0, 9)
                if str(n) not in answer:
                    answer = answer + str(n)
        else:
            words = GameService.words_dict[str(length)]
            index = random.randint(0, len(words))
            answer = words[index]
        return answer

    @classmethod
    def _check_if_question_is_ok(cls, question: str, word_type: GameType, length: int) -> GameActionResponse:
        result = GameActionResponse(success=False)
        set_question = set(question)
        length = int(length)

        if len(question) != length:
            result.message = f'Строка должна иметь длину {length}!'
        if len(question) != len(set_question):
            result.message = f'Все символы строки должны быть разными!'
        if word_type == GameType.WORDS.value:
            r = re.compile("[а-яА-Я]+")
            list_q = [
                question,
            ]
            lines = [w for w in filter(r.match, list_q)]
            if len(lines) == 0:
                result.message = f'Все символы должны быть буквами кириллицы!'
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
