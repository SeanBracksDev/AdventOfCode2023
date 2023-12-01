SPELT_NUMBERS = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]


def get_line_value(line: str) -> int:
    line_numbers = "".join([c for c in line if c.isdigit()])
    return int(line_numbers[0] + line_numbers[-1])


def convert_spelt_numbers(line: str) -> str:
    for sn in SPELT_NUMBERS:
        line = line.replace(sn, f"{sn}{SPELT_NUMBERS.index(sn) + 1}{sn}")
    return line


def part1(_input: list[str]):
    total = 0
    for line in _input:
        total += get_line_value(line)
    return total


def part2(_input: list[str]):
    total = 0
    for line in _input:
        line = convert_spelt_numbers(line)
        total += get_line_value(line)
    return total


parts = (part1, part2)
