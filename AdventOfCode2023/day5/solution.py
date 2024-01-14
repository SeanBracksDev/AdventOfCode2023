from dataclasses import dataclass
from itertools import batched
import bisect

MAPPING_NAMES = (
    "seed-to-soil",
    "soil-to-fertilizer",
    "fertilizer-to-water",
    "water-to-light",
    "light-to-temperature",
    "temperature-to-humidity",
    "humidity-to-location",
)


@dataclass
class Range:
    """data structure for mine & max of a range numbers."""

    min: int
    max: int


def _parse(data: list[str]) -> tuple[list[int], dict[str, list[list[int]]]]:
    parsed_conversion_data: dict[str, list[list[int]]] = {k: [] for k in MAPPING_NAMES}
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
            parsed_conversion_data[current_conversion_type].append([int(x) for x in line.split()])

    return seeds, parsed_conversion_data


def _parse_ranges(data: dict[str, list[list[int]]]) -> dict[str, list[list[Range]]]:
    parsed_ranges = {k: [] for k in MAPPING_NAMES}
    for mapping_name in MAPPING_NAMES:
        for entry in data[mapping_name]:
            parsed_ranges[mapping_name].append(
                [
                    Range(entry[0], entry[0] + entry[2] - 1),
                    Range(entry[1], entry[1] + entry[2] - 1),
                ]
            )

    return parsed_ranges


def get_location(seed: int, conversion_mappings: dict[str, list[list[Range]]]) -> int:
    seed_conversion = seed
    for mapping_name in conversion_mappings:
        for range_map in conversion_mappings[mapping_name]:
            if range_map[1].min <= seed_conversion <= range_map[1].max:
                seed_conversion = range_map[0].min + (seed_conversion - range_map[1].min)
                break
    return seed_conversion


def get_range_overlap(range_1: Range, range_2: Range) -> tuple[int, int] | tuple[None, None]:
    """Returns the min and max values overlap between two ranges

    :param Range range_1: range 1
    :param Range range_2: range 2
    :return tuple[int, int] | None: intersecting min & max of ranges or None if no overlap
    """
    if range_1.max < range_2.min or range_2.max < range_1.min:
        return None, None

    return max(range_1.min, range_2.min), min(range_1.max, range_2.max)


def convert_seeds(seed_range: Range, conversion_mappings: dict[str, list[list[Range]]]):
    curr_values = list(range(seed_range.min, seed_range.max + 1))
    converted_values = []
    # print(curr_values)
    for mapping_name in conversion_mappings:
        # print(mapping_name)
        for dest_range, source_range in conversion_mappings[mapping_name]:
            overlap = get_range_overlap(
                range_1=Range(min=min(curr_values), max=max(curr_values)),
                range_2=source_range,
            )
            if overlap[0] is None:
                continue

            overlap_values = list(range(overlap[0], overlap[1] + 1))
            dest_range_values = list(range(dest_range.min, dest_range.max + 1))
            source_range_values = list(range(source_range.min, source_range.max + 1))
            # print(f"{overlap=}")
            # print(f"{source_range_values=}")
            # print(f"{dest_range_values=}")
            # print(f"{seed_range=}")
            for v in curr_values.copy():
                if v in overlap_values:
                    bisect.insort(converted_values, dest_range_values[source_range_values.index(v)])
                    curr_values.remove(v)

            if not curr_values:
                break

        # if any values are left over, their value is kept the same
        for v in curr_values.copy():
            bisect.insort(converted_values, v)
            curr_values.remove(v)

        # print(converted_values)
        # print("*" * 50)
        curr_values, converted_values = converted_values, curr_values

    return curr_values


def part1(_input: list[str]) -> int:
    seeds, parsed_data = _parse(data=_input)
    parsed_range_data = _parse_ranges(parsed_data)

    return min(list((get_location(s, parsed_range_data) for s in seeds)))


def part2(_input: list[str]) -> int:
    # TODO
    seeds, parsed_data = _parse(data=_input)
    parsed_range_data = _parse_ranges(parsed_data)
    seed_locations = []
    for seed_batch in batched(seeds, 2):
        seed_range = Range(min=seed_batch[0], max=seed_batch[0] + seed_batch[1] - 1)
        seed_locations += convert_seeds(seed_range, parsed_range_data)

    return min(seed_locations)


parts = (part1, part2)
