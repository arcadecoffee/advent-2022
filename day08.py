"""
Advent of Code 2022 Day 8
"""
from collections import namedtuple
import sys

from advent_tools import get_daily_input

DAY = 8

DEBUG = sys.argv[1] == "debug" if len(sys.argv) > 1 else False

DEBUG_DATA = """
30373
25512
65332
33549
35390
"""

if DEBUG:
    def get_daily_input(x):
        for line in DEBUG_DATA.strip().split("\n"):
            yield line.strip("\n")


def load_forest() -> list[list[int]]:
    forest = []
    for input_row in get_daily_input(DAY):
        tree_row = [int(height) for height in input_row]
        forest.append(tree_row)
    return forest


def get_visibility(forest: list[list[int]]) -> list[list[bool]]:
    visibility = [[True] * len(forest[0])]
    for row in range(1, len(forest) - 1):
        visibility.append([True] + [False] * (len(forest[row]) - 2) + [True])
        for col in range(1, len(forest[row]) - 1):
            visibility[row][col] = \
                max([c[col] for c in forest[:row]]) < forest[row][col] or \
                max([c[col] for c in forest[row + 1:]]) < forest[row][col] or \
                max([c for c in forest[row][col + 1:]]) < forest[row][col] or \
                max([c for c in forest[row][:col]]) < forest[row][col]
    visibility.append([True] * len(forest[0]))
    return visibility


def part_1() -> int:
    visibility = get_visibility(load_forest())
    return sum(sum(v) for v in visibility)


def part_2() -> int:
    data = get_daily_input(DAY)
    return 0

def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
