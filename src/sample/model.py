""" model.py """

import string
from collections import defaultdict
from typing import Dict, Final, Set, List

from .utils import get_all_words, get_random_word


class HangmanAI:
    """
    AI model that plays hangman
    """

    def __init__(self, word: str, words: List[str]) -> None:
        self.current_word: str = word
        self.possible_words: Set[str] = words
        self.guessed_word: str = "*" * len(word)
        self.alphabet: List[str] = list(string.ascii_uppercase)

    def prune_by_letter(self, letter: str) -> None:
        """
        Removes all words that donot possess letter
        """

        possible_words: Set[str] = set([
            word for word in self.possible_words if letter in word
        ])

        self.possible_words = possible_words

    def prune_by_index(self, letter: str) -> None:
        """
        Narrow search space by removing words by checking
        if guessed letter occurs at similation position as
        in queried word
        """

        word_pool: Set[str] = set()

        for word in self.possible_words:
            for i, _ in enumerate(zip(self.guessed_word, self.current_word)):
                if self.guessed_word[i] == "*" and self.current_word[i] == word[i] == letter:
                    self.__update_word(i, letter=letter)
                if letter in self.current_word:
                    tmp = list(self.current_word)
                    if tmp[i] == letter:
                        word_pool.add(word)
        self.possible_words = word_pool

    def get_most_probable_letter(self, letter_frequencies: Dict[str, int]) -> str:
        """Provides the letter with the highest probability of occuring"""

        highest_frequency: int = max(letter_frequencies, key=letter_frequencies.get)

        return highest_frequency

    def get_current_state(self) -> str:
        """get the guessing state of the guessing"""
        return self.guessed_word

    def __update_word(self, index: int, letter: str) -> None:
        """Add a guessed letter in hidden word"""
        word_list = list(self.guessed_word)
        word_list[index] = letter
        self.guessed_word = "".join(word_list)

    def get_possible_words(self) -> List[str]:
        """Get all possible words considering the game state"""
        return self.possible_words

    def has_letter(self, letter: str) -> bool:
        """Determines if letter is present in current word"""
        return letter in self.current_word


def generate_letter_distribution(words: List[str]) -> Dict[str, int]:
    """
    Build a table containing the frequencies of every letter.
    """

    table_frequencies: Dict[str, int] = defaultdict(int)
    for word in words:
        for letter in word:
            table_frequencies[letter.upper()] = table_frequencies[letter] + 1

    return table_frequencies


if __name__ == "__main__":
    cur_word: str = get_random_word()
    pos_words: List[str] = set(
        (word.decode().upper() for word in get_all_words() if len(word) == len(cur_word))
    )
    letter_frequency: Dict[str, int] = generate_letter_distribution(words=pos_words)
    guessed_letters: List[str] = []
    hangman_ai: HangmanAI = HangmanAI(word=cur_word, words=pos_words)

    current_mistakes: int = 0 # pylint: disable=C0103
    MAX_MISTAKES: Final[int] = 6
    game_completed: bool = False # pylint: disable=C0103


    while not game_completed or current_mistakes < MAX_MISTAKES:
        game_state: str = hangman_ai.get_current_state()
        if "*" not in game_state:
            game_completed = True # pylint: disable=C0103
            print(f"You Win!!! - Your word was: {cur_word}")
            break
        guess: str = hangman_ai.get_most_probable_letter(
            letter_frequencies=letter_frequency
        )
        guessed_letters.append(guess)
        letter_present = hangman_ai.has_letter(letter=guess)


        if letter_present:
            hangman_ai.prune_by_letter(letter=guess)
            hangman_ai.prune_by_index(letter=guess)
        else:
            current_mistakes = current_mistakes + 1 # pylint: disable=C0103

        pos_words = hangman_ai.get_possible_words()
        letter_frequency = generate_letter_distribution(words=pos_words)

        for guessed in guessed_letters:
            letter_frequency[guessed] = -10

        game_state: str = hangman_ai.get_current_state()
        print(f"Current Guess: {guess} - Game State: {game_state}")