import random
from enum import Enum
from typing import List, Tuple, Union

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

NUM_DOORS_DEFAULT = 3
WINNING_PRIZE = 'car'
LOSING_PRIZE = 'goat'


class GameStrategy(Enum):
    STICK = 'stick'
    SWITCH = 'switch'


class GameResult(Enum):
    LOST = 'lost'
    WON = 'won'


def play_game(strategy: Union[GameStrategy, str], num_doors: int = NUM_DOORS_DEFAULT) -> str:
    """
    Play a single iteration of the Monte Hall problem.
    :param strategy: The player can choose to stick with or switch from their initial choice.
    :param num_doors: The number of doors in the game. The default is 3.
    :return: Returns a value indicating whether the player won or lost.
    """

    if not isinstance(strategy, GameStrategy):
        strategy = GameStrategy(strategy)

    # Create all doors with goat.
    doors = [LOSING_PRIZE] * num_doors

    # Randomly replace with a car behind one of the doors.
    doors[random.randint(0, num_doors - 1)] = WINNING_PRIZE
    print(f'Doors: {doors}')

    # Play the game!

    # 1. Player picks a door, but it is not opened.
    player_choice = random.randint(0, num_doors - 1)
    print(f'Player chooses door #{player_choice}')

    # 2. Host will now select one of the other doors having a goat. Door is then opened.
    host_choices = [index for index, prize in enumerate(doors) if index != player_choice and prize != WINNING_PRIZE]
    print(f'Hosts choices: {host_choices}')

    host_choice = random.choice(host_choices)
    print(f'Host opens door #{host_choice} ({doors[host_choice]})')

    # 3. Player now decides if they want to change their first choice.
    if strategy == GameStrategy.SWITCH:
        print('Player switches door choice.')

        # Player is only allowed to choose the door not yet chosen.
        player_choice = [i for i, prize in enumerate(doors) if i != player_choice and i != host_choice][0]

    print(f'Player\'s final door choice #{player_choice}')

    result = GameResult.WON if doors[player_choice] == WINNING_PRIZE else GameResult.LOST
    print(f'Player {result.value}!')

    return result.value


def simulate_games(iterations: int, num_doors: int = NUM_DOORS_DEFAULT) -> List[Tuple[str, str]]:
    """
    Play multiple iterations of the Monte Hall problem, randomly choosing a game strategy each time.
    :param iterations: The number of times to play the game.
    :param num_doors: The number of doors in the game. The default is 3.
    :return: Returns a list of tuples containing the strategy and the game result.
    """

    if num_doors < NUM_DOORS_DEFAULT:
        raise ValueError(f'Number of doors must be greater than or equal to {NUM_DOORS_DEFAULT}')

    game_results = []

    for i in range(iterations):
        strategy = random.choice(list(GameStrategy))
        result = play_game(strategy, num_doors)
        game_results.append((strategy.value, result))

    return game_results


def plot_data(results, num_doors: int = NUM_DOORS_DEFAULT) -> None:
    num_stick_wins = 0
    num_stick_total = 0

    num_switch_wins = 0
    num_switch_total = 0

    win_pct = []

    # Calculate win percentage over time.
    for i, row in enumerate(results):
        strategy = row[0]
        result = row[1]

        # win pct = # wins / # total
        if strategy == GameStrategy.STICK.value:
            num_stick_wins += 1 if result == GameResult.WON.value else 0
            num_stick_total += 1
            win_pct.append([i + 1, num_stick_wins / num_stick_total, strategy])
        else:
            num_switch_wins += 1 if result == GameResult.WON.value else 0
            num_switch_total += 1
            win_pct.append([i + 1, num_switch_wins / num_switch_total, strategy])

    df = pd.DataFrame(data=win_pct, columns=['total', 'percent', 'strategy'])

    sns.lineplot(data=df, x='total', y='percent', hue='strategy')
    plt.title(f'Monte Hall Problem ({num_doors} doors)', fontsize=18)
    plt.xlabel('Games Played', fontsize=12)
    plt.ylabel('Probability of Winning', fontsize=12)
    plt.legend(title='Strategy')
    plt.show()


if __name__ == '__main__':
    ITERATIONS = 1000
    NUM_DOORS = 3

    strategy_results = simulate_games(ITERATIONS, NUM_DOORS)
    plot_data(strategy_results)
