import gettext


class Messages:

    lang = gettext.translation('messages', './static/locale', languages=['ru'])
    lang.install()

    def change_language(self, language):
        self.lang = gettext.translation('messages', './static/locale', languages=[language])
        self.lang.install()

    HELLO_MESSAGE = _('Hi, this bot is designed to play "Bulls and Cows"')
    RULES_MESSAGE = _('Bulls and cows is a logical game, during which, in several attempts, '
                      'the player must determine what the bot has planned. Variants of the game may '
                      'depend on the type of predictable sequence - it can be numbers or words. '
                      'After each attempt, the bot puts a "rating", indicating the number of guesses without'
                      ' coincidence with their positions (the number of "cows") and complete matches (the number of'
                      ' "bulls"). The guesser must analyze the attempts made and the estimates obtained. The bot only'
                      ' compares the next option with the plan and puts a mark on formal rules.')
    GAME_TYPE_MESSAGE = _('Choose the type of string to make')
    GAME_LENGTH_MESSAGE = _('Choose the length of the string to be guessed')
    GAME_START_MESSAGE = _('I made up the {} of length {}, start guessing!')

    START_GAME_MESSAGE = _('New game')
    RULES_GAME_MESSAGE = _('Rules')
    STATISTICS_MESSAGE = _('Statistics')
    USER_STATISTICS_DATA_MESSAGE = _('{} games were played, average time: {} seconds')
    NUMBER_MESSAGE = _('number')
    PLURAL_NUMBER_MESSAGE = _('Numbers')
    LETTER_MESSAGE = _('word')
    PLURAL_LETTER_MESSAGE = _('Words')
