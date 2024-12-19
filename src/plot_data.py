# plot_data.py
#
# Uses matplotlib to plot the data of win-rates for each scenario.
import argparse
import matplotlib.pyplot as plt
import numpy as np
from io import TextIOWrapper
from colorama import Fore, Style
from json import load
from pathlib import Path

ERROR_STR: str = Fore.RED + Style.BRIGHT + 'ERROR' + Style.RESET_ALL + ': '

BLANK_BLUE: str = '#1293E7'
RAGEFUL_RED: str = '#EC3436'
PLOT_COLORS = [BLANK_BLUE, RAGEFUL_RED]

parser = argparse.ArgumentParser(
    prog="PlotBuckshotData",
    description="Plots the data gathered from matches of Buckshot Roulette played by Stratagems."
)

parser.add_argument('foldername', help='name of folder with experiment .json files')
parser.add_argument('experiment', help='experiment number')
parser.add_argument('-w', '--winrate', help='plot the winrate of a specific stratagem')
parser.add_argument('-a', '--all', help='plot the overall winrates of all stratagems', action='store_true')
parser.add_argument('-c', '--compone', help='compare algorithm one to algorithm two')
parser.add_argument('-x', '--comptwo', help='add algorithm two')

args = parser.parse_args()


def plot_winrate(results_json: dict, name: str) -> None:
    """
    Plots the win rate of a specific stratagem with name `name`.

    :param dict results_json: The result dictionary to read from.
    :param str name: The name of the stratagem to plot.
    """
    name = name.lower()

    if (name not in results_json['strats']):
        print(f'{ERROR_STR}Stratagem "{name}" not found.')
        exit()
    
    strats: list[str] = list(results_json['strats'][name].keys())
    win_rates: list[float] = [float(i) for i in results_json['strats'][name].values()]

    fig, ax = plt.subplots()

    bars = ax.bar(strats, win_rates, 
                  color=[PLOT_COLORS[i % 2] for i in range(len(win_rates))])
    ax.bar_label(bars, labels=[f'{i * 100:0.1f}%' for i in win_rates])
    ax.set_ylim(0, 1)

    params: dict = results_json['params']
    fig.suptitle(f'{name.title()} Player\'s Win Rates in Buckshot Roulette')
    plt.ylabel('Percentage of Matches Won')
    plt.xlabel('Opponent Algorithm')
    plt.title(f'{params['blanks']} Blanks, {params['lives']} Lives, {params['health']} HP, {params['trials']//1000}k Trials', fontsize=8)
    plt.show()


def plot_overall_winrates(results_json: dict) -> None:
    """
    Plot all overall win rates from an experiment in a bar chart.

    :param dict results_json: The result dictionary to read from.
    """
    strats: list[str] = list(results_json['strats'].keys())
    win_rates: list[float] = list(float(results_json['strats'][strat_name]['overall']) for strat_name in strats)

    fig, ax = plt.subplots()
    bars = ax.bar(strats, win_rates, 
                  color=[PLOT_COLORS[i % 2] for i in range(len(win_rates))])
    ax.bar_label(bars, labels=[f'{i * 100:0.1f}%' for i in win_rates])
    ax.set_ylim(0, 1.2)

    params: dict = results_json['params']
    fig.suptitle(f'All Stratagems\' Overall Win Rates in Buckshot Roulette')
    plt.ylabel('Percentage of Matches Won')
    plt.xlabel('Opponent Algorithm')
    plt.title(f'{params['blanks']} Blanks, {params['lives']} Lives, {params['health']} HP, {params['trials']//1000}k Trials', fontsize=8)
    plt.show()


def plot_winrate_comparison(results_json: dict, alg_one: str, alg_two: str) -> None:
    """
    Plot the comparison of two algorithms from an experiment in a bar chart.

    :param dict results_json: The result dictionary to read from.
    :param str alg_one: The name of the first algorithm to compare.
    :param str alg_two: The name of the second algorithm to compare.
    """
    if alg_one.lower() not in results_json['strats']:
        print(f'{ERROR_STR}Stratagem "{alg_one}" not found.')
        exit()
    if alg_two.lower() not in results_json['strats']:
        print(f'{ERROR_STR}Stratagem "{alg_two}" not found.')
        exit()

    strats = ('balanced', 'greedy', 'random', 'reckless')
    versus_data = {
        'reckless': (0.1, 0.2, 0.3, 0.4),
        'scared': (0.2, 0.4, 0.6, 0.8)
    }

    strats = list(results_json['strats'][alg_one.lower()].keys())
    alg_one_data: list[float] = [float(i) for i in results_json['strats'][alg_one.lower()].values()]
    alg_two_data: list[float] = [float(i) for i in results_json['strats'][alg_two.lower()].values()]


    x = np.arange(len(strats))
    width = 0.35
    fig, ax = plt.subplots()

    alg_one_rects = ax.bar(x, alg_one_data, width, label=alg_one.title(), color=RAGEFUL_RED)
    alg_two_rects = ax.bar(x + width, alg_two_data, width, label=alg_two.title(), color=BLANK_BLUE)

    ax.bar_label(alg_one_rects, labels=[f'{i * 100:0.1f}%' for i in alg_one_data])
    ax.bar_label(alg_two_rects, labels=[f'{i * 100:0.1f}%' for i in alg_two_data])

    # for strategy, winrate in versus_data.items():
    #     offset = width * multiplier
    #     rects = ax.bar(x + offset, winrate, width, label=strategy)
    #     ax.bar_label(rects)
    #     multiplier += 1

    ax.set_xticks(x + (width/2), strats)
    ax.legend(loc='upper left', ncols=2)
    ax.set_ylim(0, 1.2)
    
    plt.ylabel('Percentage of Matches Won')

    params: dict = results_json['params']
    fig.suptitle(f'Comparison of {alg_one.title()} and {alg_two.title()} Players\'s winrates')
    plt.title(f'{params['blanks']} Blanks, {params['lives']} Lives, {params['health']} HP, {params['trials']//1000}k Trials', fontsize=8)
    plt.ylabel('Percentage of Matches Won')
    plt.xlabel('Opponent Algorithm')
    plt.show()



def get_result_json_dict(filename: str) -> dict:
    """
    Returns the result json dict from the json data at `filename`.

    :param str filename: The name of the file to read from.
    """

    with open(filename, 'r') as in_file:
        return load(in_file)


def main() -> None:
    file_path: Path = Path.cwd() / Path(f'{args.foldername}/experiment-{args.experiment}.json')
    
    if not file_path.is_file():
        print(ERROR_STR + f'Folder "{file_path}" not found.')

    results: dict = get_result_json_dict(file_path)

    if args.winrate:
        plot_winrate(results, args.winrate)
    elif args.all:
        plot_overall_winrates(results)
    elif args.compone and args.comptwo:
        plot_winrate_comparison(results, args.compone, args.comptwo)



if __name__ == '__main__':
    main()