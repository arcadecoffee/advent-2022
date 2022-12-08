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
    visibility = []
    for row in range(len(forest)):
        visibility.append([False] * len(forest[row]))
        for col in range(len(forest[row])):
            if row in (0, len(forest) - 1) or col in (0, len(forest[row]) - 1):
                visibility[row][col] = True
            else:
                north = max([c[col] for c in forest[:row]])
                south = max([c[col] for c in forest[row + 1:]])
                east = max([c for c in forest[row][col + 1:]])
                west = max([c for c in forest[row][:col]])
                visibility[row][col] = min(north, south, east, west) < forest[row][col]
    return visibility


def part_1() -> int:
    total = 0
    for f in get_visibility(load_forest()):
        total += sum(f)
    return total


def part_2() -> int:
    data = get_daily_input(DAY)
    return 0

def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
