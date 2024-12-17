# stratagem.py
#
# Defines stratagems to play the game.
from abc import ABC, abstractmethod
from enum import Enum
from random import randint
from dataclasses import dataclass

@dataclass
class GameState:
    """Represents the state of the game (bullets remaining, items, etc.)"""
    blank_shells: int
    live_shells: int


class Outcome(Enum):
    """Represents an outcome from any given move."""
    SHOOT_SELF_WITH_BLANK = 0
    SHOOT_SELF_WITH_LIVE = 1
    SHOOT_OPPO_WITH_BLANK = 2
    SHOOT_OPPO_WITH_LIVE = 3

class Move(Enum):
    """Represents a possible move by a stratagem."""
    SHOOT_SELF = 0
    SHOOT_OPPO = 1


class Stratagem(ABC):
    def get_move(self, game_state: GameState) -> None | Move:
        """Returns the move to be made based on the current game state."""
        pass


class Greedy(Stratagem):
    """
    This player shoots the opponent if the shell in the chamber is more likely 
    to be live. When the odds are even (50:50), this player will shoot itself 
    in an effort to keep control of the gun (if the current shell is blank).
    """

    def get_move(self, game_state: GameState) -> Move:
        if (game_state.live_shells > game_state.blank_shells):
            return Move.SHOOT_OPPO
        elif (game_state.live_shells < game_state.blank_shells):
            return Move.SHOOT_SELF
        else:
            return Move.SHOOT_SELF


class Safe(Stratagem):
    """
    Like Greedy, this player shoots the opponent if the shell in 
    the chamber is more likely to be live. When the odds are even (50:50), 
    this player will shoot the other player in effort to avoid shooting itself.
    """

    def get_move(self, game_state: GameState) -> Move:
        if (game_state.live_shells > game_state.blank_shells):
            return Move.SHOOT_OPPO
        elif (game_state.live_shells < game_state.blank_shells):
            return Move.SHOOT_SELF
        else:
            return Move.SHOOT_OPPO
        

class Balanced(Stratagem):
    """
    Like Greedy and Safe, this player shoots the opponent if the shell in the 
    chamber is more likely to be live. When the odds are even (50:50), this 
    player will flip a coin and shoot the opponent if the coin lands on heads, 
    shooting itself otherwise (similar to Random).
    """

    def get_move(self, game_state: GameState) -> Move:
        if (game_state.live_shells > game_state.blank_shells):
            return Move.SHOOT_OPPO
        elif (game_state.live_shells < game_state.blank_shells):
            return Move.SHOOT_SELF
        else:
            heads: bool = bool(randint(0 ,1))
            return Move.SHOOT_OPPO if heads else Move.SHOOT_SELF


class Random(Stratagem):
    """
    This player will flip a coin and shoot the opponent if the coin lands on 
    heads, shooting itself otherwise.
    """

    def get_move(self, game_state: GameState) -> Move:
        heads: bool = bool(randint(0, 1))
        return Move.SHOOT_OPPO if heads else Move.SHOOT_SELF


class Risky(Stratagem):
    """
    Opposite of Scared. This player will always shoot itself until it is sure that the gun only 
    contains live shells.
    """

    def get_move(self, game_state: GameState) -> Move:
        if (game_state.blank_shells > 0):
            return Move.SHOOT_SELF
        return Move.SHOOT_OPPO


class Scared(Stratagem):
    """
    Opposite of Risky. This player will always shoot the opponent until it is sure that the gun 
    only contains blank shells.
    """

    def get_move(self, game_state: GameState) -> Move:
        if (game_state.live_shells > 0):
            return Move.SHOOT_OPPO
        return Move.SHOOT_SELF