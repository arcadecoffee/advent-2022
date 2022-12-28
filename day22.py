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


def load_data():
    data_stream = get_daily_input(DAY)
    map_data: list[str] = []
    path_data: str = ""
    for d in data_stream:
        if d:
            map_data.append(d)
        else:
            path_data = next(data_stream)

    width = max(len(m) for m in map_data)
    map_data = list([m.ljust(width) for m in map_data])

    return map_data, re.findall(r"\d+|[LR]", path_data)


def part_1() -> int:
    facings = ">v<^"

    monkey_map, path = load_data()
    position = (0, monkey_map[0].find("."))
    facing = ">"

    def next_position(r, c, f):
        if f == ">":
            points = monkey_map[r]
            offset = c
        elif f == "<":
            points = "".join(reversed(monkey_map[r]))
            offset = len(points) - c - 1
        elif f == "v":
            points = "".join([m[c] for m in monkey_map])
            offset = r
        else:
            points = "".join([m[c] for m in reversed(monkey_map)])
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

    for p in path:
        if p.isnumeric():
            for _ in range(int(p)):
                position = next_position(*position, facing)
        elif p == "L":
            facing = facings[facings.find(facing) - 1]
        else:
            facing = facings[(facings.find(facing) + 1) % 4]

    return 1000 * (position[0] + 1) + 4 * (position[1] + 1) + facings.find(facing)


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