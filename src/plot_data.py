# plot_data.py
#
# Uses matplotlib to plot the data of win-rates for each scenario.
import argparse
import matplotlib.pyplot as plt
from io import TextIOWrapper
from colorama import Fore, Style
from json import load
from pathlib import Path

ERROR_STR: str = Fore.RED + Style.BRIGHT + 'ERROR' + Style.RESET_ALL + ': '

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
    
    strats: list[str] = list()
    win_rates: list[float] = list()
    for strat_name, win_str in results_json['strats'][name].items():
        strats.append(strat_name)
        win_rates.append(float(win_str))
    x = list(range(len(win_rates)))

    fig, ax = plt.subplots()

    colors = ['#1293E7', '#EC3436']
    
    bars = ax.bar(x, win_rates, 
                  tick_label=strats, 
                  color=[colors[i % 2] for i in range(len(win_rates))])
    ax.bar_label(bars)

    params: dict = results_json['params']
    fig.suptitle(f'{name.title()} Player\'s Performance in Buckshot Roulette')
    plt.title(f'{params['blanks']} Blanks, {params['lives']} Lives, {params['health']} HP, {params['trials']//1000}k Trials', fontsize=8)
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

    if args.winrate:
        plot_winrate(get_result_json_dict(file_path), args.winrate)



if __name__ == '__main__':
    main()