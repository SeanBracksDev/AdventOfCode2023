import sys
from importlib import metadata, resources

from natsort import natsorted


def main():
    names = sys.argv[1:]
    days = metadata.entry_points().select(group="AdventOfCode2023.days")
    for entry in natsorted(days, key=lambda entry: entry.name):
        if names and entry.name.removeprefix("day") not in names:
            continue
        print(f"Day {entry.name.removeprefix('day')}")
        with resources.files("AdventOfCode2023").joinpath(
            f"{entry.name}/input.txt"
        ).open() as file:
            data = [line.replace("\n", "") for line in file.readlines()]
        print(entry.load()[1](data))
        # for part in entry.load():
        #     print(part(data))
        print()


if __name__ == "__main__":
    main()
