""" utils.py """

import sys
import random
from typing import List, Tuple, Dict

import requests
import outputformat as out
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
    Gets all words from the dictionary and words with
    size five to eight.

    Return
    ------
    words (list[str]): All words of size five to eight
    """

    min_word_size, max_word_size = 4, 9
    all_words: List[str] = dictionary_connection()
    words: List[str] = list((word.decode() for word in \
        all_words if min_word_size < len(word) < max_word_size\
            and word.isalpha()))

    return words

def get_train_test_set() -> Tuple:
    """ Build train and test set """
    words: List[str] = dictionary_connection()
    word_organizer: Dict[str, str] = {}

    train_set, test_set = [], []

    for word in words:
        first_character: str = word[:1]
        word_organizer[first_character] = word

    for _, value in word_organizer.items():
        shuffled_words: List[str] = random.sample(value, len(value))
        size: int = int(round(0.8*len(shuffled_words)))
        train_set.append(shuffled_words[size:])
        test_set.append(shuffled_words[:size])

    return train_set, test_set


def get_random_word() -> str:
    """
    Provides a random word of length 5 to 7 from
    a list of 5 to 7 letter words.

    return
    ------
    word: str
    """

    words: List[str] = gameplay_words()
    word: str = random.choice(words)

    return word.upper()

def get_display_word(word: str, display: str, letter: str = "") -> str:
    """
    Displays letters as they are guessed.

    Params
    ------
    word (str): word to be guessed
    display (str): shows words as letters are guessed
    letter (str): guessed letter to be added

    Return
    ------
    display (str): string of all guesse letters
    """

    if not letter:
        return "*"*len(word)

    copy_display: List[str] = list(display)

    for i, char_pair in enumerate(zip(display, word)):
        _, char = char_pair
        if letter == char:
            copy_display[i] = letter

    return "".join(copy_display)

def prettify_display(display: str) -> str:
    """
    Makes a nice display of the guessed words.

    Params:
    ------
    display (str): string to be displayed

    Returns
    -------
    copy_display (str): prettified string to be displayed
    """

    copy_display = out.boxtitle(display, return_str=True).strip()

    # for elem in print_display:
    #     copy_display = copy_display +  + " "

    return copy_display


if __name__ == "__main__":
    pass
    # rand_word: str = get_random_word()
    # print(rand_word)
    # p_display: str = "*"*len(rand_word)

    # counts: int = 0
    # num_of_guesses: int = len(rand_word)
    # print(get_display_word(word=rand_word, display=p_display))

    # while counts <= num_of_guesses and "*" in p_display:
    #     char: str = input("Enter a letter: ").upper()

    #     while len(char) > 1:
    #         char = input("You can only guess letters! Enter a letter again: ").upper()

    #     p_display = get_display_word(word=rand_word,\
    #         display=p_display, letter=char)

    #     s_display: str = prettify_display(p_display)
    #     print(s_display)
