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


def load_data() -> list[list[bool]]:
    data: list[list[bool]] = [[c == "#" for c in l] for l in get_daily_input(DAY)]
    return data


def count_empty(map_data: list[list[bool]]) -> int:
    return len(map_data) * len(map_data[0]) - sum([sum(m) for m in map_data])


def dump_map(map_data: list[list[bool]]):
    print("\n".join(["".join(["#" if c else "." for c in m]) for m in map_data]))


def pad_map(map_data: list[list[bool]]) -> list[list[bool]]:
    new_map: list[list[bool]] = [[False] * (len(map_data[0]) + 2)]
    for m in map_data:
        new_map.append([False] + m + [False])
    new_map.append([False] * (len(map_data[0]) + 2))
    return new_map


def make_moves(map_data: list[list[bool]], rule_order: str) -> list[list[bool]]:
    proposed_moves: dict[tuple[int, int], list[tuple[int, int]]] = {}

    for i in range(1, len(map_data) - 1):
        for j in range(1, len(map_data[i]) - 1):
            if map_data[i][j]:
                proposed_moves[(i, j)] = [(i, j)]
                surroundings: dict[str, tuple[bool, tuple[int, int]]] = {}
                for direction in ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]:
                    r = i + (1 if "S" in direction else -1 if "N" in direction else 0)
                    d = j + (1 if "E" in direction else -1 if "W" in direction else 0)
                    surroundings[direction] = map_data[r][d], (r, d)
                if any([surroundings[k][0] for k in surroundings]):
                    for direction in rule_order:
                        if not any([surroundings[k][0] for k in surroundings if direction in k]):
                            proposed_moves[surroundings[direction][1]] = \
                                proposed_moves.get(surroundings[direction][1], []) + [(i, j)]
                            del proposed_moves[(i, j)]
                            break

    new_map = [[False] * len(m) for m in map_data]
    for k, v in proposed_moves.items():
        if len(v) > 1:
            for i in v:
                new_map[i[0]][i[1]] = True
        else:
            new_map[k[0]][k[1]] = True

    return new_map


def prune_map(map_data: list[list[bool]]) -> list[list[bool]]:
    new_map = map_data.copy()
    while not any(new_map[0]):
        new_map.pop(0)
    while not any(new_map[-1]):
        new_map.pop()
    while not any(m[0] for m in new_map):
        for i in range(len(new_map)):
            new_map[i] = new_map[i][1:]
    while not any(m[-1] for m in new_map):
        for i in range(len(new_map)):
            new_map[i] = new_map[i][:-1]
    return new_map


def part_1() -> int:
    map_data = load_data()
    rule_order = "NSWE"
    # print("== Initial State ==")
    # dump_map(map_data)
    for i in range(10):
        map_data = pad_map(map_data)
        map_data = make_moves(map_data, rule_order)
        map_data = prune_map(map_data)

        # print(f"\n== End of Round {i + 1} ==")
        # dump_map(map_data)
        # print()

        rule_order = rule_order[1:] + rule_order[0]
    return count_empty(map_data)


def part_2() -> int:
    map_data = load_data()
    prev_map_data = None
    rule_order = "NSWE"
    i = 0
    while prev_map_data != map_data:
        i += 1
        prev_map_data = map_data
        map_data = pad_map(map_data)
        map_data = make_moves(map_data, rule_order)
        map_data = prune_map(map_data)
        rule_order = rule_order[1:] + rule_order[0]
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