""" hangman.py """

import time
from typing import Any, Dict, Final, List, Set

from .model import generate_letter_distribution, HangmanAI
from .utils import get_all_words, get_random_word

import outputformat as out

def print_hangman_image(mistakes: int):
    """Prints out a gallows image for hangman. The image printed depends on
  the number of mistakes (0-6)."""

    if mistakes <= 0:
        print(''' ____________________
| .__________________|
| | / /     
| |/ /  
| | /     
| |/   
| |     
| |   
| |    
| |     
| |    
| |   
| |   
| |    
| |      
| |      
| |       
| |      
""""""""""""""""""""""""|
|"|"""""""""""""""""""|"|
| |                   | |
: :                   : : 
. .                   . .''')

    elif mistakes == 1:
        print(''' ___________.._______
| .__________))______|
| | / /      ||
| |/ /       ||
| | /        ||.-''.
| |/         |/  _  \\
| |          ||  `/,|
| |          (\\\\`_.'
| |        
| |     
| |    
| |   
| |   
| |    
| |      
| |      
| |       
| |      
""""""""""""""""""""""""|
|"|"""""""""""""""""""|"|
| |                   | |
: :                   : : 
. .                   . .''')
    elif mistakes == 2:
        print(''' ___________.._______
| .__________))______|
| | / /      ||
| |/ /       ||
| | /        ||.-''.
| |/         |/  _  \\
| |          ||  `/,|
| |          (\\\\`_.'
| |          -`--' 
| |          |. .|  
| |          |   |   
| |          | . |    
| |          |   |     
| |          || ||
| |      
| |      
| |       
| |      
""""""""""""""""""""""""|
|"|"""""""""""""""""""|"|
| |                   | |
: :                   : : 
. .                   . .''')
    elif mistakes == 3:
        print(''' ___________.._______
| .__________))______|
| | / /      ||
| |/ /       ||
| | /        ||.-''.
| |/         |/  _  \\
| |          ||  `/,|
| |          (\\\\`_.'
| |         .-`--' 
| |        /Y . .|
| |       // |   |  
| |      //  | . |   
| |     ')   |   |     
| |          || ||
| |      
| |      
| |       
| |      
""""""""""""""""""""""""|
|"|"""""""""""""""""""|"|
| |                   | |
: :                   : : 
. .                   . .''')
    elif mistakes == 4:
        print(''' ___________.._______
| .__________))______|
| | / /      ||
| |/ /       ||
| | /        ||.-''.
| |/         |/  _  \\
| |          ||  `/,|
| |          (\\\\`_.'
| |         .-`--'.
| |        /Y . . Y\\
| |       // |   | \\\\
| |      //  | . |  \\\\
| |     ')   |   |   (`
| |          || ||
| |      
| |      
| |       
| |      
""""""""""""""""""""""""|
|"|"""""""""""""""""""|"|
| |                   | |
: :                   : : 
. .                   . .''')
    elif mistakes == 5:
        print(''' ___________.._______
| .__________))______|
| | / /      ||
| |/ /       ||
| | /        ||.-''.
| |/         |/  _  \\
| |          ||  `/,|
| |          (\\\\`_.'
| |         .-`--'.
| |        /Y . . Y\\
| |       // |   | \\\\
| |      //  | . |  \\\\
| |     ')   |   |   (`
| |          ||'||
| |          ||   
| |          ||   
| |          ||   
| |         / |  
""""""""""""""""""""""""|
|"|"""""""""""""""""""|"|
| |                   | |
: :                   : : 
. .                   . .''')
    else:  # mistakes >= 6
        print(''' ___________.._______
| .__________))______|
| | / /      ||
| |/ /       ||
| | /        ||.-''.
| |/         |/  _  \\
| |          ||  `/,|
| |          (\\\\`_.'
| |         .-`--'.
| |        /Y . . Y\\
| |       // |   | \\\\
| |      //  | . |  \\\\
| |     ')   |   |   (`
| |          ||'||
| |          || ||
| |          || ||
| |          || ||
| |         / | | \\
""""""""""|_`-' `-' |"""|
|"|"""""""\ \       '"|"|
| |        \ \        | |
: :         \ \       : : 
. .          `'       . .''')



def step(player: Any, letter_frequency: Dict[str, int]) -> Dict[str, bool]:
    """
    Simulates a single step of hangman
    """
    guess: str = player.get_most_probable_letter(
            letter_frequencies=letter_frequency
        )

    letter_present: bool = player.has_letter(letter=guess)

    if letter_present:
        player.prune_by_letter(letter=guess)
        player.prune_by_index(letter=guess)

    return {"guess": guess, "present": letter_present}


def play(word: str) -> str:
    """
    Simulates the Hangman game
    """

    state: str
    num_mistakes: int = 0
    max_mistakes: Final[int] = 6
    game_completed: bool = False
    guessed_letters: List[str] = []

    dictionary: List[str] = set(
        (cur_word.decode().upper() for cur_word in get_all_words() if len(cur_word) == len(word))
    )

    ai_player: HangmanAI = HangmanAI(word=word, words=dictionary)
    letter_frequency: Dict[str, int] = generate_letter_distribution(words=dictionary)

    while not game_completed:
        state = ai_player.get_current_state()
        if "*" not in state:
            game_completed = True # pylint: disable=C0103
            print(f"You Win!!! - Your word was: {word}")
            break

        outcome: Dict[str, bool] = step(player=ai_player, letter_frequency=letter_frequency)
        if not outcome.get("present", ""):
            num_mistakes = num_mistakes + 1
            print_hangman_image(mistakes=num_mistakes)

        guessed_letters.append(outcome.get("guess", ""))

        time.sleep(1)

        possible_words: Set[str] = ai_player.get_possible_words()
        letter_frequency: Dict[str, int] = generate_letter_distribution(words=possible_words)

        for guessed in guessed_letters:
            letter_frequency[guessed] = -10

        # state: str = ai_player.get_current_state()
        # print(f"Current Guess: {outcome.get('guess', '')} - Game State: {state}")

        state = ai_player.get_current_state()
        out.boxtitle(state)

        if num_mistakes == max_mistakes:
            game_completed = True
            out.boxtitle(f"You lose!!! Your word was: {word}")

    return state


if __name__ == "__main__":
    current_word = get_random_word()
    play(word=current_word)
