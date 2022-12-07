
""" __init__.py """

from hangman import play
from utils import get_random_word

def main():
    """ application entry point """
    word: str = get_random_word()
    play(word=word)


if __name__ == "__main__":
    main()
