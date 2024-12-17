# game.py
#
# Runs the game simulation and outputs the winner of two algorithms.
from dataclasses import dataclass
from stratagem import Stratagem
from random import shuffle

@dataclass
class GameState:
    """Represents the state of the game (bullets remaining, items, etc.)"""
    blank_shells: int
    live_shells: int


class Match:
    """Represents a match between two players. Match completes when one player runs out of health."""
    def __init__(self, num_blanks: int, num_live: int, 
                 starting_health: int,
                 player_one_strat: Stratagem, 
                 player_two_strat: Stratagem) -> None:
        self._state: GameState = GameState(num_blanks, num_live)
        self._p1: Stratagem = player_one_strat
        self._p2: Stratagem = player_two_strat

        self._p1_health: int = starting_health
        self._p2_health: int = starting_health

        self._shell_order: list[bool] = [True] * num_live + [False] * num_blanks
        shuffle(self._shell_order)

    
    def _get_next_shell(self) -> bool:
        """Returns true if the next shell is live, false otherwise."""
        is_live: bool = self._shell_order.pop()

        return is_live


    def play(self, visual: bool = False) -> bool:
        """
        Runs the simulation and outputs the result.

        :param bool visual: Whether or not to output play-by-play in `stdout`.
        :returns bool: Returns `True` if player one wins, `False` if player two wins.
        """
        is_player1_turn: bool = True
    
        while self._p1_health > 0 and self._p2_health > 0:
            pass

        return True
