from functools import lru_cache


def _parse(data: list[str]) -> dict[int, list[list[str]]]:
    parsed_data: dict[int, list[list[str]]] = {}
    for line in data:
        card_id = int(line.split(":")[0].split()[1])
        winning_section, got_section = line.split(":")[1].split("|")
        winning_numbers = winning_section.strip().split()
        got_numbers = got_section.strip().split()
        parsed_data[card_id] = [winning_numbers, got_numbers]
    return parsed_data


def part1(_input: list[str]) -> int:
    total = 0
    for winning_numbers, got_numbers in _parse(_input).values():
        matching_numbers = [num for num in got_numbers if num in winning_numbers]
        if len(matching_numbers):
            if len(matching_numbers) == 1:
                total += 1
            else:
                total += 2 ** (len(matching_numbers) - 1)
    return total


def _get_won_games(
    card_id: int,
    game_data: dict[int, list[list[str]]],
    total_cards: int,
    cache: dict[tuple[int, int], int] | None = None,
) -> int:
    if cache is None:
        cache = {}

    if (card_id, total_cards) in cache:
        return cache[(card_id, total_cards)]

    winning_numbers, got_numbers = game_data[card_id]
    matching_numbers = [num for num in got_numbers if num in winning_numbers]

    additional_cards = len(matching_numbers)

    for ci in range(card_id + 1, min(card_id + additional_cards + 1, len(game_data))):
        additional_cards += _get_won_games(ci, game_data, 0, cache)

    cache[(card_id, total_cards)] = additional_cards

    return additional_cards


def part2(_input: list[str]) -> int:
    parsed_data = _parse(_input)
    total_cards = len(parsed_data)

    for card_id in parsed_data:
        total_cards += _get_won_games(card_id, parsed_data, total_cards)

    return total_cards


parts = (part1, part2)
