# py-Hangman

A python implementation of the hangman game.
Complemented with a rule-based NLP system.

## Implementation
### Human Player
1. Obtains a list of 5 to 7 letter words MIT's word API
2. A word in randonly selected for the list
3. User guesses the word, character by character but has
    length of word + 1 guess
4. User can only put guess one letter at the time
5. If chacracter is present in chosen word, position is replaced
    else asterisk remains in the position
6. Words are displayed at each step

### AI Player
1. Receives a random word
2. Narrows down the se of words by length first
3. Builds a table of frequencies for each letter
4. Provides the most probable word
5. If present, all positions where it belongs are revelead
    all words not containing the word are letter are discarded,
    even at the position they appear
6. The word set are adjusted
7. The frequency of each letter are calculated
8. Steps 3 - 7 are repeated till the game is done

## To-Do
1. Get a larger dictionary of words
2. Get statistics, on how often models wins vs losses
3. Build a GUI

## How to Use
1. statistics: python main.py --stats abc
    Current implementation seems to be faulty, as
    model seems not to be able to solve puzzle.
    (Might be due to the limited dictionary size)
2. ai player: python main.py --ai abc
3. human player: python main.py --human abc