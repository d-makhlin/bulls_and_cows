import gettext
import os

lang = gettext.translation('messages', './locale', languages=['ru'])
lang.install()

HELLO_MESSAGE = 'Привет, этот бот предназначен для игры в "Быки и Коровы"'
RULES_MESSAGE = 'Быки и коровы — логическая игра, в ходе которой за несколько попыток игрок должен определить,' \
                ' что задумал бот. Варианты игры могут зависеть от типа отгадываемой последовательности — это ' \
                'могут быть числа или слова. После каждой попытки бот выставляет "оценку", указывая количество ' \
                'угаданного без совпадения с их позициями (количество "коров") и полных совпадений (количество' \
                ' "быков"). Угадывающий должен анализировать сделанные попытки и полученные оценки. ' \
                'Бот лишь сравнивает очередной вариант с задуманным и выставляет оценку по формальным правилам.'
GAME_TYPE_MESSAGE = 'Выбери тип строки для загадывания'
GAME_LENGTH_MESSAGE = 'Выбери длину загадываемой строки'
GAME_START_MESSAGE = 'Я загадал {} длины {}, отгадывай!'

# Messages to be translated
START_GAME_MESSAGE = _('New game')
RULES_GAME_MESSAGE = _('Правила')
STATISTICS_MESSAGE = _('Статистика')
USER_STATISTICS_DATA_MESSAGE = _('Сыграно {} игр, среднее время: {} секунд')
NUMBER_MESSAGE = _('число')
PLURAL_NUMBER_MESSAGE = _('Числа')
LETTER_MESSAGE = _('слово')
PLURAL_LETTER_MESSAGE = _('Слова')

os.environ['LANGUAGE'] = 'en'
print(START_GAME_MESSAGE)
