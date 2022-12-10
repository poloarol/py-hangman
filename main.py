""" __init__.py """

import argparse
import io
import random
import sys

# import numpy as np
import pandas as pd

from src.sample.hangman import play, human_player
from src.sample.utils import get_all_words, get_random_word, get_word

def obtain_statistics(
    dataframe: pd.DataFrame, current_word: str, guess: str
) -> pd.DataFrame:
    """
    Calculate statistics on how often the model is able to correctly guess a word.
    """

    if "*" in guess:
        dataframe.loc[len(dataframe)] = [current_word, guess, 1, 0, "incomplete", len(current_word)]
    elif current_word.lower() != guess.lower():
        dataframe.loc[len(dataframe)] = [current_word, guess, 1, 0, "wrong", len(current_word)]
    else:
        dataframe.loc[len(dataframe)] = [current_word, guess, 1, 1, "correct", len(current_word)]

    return dataframe


if __name__ == "__main__":

    parser = argparse.ArgumentParser("Welcome to py-Hangman")
    parser.add_argument(
        "-u",
        "--human",
        type=str,
        help="Human player leads the game",
        action="store",
        nargs="*",
    )
    parser.add_argument(
        "-a",
        "--ai",
        type=str,
        help="AI model plays the game",
        action="store",
        nargs="*",
    )
    parser.add_argument(
        "-s",
        "--stats",
        type=str,
        help="Get statistics on AI model",
        action="store",
        nargs="*",
    )

    args = parser.parse_args()

    if args.human:
        word = get_word()
        # print(word)
        human_player(word=word)
    elif args.ai:
        word = get_random_word()
        play(word=word)
    elif args.stats:
        words = get_all_words()
        sample_size: int = int(0.1 * len(words))
        words = random.sample(words, sample_size)

        df: pd.DataFrame = pd.DataFrame(
            columns=["Word", "Guess", "Actual", "Predicted", "Game-Status", "word-length"]
        )

        text_trap = io.StringIO()
        sys.stdout = text_trap

        for word in words:
            game_state = play(word=word.decode())
            df = obtain_statistics(dataframe=df, current_word=word.decode(), guess=game_state)

        df.to_csv("data/hangman-statistics.csv", sep=",", index=False)
    else:
        print("Choose a valid option!")
