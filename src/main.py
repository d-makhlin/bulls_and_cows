import telebot

from src.messages import HELLO_MESSAGE, RULES_MESSAGE

BOT_TOKEN = ''
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    start_keyborad = telebot.types.ReplyKeyboardMarkup('Начать игру', 'Правила')
    bot.send_message(message.chat.id, HELLO_MESSAGE, reply_markup=start_keyborad)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'правила':
        bot.send_message(message.chat.id, RULES_MESSAGE)


bot.polling()
