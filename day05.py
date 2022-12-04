"""
Advent of Code 2022 Day 5
"""
import sys

from advent_tools import get_daily_input

DAY = 5

DEBUG = sys.argv[1] == "debug" if len(sys.argv) > 1 else False

DEBUG_DATA = """
"""

if DEBUG:
    def get_daily_input(x):
        for line in DEBUG_DATA.strip().split("\n"):
            yield line.strip()


def part_1() -> int:
    data = get_daily_input(DAY)
    return 0


def part_2() -> int:
    data = get_daily_input(DAY)
    return 0

def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
