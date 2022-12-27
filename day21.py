"""
Advent of Code 2022 Day 21
"""
import sys

from advent_tools import get_daily_input

DAY = 21

TEST = sys.argv[1] == "test" if len(sys.argv) > 1 else False

TEST_DATA = """
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"""

if TEST:
    def get_daily_input(_):
        for line in TEST_DATA.strip().split("\n"):
            yield line.strip("\n")


def load_data() -> dict[str, [str | int]]:
    data = {}
    for line in get_daily_input(DAY):
        name, value = line.split(": ")
        data[name] = int(value) if value.isnumeric() else value
    return data


operations: dict[str, callable] = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a // b,
}


def solve(data: dict[str, [str | int]], key: str) -> int:
    if type(data[key]) == int:
        return data[key]
    else:
        v1, op, v2 = data[key].split(" ")
        return operations[op](solve(data, v1), solve(data, v2))


def part_1() -> int:
    data = load_data()
    r = solve(data, "root")
    return r


def part_2() -> int:
    data = get_daily_input(DAY)
    return len(list(data))


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
