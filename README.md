> buckshot-roulette-sim

Running experiments on different algorithms to play the game [Buckshot Roulette](https://store.steampowered.com/app/2835570/Buckshot_Roulette/).


## Experimental Variables
There are a few different variables that we can fix or change to influence how the outcomes of the games go.

`Fixed` variables do not change from experiment to experiment.

`Not Implemented` variables do not impact the experiment at all because I haven't gotten around to implementing them.

`Variable` variables change from experiment to experiment.

| Variable         | Description                                                          | Status            |
| ---------------- | -------------------------------------------------------------------- | ----------------- |
| Items            | Whether or not the players should have access to items.              | `Not Implemented` |
| Shell Amounts    | The amount of lives and blanks in the gun at each load.              | `Fixed`           |
| Health           | The amount of damage a player can receive before the game is called. | `Fixed`           |
| Strategy         | The strategy for a simulated player to take.                         | `Variable`        |
| Number of Trials | The number of games for the pair to play.                            | `Fixed`           |

## Strategies
Each simulated player adopts a different strategy. Those implemented are highlighted below:

### Greedy
This player shoots the opponent if the shell in the chamber is more likely to be live. When the odds are even (50:50), this player will shoot itself to keep control of the gun (if the current shell is blank).

### Safe
Like [Greedy](#greedy), this player shoots the opponent if the shell in the chamber is more likely to be live. When the odds are even (50:50), this player will shoot the other player in effort to avoid shooting itself.

### Balanced
Like [Greedy](#greedy) and [Safe](#safe), this player shoots the opponent if the shell in the chamber is more likely to be live. When the odds are even (50:50), this player will flip a coin and shoot the opponent if the coin lands on heads, shooting itself otherwise (similar to [Random](#random)).

### Random
This player will flip a coin and shoot the opponent if the coin lands on heads, shooting itself otherwise.

### Risky/Suicidal
This player will always shoot itself until it is sure that the gun only contains live shells.

### Scared/Super Safe
This player will always shoot the opponent until it is sure that the gun only contains blank shells.

## Experiments to Run
The following experiments will be run against every single pair of strategies outlined above. The experiment will continue for a fixed number of trials.

| Experiment # | Completed?     | Load             | Number of Trials | Health |
| ------------ | -------------- | ---------------- | ---------------- | ------ |
| 1            | :red_circle:   | 4 Blank, 4 Live  | 100000           | 3      |
| 2            | :green_circle: | 2 Blank, 4 Live  | 100000           | 3      |
| 3            | :red_circle:   | 1 Blank, 4 Live  | 100000           | 3      |
| 4            | :red_circle:   | 4 Blank, 4 Live  | 100000           | 5      |
| 5            | :green_circle: | 2 Blank, 4 Live  | 100000           | 5      |
| 6            | :red_circle:   | 1 Blank, 4 Live  | 100000           | 5      |