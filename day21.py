"""
Advent of Code 2022 Day 21
"""
import re
import sys
from typing import Iterable

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


class MonkeyMathSolver:
    operations: dict[str, callable] = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a // b,
    }

    inverse_right: dict[str, callable] = {
        "+": lambda a, b: a - b,
        "-": lambda a, b: a + b,
        "*": lambda a, b: a // b,
        "/": lambda a, b: a * b,
    }

    inverse_left: dict[str, callable] = {
        "+": lambda a, b: a - b,
        "-": lambda a, b: (a - b) * -1,
        "*": lambda a, b: a // b,
        "/": lambda a, b: b // a,
    }

    def __init__(self, input_data: Iterable[str]):
        self.data: dict[str, [str | int]] = {}
        for line in input_data:
            name, value = line.split(": ")
            self.data[name] = int(value) if value.isnumeric() else value

    def resolve_root(self, data: dict[str, [str | int]] = None,
                     key: str = "root") -> int | str:
        if not data:
            data = self.data
        if type(data[key]) == int:
            return data[key]
        else:
            v1, op, v2 = data[key].split(" ")
            if data.get(v1):
                v1 = self.resolve_root(data, v1)
            if data.get(v2):
                v2 = self.resolve_root(data, v2)
            if type(v1) == int and type(v2) == int:
                return self.operations[op](v1, v2)
            else:
                return f"({v1} {op} {v2})"

    def solve_for(self, key: str = "humn"):
        data = self.data.copy()
        data["root"] = re.sub(r"[+\-*/]", "=", data["root"])
        del (data[key])
        left, right = self.resolve_root(data)[1:-1].split(" = ")

        if left.isnumeric():
            left, right = right, int(left)
        elif right.isnumeric():
            right = int(right)

        while left != key:
            if left.startswith("(") and left.endswith(")"):
                left = left[1:-1]
            elif left.startswith(("(", key)):
                v1, op, v2 = re.search(r"^(.+) ([+\-*/]) (\d+)$", left).groups()
                left = v1
                right = self.inverse_right[op](right, int(v2))
            elif left.endswith((")", key)):
                v1, op, v2 = re.search(r"^(\d+) ([+\-*/]) (.+)$", left).groups()
                left = v2
                right = self.inverse_left[op](right, int(v1))
            else:
                return f"{left} = {right}"

        return right


def part_1() -> int:
    mms = MonkeyMathSolver(get_daily_input(DAY))
    return mms.resolve_root()


def part_2() -> int | str:
    mms = MonkeyMathSolver(get_daily_input(DAY))
    return mms.solve_for()


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
