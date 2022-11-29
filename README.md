# py-Hangman

A python implementation of the hangman game.

## Implementation
1. Obtains a list of 5 to 7 letter words MIT's word API
2. A word in randonly selected for the list
3. User guesses the word, character by character but has
    length of word + 1 guess
4. User can only put guess one letter at the time
5. If chacracter is present in chosen word, position is replaced
    else asterisk remains in the position
6. Words are displayed at each step

## To-Do
1. Begin main page for user prompts
2. Write unit tests for modules
3. Develop a GUI (tkinter or pyQT)