"""
Advent of Code 2022 Day 4
"""
import re
import sys

from advent_tools import get_daily_input

DAY = 4

DEBUG = sys.argv[1] == "debug" if len(sys.argv) > 1 else False

DEBUG_DATA = """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""

if DEBUG:
    def get_daily_input(x):
        for line in DEBUG_DATA.strip().split("\n"):
            yield line.strip()


def part_1() -> int:
    """
    Solve part 1
    """
    total = 0
    for line in get_daily_input(DAY):
        sections = [int(i) for i in  re.split(r"[,-]", line)]
        if (sections[0] <= sections[2] and sections[1] >= sections[3]) or \
                (sections[0] >= sections[2] and sections[1] <= sections[3]):
            total += 1
    return total


def part_2() -> int:
    """
    Solve part 2
    """
    total = 0
    return total


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
