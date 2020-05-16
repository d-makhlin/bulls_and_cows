import telebot
from src.game_service import GameService
from static.constants import GameType, GameState
from static.messages import Messages
from static.settings import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)

telebot.apihelper.proxy = {'http': 'http://159.89.82.38:3128', 'https': 'https://45.77.157.28:8080'}

messages = Messages()


@bot.message_handler(commands=['start'])
def start_message(message) -> None:
    """
    Returns initial bunch of buttons when users starts playing
    :param message: user telegram message object
    :return
    """
    russian_button = telebot.types.KeyboardButton('Русский')
    english_button = telebot.types.KeyboardButton('English')
    start_keyboard = telebot.types.ReplyKeyboardMarkup()
    start_keyboard.add(russian_button, english_button)
    bot.send_message(message.chat.id, 'Choose your language', reply_markup=start_keyboard)


@bot.message_handler(content_types=['text'])
def send_text(message) -> None:
    """
    Processes user's message depending on it's text and handles gaming process
    :param message:
    :return: user telegram message object
    """
    text = message.text
    chat_id = message.chat.id

    if text in ['Русский', 'English']:
        if text == 'Русский':
            messages.change_language('ru')
        else:
            messages.change_language('en')
        start_button = telebot.types.KeyboardButton(messages.lang.gettext(messages.START_GAME_MESSAGE))
        rules_button = telebot.types.KeyboardButton(messages.lang.gettext(messages.RULES_GAME_MESSAGE))
        statistics_button = telebot.types.KeyboardButton(messages.lang.gettext(messages.STATISTICS_MESSAGE))
        start_keyboard = telebot.types.ReplyKeyboardMarkup()
        start_keyboard.add(start_button, rules_button, statistics_button)
        bot.send_message(message.chat.id, messages.lang.gettext(messages.HELLO_MESSAGE), reply_markup=start_keyboard)

    elif text == messages.lang.gettext(messages.RULES_GAME_MESSAGE):
        button = telebot.types.KeyboardButton(messages.lang.gettext(messages.START_GAME_MESSAGE))
        play_keyboard = telebot.types.ReplyKeyboardMarkup()
        play_keyboard.add(button)
        bot.send_message(chat_id, messages.lang.gettext(messages.RULES_MESSAGE), reply_markup=play_keyboard)

    elif text == messages.lang.gettext(messages.STATISTICS_MESSAGE):
        button = telebot.types.KeyboardButton(messages.lang.gettext(messages.START_GAME_MESSAGE))
        play_keyboard = telebot.types.ReplyKeyboardMarkup()
        play_keyboard.add(button)
        response = GameService.get_statistics(chat_id)
        bot.send_message(
            chat_id,
            messages.lang.gettext(messages.USER_STATISTICS_DATA_MESSAGE).format(
                response.games_count, response.avg_time
            ),
            reply_markup=play_keyboard,
        )

    elif text == messages.lang.gettext(messages.START_GAME_MESSAGE):
        GameService.start_game(chat_id)
        numbers_button = telebot.types.KeyboardButton(messages.lang.gettext(messages.PLURAL_NUMBER_MESSAGE))
        words_button = telebot.types.KeyboardButton(messages.lang.gettext(messages.PLURAL_LETTER_MESSAGE))
        type_keyboard = telebot.types.ReplyKeyboardMarkup()
        type_keyboard.add(numbers_button, words_button)
        bot.send_message(chat_id, messages.lang.gettext(messages.GAME_TYPE_MESSAGE), reply_markup=type_keyboard)

    elif text in [
        messages.lang.gettext(messages.PLURAL_NUMBER_MESSAGE),
        messages.lang.gettext(messages.PLURAL_LETTER_MESSAGE),
    ]:
        if text == messages.lang.gettext(messages.PLURAL_NUMBER_MESSAGE):
            game_type = 'числа'
        else:
            game_type = 'слова'
        GameService.set_word_type(chat_id, game_type)
        button_4 = telebot.types.KeyboardButton('4')
        button_5 = telebot.types.KeyboardButton('5')
        button_6 = telebot.types.KeyboardButton('6')
        length_keyboard = telebot.types.ReplyKeyboardMarkup()
        length_keyboard.add(button_4, button_5, button_6)
        bot.send_message(chat_id, messages.lang.gettext(messages.GAME_LENGTH_MESSAGE), reply_markup=length_keyboard)

    elif text in ['4', '5', '6']:
        GameService.set_word_length(chat_id, text)
        game = GameService.check_if_game_exists(chat_id, [GameState.IN_PROGRESS])[1]
        word_type = (
            messages.lang.gettext(messages.LETTER_MESSAGE)
            if game.word_type == str(GameType.WORDS.value)
            else messages.lang.gettext(messages.NUMBER_MESSAGE)
        )
        bot.send_message(chat_id, messages.lang.gettext(messages.GAME_START_MESSAGE).format(word_type, game.length))

    else:
        response = GameService.play_round(chat_id, text.lower())
        start_button = telebot.types.KeyboardButton(messages.lang.gettext(messages.START_GAME_MESSAGE))
        rules_button = telebot.types.KeyboardButton(messages.lang.gettext(messages.RULES_GAME_MESSAGE))
        statistics_button = telebot.types.KeyboardButton(messages.lang.gettext(messages.STATISTICS_MESSAGE))
        start_keyboard = telebot.types.ReplyKeyboardMarkup()
        start_keyboard.add(start_button, rules_button, statistics_button)
        bot.send_message(chat_id, text=response.message, reply_markup=start_keyboard)


if __name__ == '__main__':
    bot.polling()
