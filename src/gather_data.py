# gather_data.py
# 
# Gathers data by playing matches.
from dataclasses import dataclass
from pathlib import Path
import stratagem as strat
import json
from datetime import datetime
from time import time
from inspect import getmembers, isclass
from enum import Enum
from tqdm import tqdm

from game import Match

@dataclass
class Experiment:
    num_blanks: int
    num_lives: int
    starting_health: int

# Modify these constants to change the testing parameters/# of trials for averages

# STRATAGEMS = [Greedy, Safe, Balanced, Random, Risky, Scared]
STRATAGEMS = list()

# Import all stratagems from src/stratagem.py except base class and enums
for name, stratagem in getmembers(strat):
    if isclass(stratagem) and name not in ('Stratagem', 'ABC', 'GameState') and not issubclass(stratagem, Enum):
        STRATAGEMS.append(stratagem)


NUM_TRIALS: int = 1000

EXPERIMENTS = [
    Experiment(4, 4, 3),
    # Experiment(2, 4, 3),
    # Experiment(1, 4, 3),
    # Experiment(4, 4, 5),
    # Experiment(2, 4, 5),
    # Experiment(1, 4, 5),
]

# Where to output the data generated
OUT_DIRECTORY = "./data/"

def main() -> None:
    """Run experiments defined in `EXPERIMENTS`."""
    day: str = datetime.fromtimestamp(time()).strftime('%Y-%m-%d')
    Path(f'{OUT_DIRECTORY}{day}/').mkdir(parents=True, exist_ok=True)

    for exp_num, experiment in enumerate(tqdm(EXPERIMENTS, 'Experiments')):
        result_dict: dict = dict()
        result_dict['params'] = {'blanks': experiment.num_blanks, 
                                 'lives': experiment.num_lives, 
                                 'health': experiment.starting_health,
                                 'trials': NUM_TRIALS}
        result_dict['strats'] = dict()

        for strat in tqdm(STRATAGEMS, 'Strats', colour='dodgerblue'):
            result_dict['strats'][strat.__name__.lower()] = dict()
            for enemy_strat in tqdm(STRATAGEMS, 'Enemy Strats', colour='red'):
                wins: int = 0
                for _ in tqdm(range(NUM_TRIALS), 'Trials', colour='green'):
                    new_match: Match = Match(experiment.num_blanks, experiment.num_lives, experiment.starting_health, strat(), enemy_strat())
                    wins += 1 if new_match.play() else 0
                
                result_dict['strats'][strat.__name__.lower()][enemy_strat.__name__.lower()] = f'{(wins/NUM_TRIALS):.3f}'
            
            overall_sum: float = 0.0

            for win_percentage in result_dict['strats'][strat.__name__.lower()].values():
                overall_sum += float(win_percentage)

            result_dict['strats'][strat.__name__.lower()]['overall'] = f'{(overall_sum/len(STRATAGEMS)):.3f}'
                
        current_time: str = datetime.fromtimestamp(time()).strftime('%H-%M-%S')
        with open(f'{OUT_DIRECTORY}{day}/experiment-{exp_num}-({current_time}).json', 'w+') as out_file:
            json.dump(result_dict, out_file)
    
if __name__ == '__main__':
    main()