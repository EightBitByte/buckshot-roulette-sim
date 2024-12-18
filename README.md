> buckshot-roulette-sim

Running experiments on different algorithms to play the indie video game [Buckshot Roulette](https://store.steampowered.com/app/2835570/Buckshot_Roulette/).

## How is Buckshot Roulette Played?
| :bangbang: *Do not attempt this in real life. These are the rules of the video game.* |
| - |

- Two players take turns shooting the shotgun at themselves or at their opponent. 
    - Player One (Dealer) always starts first.
- The shotgun is loaded with blank and live shells, in a sequence unknown to the players. 
    - However, the number of each type of shell is visible to both players. 
    - When the shotgun runs out of shells, it is reloaded with a new load of shells identical to the previous load. 
    - Whomever a player shoots with a live shell takes a point of damage. Blank shells deal no damage. 
- If a player chooses to fire upon themself and a blank is loaded, they do not end their turn. 
- If a player fires a live shell *regardless of the target*, or fires a blank at the opponent, the shooter ends their turn. 
- The game ends when a player has no more health points left, and the player left standing wins.

## Goal of Experiment
When I played Buckshot Roulette for the first time (and lost many, many times), I found myself wondering what the most optimal strategy was. The idea came to mind to experimentally test algorithms in a simulated environment for the game, and thus the idea for this experiment was born.

The goal of the experiment is to see how the win rate of each strategy varies as opposed to other strategies in differing conditions, such as different starting health and blank to live ratio.

## How to Use This Repo

| :bug: *Found a bug? Leave an Issue or PR with a bug fix.* |
| - |

### Installation
To install and run this repo to gather data for yourself, follow these steps:

1. If not installed, install Python >=3.12
2. Run `git clone https://github.com/EightBitByte/buckshot-roulette-sim.git`
3. `cd` into this new directory
4. Run `python -m venv venv`
5. Activate the virtual environment (run `./venv/scripts/activate`)
6. Run `pip install -r requirements.txt`

From here, you can choose to [implement your own stratagems](#implementing-a-stratagem) in `src/stratagem.py`, alter the experiment variables in `src/gather.data.py`, and/or [gather data](#gathering-data).

### Implementing a Stratagem
In `src/stratagem.py`, you should define a class that inherits from the `Stratagem` base class. It should implement one function: `get_move`, which takes a `GameState` object and returns a `Move` object.

The `GameState` object represents the simulated player counting the rounds in the gun; from this information, the simulated player should be able to make a decision.

For instance, one could implement a `Stupid` stratagem that shoots itself when there are more live shells than blanks in the gun, like so:

```python
# src/stratagem.py

class Stupid(Stratagem):
    """
    This player shoots itself when there are more lives in the gun than blanks,
    and shoots the opponent when there are more blanks in the gun than lives.
    """
    def get_move(self, game_state: GameState) -> Move:
        if (game_state.live_shells > game_state.blank_shells):
            return Move.SHOOT_SELF
        elif (game_state.live_shells < game_state.blank_shells):
            return Move.SHOOT_OPPO
        else:
            return Move.SHOOT_SELF
```

As implemented in this repo, you should be able to run the code in `gather_data.py` and see your stratagem against the others implemented. If you want to test only a selection of stratagems, see line 26 in `gather_data.py`.

### Gathering Data
To gather data and plot on a graph:

1. Run `python ./src/gather_data.py` to gather data per your experiments
2. TBD

## Strategies
Each simulated player adopts a different strategy. Those implemented are highlighted below. Those not yet implemented (but are planned) have an :x: next to their names.

### Greedy
This player shoots the opponent if the shell in the chamber is more likely to be live. When the odds are even (50:50), this player will shoot itself in an effort to keep control of the gun (if the current shell is blank).

### Safe
Like [Greedy](#greedy), this player shoots the opponent if the shell in the chamber is more likely to be live. When the odds are even (50:50), this player will shoot the other player in effort to avoid shooting itself.

### Balanced
Like [Greedy](#greedy) and [Safe](#safe), this player shoots the opponent if the shell in the chamber is more likely to be live. When the odds are even (50:50), this player will flip a coin and shoot the opponent if the coin lands on heads, shooting itself otherwise (similar to [Random](#random)).

### Random
This player will flip a coin and shoot the opponent if the coin lands on heads, shooting itself otherwise.

### Reckless
Opposite of [Scared](#scared). This player will always shoot itself until it is sure that the gun only contains live shells. Then, it will shoot the other player until the next load.

### Scared
Opposite of [Reckless](#reckless). This player will always shoot the opponent until it is sure that the gun only contains blank shells.

### Conservative :x:
This player plays the same as [Safe](#Safe) until brought down to 1 HP. Then, it plays like [Scared](#scared).


## Experiments to Run
The following experiments will be run against every single pair of strategies outlined above. The experiment will continue for a fixed number of trials.

| Experiment # | Load            | Number of Trials | Health | Completed? |
| ------------ | --------------- | ---------------- | ------ | ---------- |
| 1            | 4 Blank, 4 Live | 100000           | 3      | :x:        |
| 2            | 2 Blank, 4 Live | 100000           | 3      | :x:        |
| 3            | 1 Blank, 4 Live | 100000           | 3      | :x:        |
| 4            | 4 Blank, 4 Live | 100000           | 5      | :x:        |
| 5            | 2 Blank, 4 Live | 100000           | 5      | :x:        |
| 6            | 1 Blank, 4 Live | 100000           | 5      | :x:        |

## Glossary of Terms
I defined a few terms in the context of this project that I refer to in this `README` and in the code. They are defined below.

| Term          | Definition                                                                              |
| :------------ | :-------------------------------------------------------------------------------------- |
| `blank`       | A blank shell that deals no damage to the target.                                       |
| `health`      | The amount of damage points that a player can take before ending the game.              |
| `live`        | A live shell that deals 1 health point to the target.                                   |
| `load`        | A randomized sequence of shells consisting of an enumerated amount of blanks and lives. |
| `match/trial` | A single game played between two simulated players.                                     |
| `pairing`     | A unique pair of two stratagems.                                                        |