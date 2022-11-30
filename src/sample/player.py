""" player.py """

from dataclasses import dataclass


class Player:
    """ Defines a player """
    name: str

    @property
    def name(self) -> str:
        """ Provides the player's name """
        return self.name

    @name.setter
    def set_name(self, new_name: str) -> None:
        """ Changes player's name """
        if not new_name:
            raise ValueError("Name cannot be an empty string")
        self.name = new_name


# class ComputerPlayer():
#     """ Defines the computer player """

#     def __init__(self) -> None:
#         pass