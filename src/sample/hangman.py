""" hangman.py """

from typing import List, Tuple, Dict

from utils import get_display_word, prettify_display


class Hangman:
    """
    Defines the hangman class, by providing
    methods to play the game.
    """

    def __init__(self, word: str) -> None:
        self.current_word: str = word
        self.win_reward: int = 30
        self.correct_reward: int = 1
        self.incorrect_reward: int = -1
        self.lose_reward: int = -1
        self.repeated_guessing_penalty: int = -100
        self.guessed: List[str] = []
        self.completed: bool = False
        self.answer: Dict = {'ans': ""}

    def __post_init__(self):
        self.current_board: str = "*" * len(self.current_word)
        self.number_of_guesses: int = len(self.current_word)

    def play(self) -> bool:
        """ allows to play the game """

        counter: int = 0
        print(get_display_word(word=self.current_word, display=self.current_board))

        while counter <= self.number_of_guesses and "*" in self.current_board:
            character: str = input("Enter a letter: ").upper()

            while len(character) > 1:
                character = input("You can only guess letters! Enter a letter again: ").upper()

            if not character.isalpha():
                raise TypeError("Can only accept alphabet")

            print_display = get_display_word(word=self.current_word,\
                display=self.current_board, letter=character)

            screen_display: str = prettify_display(print_display)
            print(screen_display)

        game_finished: bool = False

        if "*" in self.current_board:
            return game_finished

        return not game_finished

    def get_board(self) -> str:
        """ Provides the state of the board """
        return self.current_board

    def step(self, letter: str) -> Tuple:
        """ Provides steps for the AI to play hangman """

        if not letter.isalpha():
            raise TypeError("Only use the alohabet")

        if letter not in self.current_word:
            self.guessed.append(letter)
            self.number_of_guesses = self.number_of_guesses + 1
            print(f"{letter} already used.")

            return self.get_board(), self.repeated_guessing_penalty, self.completed, self.answer

        if letter in self.current_word:
            for i in self.current_word:
                if letter == self.current_word[i]:
                    self.current_board[i] = letter
                    self.correct_reward = self.correct_reward + 1
                    self.number_of_guesses = self.number_of_guesses + 1

            if "*" not in self.current_board and self.number_of_guesses <= len(self.current_word):
                print("You Win !!!")
                self.completed = True
                self.answer['ans'] = self.current_board
                return self.get_board(), self.win_reward, self.completed, self.answer

            self.answer['ans'] = self.current_board
            return self.get_board(), self.correct_reward, self.completed, self.answer

        if "*" in self.current_board:
            if self.number_of_guesses >= len(self.current_word):
                self.completed = True
                print("You lose !!!")

                self.answer['ans'] = self.current_board
                return self.get_board(), self.lose_reward, self.completed, self.answer

            self.answer['ans'] = self.current_board
            return self.get_board(), self.incorrect_reward, self.completed, self.answer

        return None