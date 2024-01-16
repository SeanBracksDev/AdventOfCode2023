from dataclasses import dataclass

import numpy as np


@dataclass
class Race:
    time: int
    distance: int


def _parse_input_1(_input: list[str]) -> list[Race]:
    races = []
    times, distances = [], []

    for line in _input:
        if "Time" in line:
            times = line.split(":")[1].split()
        else:
            distances = line.split(":")[1].split()

    for t, d in zip(times, distances):
        races.append(Race(time=int(t), distance=int(d)))

    return races


def _parse_input_2(_input: list[str]) -> Race:
    t, d = 0, 0
    for line in _input:
        if "Time" in line:
            t = line.split(":")[1].replace(" ", "")
        else:
            d = line.split(":")[1].replace(" ", "")

    return Race(time=int(t), distance=int(d))


def get_number_of_win_combinations(race: Race) -> int:
    race_wins = 0
    for hold_button_time in range(race.time + 1):
        time_left = race.time - hold_button_time
        if time_left * hold_button_time > race.distance:
            race_wins += 1
    return race_wins


def part1(_input: list[str]) -> int:
    races = _parse_input_1(_input)
    race_win_combinations: list[int] = []
    for r in races:
        race_win_combinations.append(get_number_of_win_combinations(r))
    return np.prod(race_win_combinations)


def part2(_input: list[str]) -> int:
    # ? TODO This could be done in a more efficient way, but it works so ¯\_(ツ)_/¯
    race = _parse_input_2(_input)
    return get_number_of_win_combinations(race)


parts = (part1, part2)
