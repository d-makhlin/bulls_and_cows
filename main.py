import telebot

from src.game_service import GameService
from static.constants import GameType, GameState
from static.messages import HELLO_MESSAGE, RULES_MESSAGE, GAME_TYPE_MESSAGE, GAME_LENGTH_MESSAGE, GAME_START_MESSAGE
from static.settings import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)

telebot.apihelper.proxy = {'http': 'http://159.89.82.38:3128', 'https': 'https://45.77.157.28:8080'}


@bot.message_handler(commands=['start'])
def start_message(message):
    start_button = telebot.types.KeyboardButton('Новая игра')
    rules_button = telebot.types.KeyboardButton('Правила')
    statistics_button = telebot.types.KeyboardButton('Статистика')
    start_keyboard = telebot.types.ReplyKeyboardMarkup()
    start_keyboard.add(start_button, rules_button, statistics_button)
    bot.send_message(message.chat.id, HELLO_MESSAGE, reply_markup=start_keyboard)


@bot.message_handler(content_types=['text'])
def send_text(message):
    text = message.text.lower()
    chat_id = message.chat.id

    if text == 'правила':
        button = telebot.types.KeyboardButton('Новая игра')
        play_keyboard = telebot.types.ReplyKeyboardMarkup()
        play_keyboard.add(button)
        bot.send_message(chat_id, RULES_MESSAGE, reply_markup=play_keyboard)

    elif text == 'статистика':
        button = telebot.types.KeyboardButton('Новая игра')
        play_keyboard = telebot.types.ReplyKeyboardMarkup()
        play_keyboard.add(button)
        response = GameService.get_statistics(chat_id)
        bot.send_message(
            chat_id,
            f'Сыграно {response.games_count} игр, среднее время: {response.avg_time} секунд',
            reply_markup=play_keyboard,
        )

    elif text == 'новая игра':
        GameService.start_game(chat_id)
        numbers_button = telebot.types.KeyboardButton('Числа')
        words_button = telebot.types.KeyboardButton('Слова')
        type_keyboard = telebot.types.ReplyKeyboardMarkup()
        type_keyboard.add(numbers_button, words_button)
        bot.send_message(chat_id, GAME_TYPE_MESSAGE, reply_markup=type_keyboard)

    elif text in ['числа', 'слова']:
        GameService.set_word_type(chat_id, text)
        button_4 = telebot.types.KeyboardButton('4')
        button_5 = telebot.types.KeyboardButton('5')
        button_6 = telebot.types.KeyboardButton('6')
        length_keyboard = telebot.types.ReplyKeyboardMarkup()
        length_keyboard.add(button_4, button_5, button_6)
        bot.send_message(chat_id, GAME_LENGTH_MESSAGE, reply_markup=length_keyboard)

    elif text in ['4', '5', '6']:
        GameService.set_word_length(chat_id, text)
        game = GameService.check_if_game_exists(chat_id, [GameState.IN_PROGRESS])[1]
        word_type = 'слово' if game.word_type == str(GameType.WORDS) else 'число'
        bot.send_message(chat_id, GAME_START_MESSAGE.format(word_type, game.length))

    else:
        response = GameService.play_round(chat_id, text)
        start_button = telebot.types.KeyboardButton('Новая игра')
        rules_button = telebot.types.KeyboardButton('Правила')
        statistics_button = telebot.types.KeyboardButton('Статистика')
        start_keyboard = telebot.types.ReplyKeyboardMarkup()
        start_keyboard.add(start_button, rules_button, statistics_button)
        bot.send_message(chat_id, text=response.message, reply_markup=start_keyboard)


if __name__ == '__main__':
    bot.polling()
