""" __init__.py """

import argparse

from src.sample.hangman import play
from src.sample.utils import get_random_word

if __name__ == "__main__":

    parser = argparse.ArgumentParser("Welcome to py-Hangman")
    parser.add_argument("-u", "--human", type=str, help="Human player leads the game", action="store", nargs="*")
    parser.add_argument("-a", "--ai", type=str, help="AI model plays the game", action="store", nargs="*")
    parser.add_argument("-s", "--stats", type=str, help="Get statistics on AI model", action="store", nargs="*")

    words: str
    args = parser.parse_args()

    if args.human:
        word = get_random_word()
    elif args.ai:
        word = get_random_word()
        play(word=word)
    elif args.stats:
        pass
    else:
        print("Choose a valid option!")
