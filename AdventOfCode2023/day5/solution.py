MAPPING_NAMES = (
    "seed-to-soil",
    "soil-to-fertilizer",
    "fertilizer-to-water",
    "water-to-light",
    "light-to-temperature",
    "temperature-to-humidity",
    "humidity-to-location",
)


def _parse(data: list[str]) -> dict[str, list[int | list[int]]]:
    parsed_conversion_data: dict[str, list[int | list[int]]] = {
        k: [] for k in MAPPING_NAMES
    }
    seeds = []
    current_conversion_type = ""
    for line in data:
        if len(line) == 0:
            continue
        if "seeds:" in line:
            seeds = [int(x) for x in line.split(":")[1].strip().split()]
        elif line.split()[0] in parsed_conversion_data:
            current_conversion_type = line.split()[0]
        else:
            parsed_conversion_data[current_conversion_type].append(
                [int(x) for x in line.split()]
            )

    return seeds, parsed_conversion_data


def _parse_ranges(
    data: dict[str, list[int | list[int]]]
) -> dict[str, list[int | list[tuple[int]]]]:
    parsed_ranges = {k: [] for k in MAPPING_NAMES}

    for mapping_name in MAPPING_NAMES:
        for entry in data[mapping_name]:
            parsed_ranges[mapping_name].append(
                [
                    (entry[0], entry[0] + entry[2] - 1),
                    (entry[1], entry[1] + entry[2] - 1),
                ]
            )

    return parsed_ranges


def part1(_input: list[str]) -> int:
    seeds, parsed_data = _parse(_input)
    parsed_range_data = _parse_ranges(parsed_data)

    seed_locations = []

    for seed in seeds:
        seed_conversion = seed
        for mapping_name in MAPPING_NAMES:
            for range_map in parsed_range_data[mapping_name]:
                if range_map[1][0] <= seed_conversion <= range_map[1][1]:
                    seed_conversion = range_map[0][0] + (
                        seed_conversion - range_map[1][0]
                    )
                    break
        seed_locations.append(seed_conversion)
    return min(seed_locations)


def part2(_input: list[str]) -> int:
    ...


parts = (part1, part2)
