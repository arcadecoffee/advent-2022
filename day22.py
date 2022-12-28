"""
Advent of Code 2022 Day 22
"""
import re
import sys

from advent_tools import get_daily_input

DAY = 22

TEST = sys.argv[1] == "test" if len(sys.argv) > 1 else False

TEST_DATA = """
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""

if TEST:
    def get_daily_input(_):
        for line in TEST_DATA.strip("\n").split("\n"):
            yield line.strip("\n")


def load_data() -> tuple[list[str], list[str]]:
    data_stream = get_daily_input(DAY)
    map_data: list[str] = []
    path_data: list[str] = []
    for d in data_stream:
        if d:
            map_data.append(d)
        else:
            path_data = re.findall(r"\d+|[LR]", next(data_stream))
    width = max(len(m) for m in map_data)
    return list([m.ljust(width) for m in map_data]), path_data


FACINGS = ">v<^"


def part_1() -> int:

    monkey_map, path = load_data()
    row, column = 0, monkey_map[0].find(".")
    facing = ">"

    for p in path:
        if p.isnumeric():
            for _ in range(int(p)):
                row, column = next_position(monkey_map, row, column, facing)
        elif p == "L":
            facing = FACINGS[FACINGS.find(facing) - 1]
        else:
            facing = FACINGS[(FACINGS.find(facing) + 1) % 4]

    return 1000 * (row + 1) + 4 * (column + 1) + FACINGS.find(facing)


def next_position(mm: list[str], r: int, c: int, f: str) -> tuple[int, int]:
    if f == ">":
        points = mm[r]
        offset = c
    elif f == "<":
        points = "".join(reversed(mm[r]))
        offset = len(points) - c - 1
    elif f == "v":
        points = "".join([m[c] for m in mm])
        offset = r
    else:
        points = "".join([m[c] for m in reversed(mm)])
        offset = len(points) - r - 1

    if offset < len(points) - 1 and points[offset + 1] == ".":
        offset = offset + 1
    elif offset >= len(points) - 1 or points[offset + 1] == " ":
        for new_offset in range(offset - 1, -2, -1):
            if new_offset < 0 or points[new_offset] == " ":
                if points[new_offset + 1] == ".":
                    offset = new_offset + 1
                break

    if f == ">":
        return r, offset
    elif f == "<":
        return r, len(points) - offset - 1
    elif f == "v":
        return offset, c
    else:
        return len(points) - offset - 1, c


def part_2() -> int:
    data = get_daily_input(DAY)
    return len(list(data))


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()

"""
Part 1: 75254
"""