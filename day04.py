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


def count_overlaps() -> [int, int]:
    full_overlaps = 0
    partial_overlaps = 0
    for line in get_daily_input(DAY):
        a_start, a_end, b_start, b_end = [int(i) for i in re.split(r"[,-]", line)]
        a_starts_in_b = b_start <= a_start <= b_end
        a_ends_in_b = b_start <= a_end <= b_end
        b_starts_in_a = a_start <= b_start <= a_end
        b_ends_in_a = a_start <= b_end <= a_end
        if a_starts_in_b or a_ends_in_b or b_starts_in_a or b_ends_in_a:
            partial_overlaps += 1
            if (a_starts_in_b and a_ends_in_b) or (b_starts_in_a and b_ends_in_a):
                full_overlaps += 1
    return full_overlaps, partial_overlaps


def main():
    full_overlaps, partial_overlaps = count_overlaps()
    print(f"Part 1: {full_overlaps}")
    print(f"Part 2: {partial_overlaps}")


if __name__ == "__main__":
    main()
