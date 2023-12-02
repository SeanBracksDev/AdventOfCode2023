import numpy

BAG = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def _parse_game_data(data: str) -> list[dict]:
    parsed_data = []
    for set in data.split(";"):
        colour_data = set.split(",")
        set_dict = {c.split()[1]: int(c.split()[0]) for c in colour_data}
        parsed_data.append(set_dict)
    return parsed_data


def part1(_input: list[str]) -> int:
    total = 0
    for line in _input:
        game, data = line.split(":")

        game_id = int(game.split()[1])
        parsed_colour_data = _parse_game_data(data)

        valid = True
        for set in parsed_colour_data:
            for colour, count in set.items():
                if count > BAG[colour]:
                    valid = False
                    break

        if valid:
            total += game_id
    return total


def part2(_input: list[str]) -> int:
    total = 0
    for line in _input:
        data = line.split(":")[1]
        parsed_colour_data = _parse_game_data(data)

        minimum_colours = dict()

        for set in parsed_colour_data:
            for colour, count in set.items():
                if count > minimum_colours.get(colour, 0):
                    minimum_colours[colour] = count
        total += numpy.prod([c for c in minimum_colours.values()])
    return total


parts = (part1, part2)
