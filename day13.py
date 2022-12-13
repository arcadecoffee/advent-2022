"""
Advent of Code 2022 Day 13
"""
import sys

from functools import cmp_to_key
from math import prod

from advent_tools import get_daily_input

DAY = 13

DEBUG = sys.argv[1] == "debug" if len(sys.argv) > 1 else False

DEBUG_DATA = """
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""

if DEBUG:
    def get_daily_input(_):
        for line in DEBUG_DATA.strip().split("\n"):
            yield line.strip("\n")


def compare(left: list, right: list) -> int:
    if left == right:
        return 0
    elif not left:
        return -1
    for i in range(len(left)):
        if i >= len(right):
            return 1
        if left[i] != right[i]:
            if type(left[i]) == int and type(right[i]) == int:
                if left[i] < right[i]:
                    return -1
                elif left[i] > right[i]:
                    return 1
            else:
                cmp = compare(left[i] if type(left[i]) == list else [left[i]],
                              right[i] if type(right[i]) == list else [right[i]])
                if cmp != 0:
                    return cmp
    return -1


def part_1() -> int:
    data = get_daily_input(DAY)
    pairs: list[dict] = []
    for left in data:
        if left:
            pairs.append({"left": eval(left), "right": eval(next(data))})

    sum_of_indicies = 0
    for i in range(len(pairs)):
        sum_of_indicies += (compare(pairs[i]["left"], pairs[i]["right"]) < 1) * (i + 1)

    return sum_of_indicies


def part_2() -> int:
    targets = [[[2]], [[6]]]
    data = targets.copy() + [eval(row) for row in get_daily_input(DAY) if row]
    data.sort(key=cmp_to_key(compare))
    return prod([(data.index(t) + 1) for t in targets])


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
