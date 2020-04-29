import telebot

from src.messages import HELLO_MESSAGE

BOT_TOKEN = '1126940255:AAGXar8Z0FYnzWRGNrjHsRY50vJbx08OA-c'
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, HELLO_MESSAGE)


bot.polling()
