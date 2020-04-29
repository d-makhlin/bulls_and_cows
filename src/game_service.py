class GameService:
    @classmethod
    def get_statistics(cls, chat_id) -> (int, float):
        return 0, 0.1

    @classmethod
    def start_game(cls):
        cls._check_if_game_exists()

    @classmethod
    def set_word_type(cls):
        cls._check_if_game_exists()

    @classmethod
    def set_word_length(cls):
        cls._check_if_game_exists()

    @classmethod
    def _check_if_game_exists(cls):
        pass
