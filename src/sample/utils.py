""" utils.py """

import sys
import random
from typing import List

import requests
from requests.exceptions import ConnectTimeout, HTTPError, ReadTimeout, Timeout


def dictionary_connection() -> List[str]:
    """
    Connects to MIT's wordlist API to collect
    words of lenght five to seven.

    return
    ------
    words: List[str]
    """

    try:
        url: str = "https://www.mit.edu/~ecprice/wordlist.10000"
        response = requests.get(url)
        return response.content.splitlines()
    except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError) as err_msg:
        print(f"Error occured when obtaining dictionary: {str(err_msg)}")
        sys.exit()

def gameplay_words() -> List[str]:
    """
    Gets all words from the dictionary and
    convert them from bytes to strings

    Return
    ------
    words (list[str]): All words of size five to eight
    """

    all_words: List[str] = dictionary_connection()
    words: List[str] = list((word.decode() for word in all_words if word.isalpha()))

    return words

def get_all_words() -> List[str]:
    """ Provides all words in dictionary """

    words: List[str] = gameplay_words()
    return words


def get_random_word() -> str:
    """
    Provides a random word

    return
    ------
    word: str
    """

    words: List[str] = gameplay_words()
    word: str = random.choice(words)

    return word.upper()

def get_word() -> str:
    """
    Provides a random word of length 5 to 7 from
    a list of 5 to 7 letter words.

    return
    ------
    word: str
    """

    words: List[str] = [word for word in gameplay_words() if 5 < len(word) < 8]
    word: str = random.choice(words)

    return word.upper()


if __name__ == "__main__":
    pass
