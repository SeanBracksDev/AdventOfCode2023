def _parse(data: list[str]) -> list[list[list[str]]]:
    parsed_data: list[list[list[str]]] = []
    for line in data:
        winning_section, got_section = line.split(":")[1].split("|")
        winning_numbers = winning_section.strip().split()
        got_numbers = got_section.strip().split()
        parsed_data.append([winning_numbers, got_numbers])
    return parsed_data


def part1(_input: list[str]) -> int:
    total = 0
    for winning_numbers, got_nummbers in _parse(_input):
        count = 0
        for number in got_nummbers:
            if number in winning_numbers:
                count += 1
        if count:
            if count == 1:
                total += 1
            else:
                total += 2 ** (count - 1)
    return total


def part2(_input: list[str]) -> int:
    ...


parts = (part1, part2)
