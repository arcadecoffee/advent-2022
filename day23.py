"""
Advent of Code 2022 Day 23
"""
import sys

from advent_tools import get_daily_input

DAY = 23

TEST = sys.argv[1] == "test" if len(sys.argv) > 1 else False

TEST_DATA = """
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
"""

if TEST:
    def get_daily_input(_):
        for line in TEST_DATA.strip().split("\n"):
            yield line.strip("\n")


def load_data() -> dict[tuple[int, int], bool]:
    data = {}
    x = 0
    for l in get_daily_input(DAY):
        y = 0
        for c in l:
            if c == "#":
                data[x, y] = True
            y += 1
        x += 1
    return data


def count_empty(map_data: list[list[bool]]) -> int:
    h = max([k[0] for k in map_data]) - min([k[0] for k in map_data]) + 1
    w = max([k[1] for k in map_data]) - min([k[1] for k in map_data]) + 1
    return h * w - len(map_data)


def make_moves(map_data: list[list[bool]], rule_order: str) -> list[list[bool]]:
    proposed_moves: dict[tuple[int, int], list[tuple[int, int]]] = {}

    for i, j in map_data:
        proposed_moves[i, j] = [(i, j)]
        surroundings: dict[str, tuple[bool, tuple[int, int]]] = {}
        for direction in ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]:
            r = i + (1 if "S" in direction else -1 if "N" in direction else 0)
            d = j + (1 if "E" in direction else -1 if "W" in direction else 0)
            surroundings[direction] = map_data.get((r, d), False), (r, d)
        if any([surroundings[k][0] for k in surroundings]):
            for direction in rule_order:
                if not any([surroundings[k][0] for k in surroundings if direction in k]):
                    proposed_moves[surroundings[direction][1]] = \
                        proposed_moves.get(surroundings[direction][1], []) + [(i, j)]
                    del proposed_moves[(i, j)]
                    break

    new_map = {}
    for k, v in [(a, b) for (a, b) in proposed_moves.items()]:
        if len(v) > 1:
            for i in v:
                proposed_moves[i] = [i]
            del proposed_moves[k]

    return proposed_moves


def part_1() -> int:
    map_data = load_data()
    rule_order = "NSWE"
    for i in range(10):
        map_data = make_moves(map_data, rule_order)
        rule_order = rule_order[1:] + rule_order[0]
    return count_empty(map_data)


def part_2() -> int:
    map_data = load_data()
    prev_map_data = {}
    rule_order = "NSWE"
    i = -1
    while prev_map_data != map_data:
        prev_map_data = map_data
        map_data = make_moves(map_data, rule_order)
        rule_order = rule_order[1:] + rule_order[0]
        i += 1
    return i


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()

"""
Part 1: 4146
Part 2: 957
"""