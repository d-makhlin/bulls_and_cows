import codecs
import json
import logging
import random
import re
from datetime import datetime
from typing import List, Optional

from pymongo import MongoClient
from src.datamodels import Game, GameActionResponse, GameRoundActionResponse, GameStatisticsResponse
from static.constants import GameState, GameType
from static.settings import MONGODB_NAME


class GameService:
    """
    Service that implements all gaming actions, works with database and builds response messages for user
    """

    con = MongoClient()[MONGODB_NAME]
    db = con['bulls_and_cows']
    logging.info('Connected to db')

    file = codecs.open('static/dictionary.txt', 'r+', encoding='utf-8')
    words_dict = json.load(file)

    @classmethod
    def get_statistics(cls, chat_id) -> GameStatisticsResponse:
        """
        Returns users's statistics about how many games has he/she played and
         how much average time does it take from him/her to win a single game
        :param chat_id: id of user's chat
        :return: dataclass that has information about users's statistics
        """
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
        """
        Starts the game for user when he has chosen every necessary game parameter
        :param chat_id: id of user's chat
        :return: dataclass that has information whether the game was started or not and why
        """
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
        """
        Sets the word type of the game (playing with numbers or letters)
        :param chat_id: id of user's chat
        :param text: type of game that was chosen by user
        :return: dataclass that has information whether the action was successful or not and why
        """
        response = GameActionResponse(success=True)
        if text == 'числа':
            word_type = GameType.NUMBERS
        else:
            word_type = GameType.WORDS
        exists, _ = cls.check_if_game_exists(chat_id, [GameState.INITIALIZATION])
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
        """
        Sets the length of the word that the user wants to play with
        :param chat_id: id of users' chat
        :param length: Length that was chosen by user
        :return: dataclass that has information whether the action was successful or not and why
        """
        response = GameActionResponse(success=True)
        exists, game = cls.check_if_game_exists(chat_id, [GameState.INITIALIZATION])
        if not exists:
            response.update(False, 'Не существует текущей игры!')
        else:
            answer = cls.generate_word(game.word_type, length)
            GameService.db.update_one(
                {'chat_id': str(chat_id), 'state': str(GameState.INITIALIZATION.value)},
                {'$set': {'length': length, 'state': str(GameState.IN_PROGRESS.value), 'answer': answer}},
            )
        return response

    @classmethod
    def play_round(cls, chat_id, text) -> GameRoundActionResponse:
        """
        Implements one round of play with user's guess and program's answer with results by bulls and cows
        :param chat_id: id of user's chat
        :param text: user's guess
        :return: dataclass that has information whether the action was successful or not and why
        """
        response = GameRoundActionResponse(success=True)
        exists, game = cls.check_if_game_exists(chat_id, [GameState.IN_PROGRESS])
        if not exists:
            response.success = False
            response.message = 'Не существует текущей игры!'
        else:
            response_action = cls.check_if_question_is_ok(text, game.word_type, game.length)
            if not response_action.success:
                response.message = response_action.message
                return response
            response.bulls, response.cows = cls.get_bulls_and_cows(text, game.answer)
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
        """
        Method for internal usage that checks if the user has a game in any given state in database
        :param chat_id: id of user's chat
        :param states: list of game states that have to be checked
        :return: Tuple, 1. does the game exist or not. 2. the game if it does exist
        """
        str_states = [str(state.value) for state in states]
        game = GameService.db.find_one({'chat_id': str(chat_id), 'state': {'$in': str_states}})
        if game:
            return True, Game.parse_obj(game)
        return False, None

    @classmethod
    def generate_word(cls, word_type: GameType, length: int) -> str:
        """
        Generates an answer of given length for the game
        :param length: given length
        :return: generated answer
        """
        length = int(length)
        if word_type == GameType.NUMBERS.value:
            answer = cls.generate_numbers_word(length)
        else:
            answer = cls.generate_letters_word(length)
        return answer

    @classmethod
    def generate_letters_word(cls, length: int) -> str:
        """
        Generates an answer of letters of given length for the game
        :param length: given length
        :return: generated answer
        """
        words = GameService.words_dict[str(length)]
        index = random.randint(0, len(words))
        return words[index]

    @classmethod
    def generate_numbers_word(cls, length: int) -> str:
        """
        Generates an answer of numbers of given length for the game
        :param length: given length
        :return: generated answer
        """
        answer = ''
        while len(answer) < length:
            number = random.randint(0, 9)
            if str(number) not in answer:
                answer = answer + str(number)
        return answer

    @classmethod
    def check_if_question_is_ok(cls, question: str, word_type: GameType, length: int) -> GameActionResponse:
        """
        Checks if the user's guess is relevant for the game
        :param question: user's guess
        :param word_type: type of game (letters or numbers)
        :param length: already set length of answer
        :return: dataclass that has information whether the action was successful or not and why
        """
        result = GameActionResponse(success=False)
        set_question = set(question)
        length = int(length)

        if len(question) != length:
            result.message = f'Строка должна иметь длину {length}!'
        if len(question) != len(set_question):
            result.message = 'Все символы строки должны быть разными!'
        if word_type == GameType.WORDS.value:
            if not cls.check_if_letter_question_is_ok(question):
                result.message = 'Все символы должны быть буквами кириллицы!'
        else:
            if not question.isnumeric():
                result.message = 'Все символы должны быть цифрами!'
        if not result.message:
            result.success = True
        return result

    @classmethod
    def check_if_letter_question_is_ok(cls, question: str) -> bool:
        """
        Checks if the string with letters is relevant for the game
        :param question: user's guess
        :return: True if question is relevant, False otherwise
        """
        russian = re.compile("[а-яА-Я]+")
        list_q = [
            question,
        ]
        lines = [w for w in filter(russian.match, list_q)]
        return len(lines) != 0

    @classmethod
    def get_bulls_and_cows(cls, question: str, answer: str) -> (int, int):
        """
        Returns numbers of bulls and cows based on given question and actual answer
        :param question: user's guess
        :param answer: correct answer
        :return: numbers of bulls and cows
        """
        bulls, cows = 0, 0
        for ind in range(len(question)):
            if question[ind] == answer[ind]:
                bulls += 1
            elif question[ind] in answer:
                cows += 1
        return bulls, cows
