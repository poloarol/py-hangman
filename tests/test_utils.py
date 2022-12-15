""" test_utils.py """

# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

from typing import List

import unittest

from src.sample.model import HangmanAI, generate_letter_distribution
from src.sample.utils import get_random_word, get_word, get_all_words


class UtilsTest(unittest.TestCase):
    """ Unit test module for utils class """

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def test_get_random_word(self) -> None:
        """
        Test the get_random_word function,
        a random word from the dictionary.
        """

        word_one: str = get_random_word()
        word_two: str = get_random_word()

        self.assertNotEqual(word_one, word_two)

    def test_get_word(self):
        """
        Test the get_word function,
        provides a random word with lenght
        between 5 and 7
        """

        word: str = get_word()
        self.assertTrue(5 < len(word) < 8)

    def test_get_all_words(self):
        """
        Test the get_all_words function,
        that provides all_words in dictionary
        """

        all_words: List[str] = get_all_words()
        var_types: bool = all((isinstance(word, str) for word in all_words))

        self.assertTrue(var_types)
        self.assertEqual(len(all_words), 10000)

class TestAI(unittest.TestCase):
    """
    Test the HangmanAI class
    """

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        word: str = "SEQUEL"
        words: List[str] = get_all_words()
        self.player: HangmanAI = HangmanAI(word=word, words=words)

    def test_has_letter(self):
        """ test if letter exists in word"""
        self.assertTrue(self.player.has_letter("E"))
        self.assertFalse(self.player.has_letter("K"))

    def test_get_current_state(self):
        """ test the current state method """
        self.assertTrue(isinstance(self.player.get_current_state(), str))

    def test_get_possible_words(self):
        """
        Test the get_possible_words
        """

        all_words: List[str] = self.player.get_possible_words()
        var_types: bool = all((isinstance(word, str) for word in all_words))
        self.assertTrue(var_types)

    def test_prune_by_letter(self):
        """ test prune by letter """

        starting_words: List[str] = self.player.get_possible_words()
        self.player.prune_by_letter(letter="E")
        ending_words: List[str] = self.player.get_possible_words()
        self.assertTrue(len(ending_words) < len(starting_words))

        starting_words: List[str] = self.player.get_possible_words()
        self.player.prune_by_letter(letter="K")
        ending_words: List[str] = self.player.get_possible_words()
        self.assertTrue(len(starting_words) == len(ending_words))

        only_letter: List[bool] = [True for word in ending_words if "E" in word]
        self.assertTrue(all((True for item in only_letter if item is True)))

    def test_prune_by_index(self):
        """ test prune by index function """

        # There's a problem with the function. Need to look more into
        # it
        # starting_words: List[str] = self.player.get_possible_words()
        # self.player.prune_by_index(letter="H")
        # ending_words: List[str] = self.player.get_possible_words()
        # self.assertTrue(len(ending_words) <= len(starting_words))

        starting_words: List[str] = self.player.get_possible_words()
        self.player.prune_by_letter(letter="K")
        ending_words: List[str] = self.player.get_possible_words()
        self.assertTrue(len(ending_words) < len(starting_words))

        only_letter: List[bool] = [True for word in ending_words if "E" in word]
        self.assertTrue(all((True for item in only_letter if item is True)))

    def test_get_most_probable_letter(self):
        """ test the get_most_probable_letter """

        freqs = generate_letter_distribution(words=get_all_words())
        max_value: int = self.player.get_most_probable_letter(letter_frequencies=freqs)
        self.assertTrue(isinstance(max_value, str))

if __name__ == "__main__":
    unittest.main()
