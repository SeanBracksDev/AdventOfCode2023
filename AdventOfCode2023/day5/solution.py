def _parse(data: list[str]) -> dict[str, list[int | list[int]]]:
    parsed_data: dict[str, list[int | list[int]]] = {
        "seed-to-soil": [],
        "soil-to-fertilizer": [],
        "fertilizer-to-water": [],
        "water-to-light": [],
        "light-to-temperature": [],
        "temperature-to-humidity": [],
        "humidity-to-location": [],
    }

    for line in data:
        current_conversion_type = ""

        if "seeds:" in line:
            parsed_data["parsed_data"] = [
                int(x) for x in line.split(":")[1].strip().split()
            ]
        elif line.split()[0] in parsed_data:
            current_conversion_type = line.split()[0]
        else:
            parsed_data[current_conversion_type].append([int(x) for x in line.split()])

    return parsed_data


def part1(_input: list[str]) -> int:
    parsed_data = _parse(_input)
    print(parsed_data)


def part2(_input: list[str]) -> int:
    ...


parts = (part1, part2)
