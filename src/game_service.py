class GameService:
    @classmethod
    def get_statistics(cls, chat_id) -> (int, float):
        return 0, 0.1

    @classmethod
    def start_game(cls, chat_id):
        cls._check_if_game_exists(chat_id)

    @classmethod
    def set_word_type(cls, chat_id, word_type):
        cls._check_if_game_exists(chat_id)

    @classmethod
    def set_word_length(cls, chat_id, length):
        cls._check_if_game_exists(chat_id)

    @classmethod
    def play_round(cls, chat_id, text):
        cls._check_if_game_exists(chat_id)

    @classmethod
    def _check_if_game_exists(cls, chat_id):
        pass
