""" test_utils.py """

# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

from typing import List

import pytest

from src.sample.utils import get_random_word, get_word, get_all_words

def test_get_random_word() -> None:
    """
    Test the get_random_word function,
    a random word from the dictionary.
    """

    word_one: str = get_random_word()
    word_two: str = get_random_word()

    assert word_one != word_two

def test_get_word():
    """
    Test the get_word function,
    provides a random word with lenght
    between 5 and 7
    """

    word: str = get_word()

    assert 5 < len(word) < 8

def test_get_all_words():
    """
    Test the get_all_words function,
    that provides all_words in dictionary
    """

    all_words: List[str] = get_all_words()
    var_types: bool = all((isinstance(word, str) for word in all_words))

    assert var_types and len(all_words) == 10000
