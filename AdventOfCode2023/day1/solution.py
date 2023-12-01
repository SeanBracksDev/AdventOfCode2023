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
    print("adding", int(line_numbers[0] + line_numbers[-1]))
    return int(line_numbers[0] + line_numbers[-1])


def convert_spelt_numbers(
    line: str,
) -> (
    str
):  # ! this does not work, because spelt numbers can overlap, e.g eightwothree should be -> 8wo3, but this produces eigh23
    print(line)
    for sn in SPELT_NUMBERS:
        line = line.replace(sn, str(SPELT_NUMBERS.index(sn) + 1))
    print(line)
    print("=" * 20)
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
