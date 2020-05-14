import codecs
import logging
import telebot
import json

from pymongo import MongoClient
from src.game_service import GameService
from static.constants import GameType, GameState
from static.messages import HELLO_MESSAGE, RULES_MESSAGE, GAME_TYPE_MESSAGE, GAME_LENGTH_MESSAGE, GAME_START_MESSAGE
from static.settings import BOT_TOKEN, MONGODB_NAME

# telebot.apihelper.proxy = {'https': 'socks5h://userproxy:password@proxy_address:port'}
bot = telebot.TeleBot(BOT_TOKEN)
telebot.apihelper.proxy = {'http': 'http://88.204.154.155:8080'}

# telebot.apihelper.proxy = {
#   'http', 'socks5://login:pass@12.11.22.33:8000',
#   'https', 'socks5://login:pass@12.11.22.33:8000'
# }


@bot.message_handler(commands=['start'])
def start_message(message):
    start_keyboard = telebot.types.ReplyKeyboardMarkup('Начать игру', 'Правила', 'Статистика')
    bot.send_message(message.chat.id, HELLO_MESSAGE, reply_markup=start_keyboard)


@bot.message_handler(content_types=['text'])
def send_text(message):
    text = message.text.lower()
    chat_id = message.chat.id

    if text == 'правила':
        play_keyboard = telebot.types.ReplyKeyboardMarkup('Начать игру')
        bot.send_message(chat_id, RULES_MESSAGE, reply_markup=play_keyboard)

    if text == 'статистика':
        play_keyboard = telebot.types.ReplyKeyboardMarkup('Начать игру')
        played, avg_time = GameService.get_statistics(chat_id)
        bot.send_message(chat_id, f'Сыграно {played} игр, среднее время: {avg_time} секунд', reply_markup=play_keyboard)

    if text == 'начать игру':
        GameService.start_game(chat_id)
        type_keyboard = telebot.types.ReplyKeyboardMarkup('Числа', 'Слова')
        bot.send_message(chat_id, GAME_TYPE_MESSAGE, reply_markup=type_keyboard)

    if text in ['числа', 'слова']:
        GameService.set_word_type(chat_id, text)
        length_keyboard = telebot.types.ReplyKeyboardMarkup('4', '5', '6')
        bot.send_message(chat_id, GAME_LENGTH_MESSAGE, reply_markup=length_keyboard)

    if text in ['4', '5', '6']:
        GameService.set_word_length(chat_id, text)
        game = GameService.check_if_game_exists(chat_id, [GameState.IN_PROGRESS])[1]
        word_type = 'слово' if game.word_type == GameType.WORDS else 'число'
        bot.send_message(chat_id, GAME_START_MESSAGE.format(word_type, game.length))

    response = GameService.play_round(chat_id, text)
    bot.send_message(chat_id, response)


db = MongoClient()[MONGODB_NAME]
logging.info('Connected to db')

file = codecs.open('../static/dictionary.txt', 'r+', encoding='utf-8')
words_dict = json.load(file)

if __name__ == '__main__':
    bot.polling()
