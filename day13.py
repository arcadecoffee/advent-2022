"""
Advent of Code 2022 Day 13
"""
import sys

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
    for i in range(len(left)):
        if i >= len(right):
            return False
        l_val = left[i]
        r_val = right[i]
        if type(l_val) == int and type(r_val) == int:
            if l_val != r_val:
                return l_val < r_val
        else:
            l_val = l_val if type(l_val) == list else [l_val]
            r_val = r_val if type(r_val) == list else [r_val]
            compare_left = compare(l_val, r_val)
            compare_right = compare(r_val, l_val)
            if compare_left != compare_right:
                return compare_left
    return True


def part_1() -> int:
    data = get_daily_input(DAY)
    pairs: list[dict] = []
    for left in data:
        if left:
            pairs.append({"left": eval(left), "right": eval(next(data))})

    sum_of_indicies = 0
    for i in range(len(pairs)):
        vals = pairs[i]
        vals["valid"] = compare(vals["left"], vals["right"])
        sum_of_indicies += abs(vals["valid"] * (i + 1))

    return sum_of_indicies


def part_2() -> int:
    data = get_daily_input(DAY)
    return len(list(data))


def main():
    print(f"Part 1: {part_1()}")
    # print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
