from dataclasses import dataclass
from itertools import batched

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

    def __str__(self) -> str:
        return f"'{', '.join([str(i) for i in range(self.min, self.max + 1)])}'"

    def __lt__(self, other) -> bool:
        return self.min < other.min

    def __gt__(self, other) -> bool:
        return self.min > other.min

    def __iter__(self):
        return iter(range(self.min, self.max + 1))


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


def get_range_overlap(range_1: Range, range_2: Range) -> Range | None:
    """Returns the min and max values overlap between two ranges

    :param Range range_1: range 1
    :param Range range_2: range 2
    :return tuple[int, int] | None: intersecting min & max of ranges or None if no overlap
    """
    if range_1.max < range_2.min or range_2.max < range_1.min:
        return None

    return Range(max(range_1.min, range_2.min), min(range_1.max, range_2.max))


def convert_seeds(seed_range: Range, conversion_mappings: dict[str, list[list[Range]]]) -> list[Range]:
    unconverted_values: list[Range] = [seed_range]
    converted_values: list[Range] = []

    for mapping_name in conversion_mappings:
        for dest_range, source_range in conversion_mappings[mapping_name]:
            # if nothing to convert, skip
            if not unconverted_values:
                break

            # for any unconverted ranges, check if they overlap with the source range
            for r in unconverted_values.copy():
                overlap = get_range_overlap(
                    range_1=r,
                    range_2=source_range,
                )
                if overlap is None:
                    continue

                lower_leftover = Range(r.min, overlap.min - 1) if r.min < overlap.min else None
                upper_leftover = Range(overlap.max + 1, r.max) if r.max > overlap.max else None

                if lower_leftover:
                    unconverted_values.append(lower_leftover)

                if upper_leftover:
                    unconverted_values.append(upper_leftover)

                converted_values.append(
                    Range(
                        dest_range.min + (overlap.min - source_range.min),
                        dest_range.min + (overlap.max - source_range.min),
                    )
                )

                unconverted_values.remove(r)

        # if any values are left over, their value is kept the same
        for r in unconverted_values:
            converted_values.append(r)

        unconverted_values = converted_values
        converted_values = []
    return unconverted_values


def part1(_input: list[str]) -> int:
    seeds, parsed_data = _parse(data=_input)
    parsed_range_data = _parse_ranges(parsed_data)

    return min(list((get_location(s, parsed_range_data) for s in seeds)))


def part2(_input: list[str]) -> int:
    seeds, parsed_data = _parse(data=_input)
    parsed_range_data = _parse_ranges(parsed_data)
    seed_locations = []
    for seed_batch in batched(seeds, 2):
        seed_range = Range(min=seed_batch[0], max=seed_batch[0] + seed_batch[1] - 1)
        seed_locations += convert_seeds(seed_range, parsed_range_data)
    return min(seed_locations).min


parts = (part1, part2)
