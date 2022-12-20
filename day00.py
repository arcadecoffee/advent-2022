"""
Advent of Code 2022 Day 0
"""
import sys

from advent_tools import get_daily_input

DAY = 0

TEST = sys.argv[1] == "test" if len(sys.argv) > 1 else False

TEST_DATA = """
"""

if TEST:
    def get_daily_input(_):
        for line in TEST_DATA.strip().split("\n"):
            yield line.strip("\n")


def part_1() -> int:
    data = get_daily_input(DAY)
    return len(list(data))


def part_2() -> int:
    data = get_daily_input(DAY)
    return len(list(data))


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
