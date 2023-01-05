"""
Advent of Code 2022 Day 25
"""
import sys

from advent_tools import get_daily_input

DAY = 25

TEST = sys.argv[1] == "test" if len(sys.argv) > 1 else False

TEST_DATA = """
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
"""

if TEST:
    def get_daily_input(_):
        for line in TEST_DATA.strip().split("\n"):
            yield line.strip("\n")


class SnafuNumber:
    def __init__(self, val: str = None):
        self.val = val or "0"

    def __add__(self, other: "SnafuNumber") -> "SnafuNumber":
        dv = int(self.base_5, 5) + int(other.base_5, 5)
        rv = ""
        while dv:
            rv += str(dv % 5)
            dv = dv // 5
        return SnafuNumber.from_base_5(rv[::-1])

    @property
    def base_5(self) -> str:
        result = ""
        carry = 0
        for v in map(self.sd_to_dd, self.val[::-1]):
            v -= carry
            carry = 1 if v < 0 else 0
            result += str(v + (5 if v < 0 else 0))
        return "".join((map(str, result[::-1]))).lstrip("0") or "0"

    @classmethod
    def from_base_5(cls, value: str) -> "SnafuNumber":
        sn = []
        carry = 0
        for v in [int(i) for i in reversed(value)]:
            nv = v + carry
            carry = 1 if nv > 2 else 0
            sn.append(cls.dd_to_sd(nv - (5 if nv > 2 else 0)))
        sn.append(str(carry))
        return SnafuNumber("".join(map(str, sn[::-1])).lstrip("0"))

    @classmethod
    def sd_to_dd(cls, v: str) -> int:
        return -1 if v == "-" else -2 if v == "=" else int(v)

    @classmethod
    def dd_to_sd(cls, v: int) -> str:
        return "-" if v == -1 else "=" if v == -2 else str(v)


def part_1() -> str:
    return sum(map(SnafuNumber, get_daily_input(DAY)), SnafuNumber()).val


def main():
    print(f"Part 1: {part_1()}")


if __name__ == "__main__":
    main()
