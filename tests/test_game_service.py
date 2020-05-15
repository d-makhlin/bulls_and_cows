import pytest

from src.game_service import GameService
from static.constants import GameType


@pytest.mark.parametrize(
    'length', [4, 5, 6],
)
def test_generate_numbers_word(length):
    question = GameService.generate_numbers_word(length)
    assert GameService.check_if_question_is_ok(question, GameType.NUMBERS.value, length)


@pytest.mark.parametrize(
    'length', [4, 5, 6],
)
def test_generate_letters_word(length):
    question = GameService.generate_numbers_word(length)
    assert GameService.check_if_question_is_ok(question, GameType.WORDS.value, length)


@pytest.mark.parametrize(
    'question, length, success', [('1234', 4, True), ('1234', 5, False), ('абвг', 4, False), ('абвг', 5, False),],
)
def test_if_numeric_question_is_ok(question, length, success):
    response = GameService.check_if_question_is_ok(question, GameType.NUMBERS.value, length)
    assert response.success == success


@pytest.mark.parametrize('question, success', [('1234', False), ('абвг', True), ('abcd', False),])
def test_if_letter_question_is_ok(question, success):
    assert success == GameService.check_if_letter_question_is_ok(question)


@pytest.mark.parametrize('question, answer, cows, bulls', [(1234, 1234, 0, 4), (1234, 2356, 2, 0), (1234, 5687, 0, 0)])
def test_get_bulls_and_cows(question, answer, cows, bulls):
    result = GameService.get_bulls_and_cows(str(question), str(answer))
    assert result[0] == bulls
    assert result[1] == cows
