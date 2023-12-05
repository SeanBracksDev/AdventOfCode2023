from string import punctuation

SYMBOLS = set(p for p in punctuation if p != ".")


def _parse(data: list[str]) -> list[list[str]]:
    return [list(line) for line in data]


def _find_neighbour_symbols(
    row: int, col: int, grid: list[list[str]], value_index: int
):
    neighbour_deltas = (
        (row - 1, col - 1),  # top left
        (row, col - 1),  # left
        (row + 1, col - 1),  # bottom left
        (row - 1, col),  # top
        (row + 1, col),  # bottom
        (row - 1, col + 1),  # top right
        (row, col + 1),  # right
        (row + 1, col + 1),  # bottom right
    )

    return [
        grid[r][c + value_index]
        for r, c in neighbour_deltas
        if 0 <= c + value_index < len(grid[0]) and 0 <= r < len(grid)
        if grid[r][c + value_index] in SYMBOLS
    ]


def _check_for_symbol(
    line_index: int,
    character_index: int,
    current_value: list[str],
    data: list[list[str]],
) -> bool:
    for value_index in range(len(current_value)):
        symbol_neighbours = _find_neighbour_symbols(
            line_index, character_index, data, value_index
        )
        if symbol_neighbours:
            return True
    return False


def part1(_input: list[str]) -> int:
    total = 0
    data = _parse(_input)

    # for line in data:
    #     print(line)

    current_value: list[str] = []
    current_start_index = -1

    for line in data:
        print(line)
    for line_index, line in enumerate(data):
        for char_index, character in enumerate(line):
            if character.isdigit():
                if not current_value:
                    current_start_index = char_index
                current_value.append(character)

            if char_index == len(line) - 1 or not character.isdigit():
                if current_value:
                    if _check_for_symbol(
                        line_index=line_index,
                        character_index=current_start_index,
                        current_value=current_value,
                        data=data,
                    ):
                        total += int("".join(current_value))
                    current_value = []

    return total


def part2(_input: list[str]) -> int:
    ...


parts = (part1, part2)
