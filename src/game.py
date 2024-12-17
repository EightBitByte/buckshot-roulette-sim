# game.py
#
# Runs the game simulation and outputs the winner of two algorithms.
from stratagem import Stratagem, Move, Outcome, GameState
from random import shuffle

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

        self._load: tuple[int, int] = (num_live, num_blanks)

        self._shell_order: list[bool] = [True] * num_live + [False] * num_blanks
        shuffle(self._shell_order)


    def _reload(self) -> None:
        """Reloads the shell order and shuffles."""
        self._shell_order: list[bool] = [True] * self._load[0] + [False] * self._load[1]
        shuffle(self._shell_order)

        self._state = GameState(self._load[0], self._load[1])
    

    def _get_outcome(self, move: Move) -> Outcome:
        """Get the outcome of a given move."""
        shell_live: bool = self._shell_order.pop()

        self._state.blank_shells -= 0 if shell_live else 1
        self._state.live_shells -= 1 if shell_live else 0
        
        if shell_live and move == Move.SHOOT_SELF:
            return Outcome.SHOOT_SELF_WITH_LIVE
        if shell_live and move == Move.SHOOT_OPPO:
            return Outcome.SHOOT_OPPO_WITH_LIVE
        if not shell_live and move == Move.SHOOT_SELF:
            return Outcome.SHOOT_SELF_WITH_BLANK
        if not shell_live and move == Move.SHOOT_OPPO:
            return Outcome.SHOOT_OPPO_WITH_BLANK
    
    def _print_load(self) -> None:
        """Prints the current load of the shotgun for debug purposes."""
        for is_live in self._shell_order[::-1]:
            if is_live:
                print('\x1b[31mL\x1b[0m', end='')
            else:
                print('\x1b[34mB\x1b[0m', end='')
        print()
    

    def play(self, visual: bool = False, pause: bool = False) -> bool:
        """
        Runs the simulation and outputs the result.

        :param bool visual: Whether or not to output play-by-play in `stdout`.
        :param bool pause: Whether or not to pause after every action.
        :returns bool: Returns `True` if player one wins, `False` if player two wins.
        """
        player1_turn: bool = True

        if visual:
            print(f'\x1b[1m\x1b[32mSTARTING NEW GAME\x1b[0m: \x1b[31m{self._p1.__class__.__name__}\x1b[0m VS \x1b[34m{self._p2.__class__.__name__}\x1b[0m')
    
        while self._p1_health > 0 and self._p2_health > 0:
            # If shotgun empty, reload
            if (len(self._shell_order) == 0):
                self._reload()

            if visual:
                if player1_turn:
                    print(f'===== \x1b[31mPlayer One [{self._p1.__class__.__name__}] Turn\x1b[0m =====')
                else: 
                    print(f'===== \x1b[34mPlayer Two [{self._p2.__class__.__name__}] Turn\x1b[0m =====')

                print(self._state)
                print('Current Load: ', end='')
                self._print_load()

            current_player: Stratagem = self._p1 if player1_turn else self._p2
            outcome: Outcome = self._get_outcome(current_player.get_move(self._state))

            # Hurt player that shot self
            if outcome == Outcome.SHOOT_SELF_WITH_LIVE and player1_turn:
                self._p1_health -= 1
            elif outcome == Outcome.SHOOT_SELF_WITH_LIVE and not player1_turn:
                self._p2_health -= 1

            # Hurt opponent shot
            elif outcome == Outcome.SHOOT_OPPO_WITH_LIVE and player1_turn:
                self._p2_health -= 1
            elif outcome == Outcome.SHOOT_OPPO_WITH_LIVE and not player1_turn:
                self._p1_health -= 1

            if visual:
                print(f'Player chooses: {outcome.name}')
                print(f'\x1b[31mP1\x1b[0m Health: ' + 'X︎' * self._p1_health)
                print(f'\x1b[34mP2\x1b[0m Health: ' + 'X︎' * self._p2_health)
                print()

                if pause:
                    print('Press Enter to Continue... ', end='')
                    input()
                    print()

            # If didn't shoot self with blank, change turns
            if outcome != Outcome.SHOOT_SELF_WITH_BLANK:
                player1_turn = not player1_turn

        if visual:
            if self._p1_health > 0:
                print(f'\x1b[1m\x1b[31mPlayer One ({self._p1.__class__.__name__}) Wins!\x1b[0m')
            else:
                print(f'\x1b[1m\x1b[34mPlayer Two ({self._p2.__class__.__name__}) Wins!\x1b[0m')

        return self._p1_health > 0