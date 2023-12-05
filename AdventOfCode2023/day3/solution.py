from string import punctuation

SYMBOLS = set(p for p in punctuation if p != ".")


def _parse(data: list[str]) -> list[list[str]]:
    return [list(line) for line in data]


def _get_whole_number(
    row: int, col: int, grid: list[list[str]]
) -> tuple[list[tuple[int, int]], int]:
    curr_numbers = [int(grid[row][col])]
    coord_used: list[tuple[int, int]] = []
    left_col, right_col = col, col
    while (left_col := left_col - 1) >= 0:
        if grid[row][left_col].isdigit():
            curr_numbers.insert(0, int(grid[row][left_col]))
            coord_used.append((row, left_col))
        else:
            break

    while (right_col := right_col + 1) < len(grid[row]):
        if grid[row][right_col].isdigit():
            curr_numbers.append(int(grid[row][right_col]))
            coord_used.append((row, right_col))
        else:
            break
    return coord_used, int("".join([str(i) for i in curr_numbers]))


def _get_surrounding_numbers(row: int, col: int, grid: list[list[str]]) -> list[int]:
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

    found_numbers: list[int] = []
    checked_coords: list[tuple[int, int]] = []
    for r, c in neighbour_deltas:
        if (
            0 <= c <= len(grid[0])
            and 0 <= r <= len(grid)
            and (r, c) not in checked_coords
        ):
            checked_coords.append((r, c))
            if grid[r][c].isdigit():
                coords, whole_number = _get_whole_number(r, c, grid)
                checked_coords += coords
                found_numbers.append(whole_number)

    print("Symbol:", grid[row][col])
    print("Surrounding numbers:", found_numbers)
    return found_numbers


def part1(_input: list[str]) -> int:
    total = 0
    data = _parse(_input)

    for line_index, line in enumerate(data):
        for char_index, character in enumerate(line):
            if character in SYMBOLS:
                surrounding_values = _get_surrounding_numbers(
                    row=line_index,
                    col=char_index,
                    grid=data,
                )
                if surrounding_values:
                    for value in surrounding_values:
                        print("adding", value)
                        total += value
                    print("=====================")
    return total


def part2(_input: list[str]) -> int:
    ...


parts = (part1, part2)
