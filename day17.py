"""
Advent of Code 2022 Day 0
"""
import itertools
import re
import sys

from itertools import cycle
from typing import Iterable

from advent_tools import get_daily_input

DAY = 17

TEST = sys.argv[1] == "test" if len(sys.argv) > 1 else False

TEST_DATA = """
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
"""

if TEST:
    def get_daily_input(_):
        for line in TEST_DATA.strip().split("\n"):
            yield line.strip("\n")


def jet_stream() -> Iterable[str]:
    data = next(get_daily_input(DAY))
    while True:
        for c in data:
            yield c


class Shaft:
    shapes = {
        "line": [
            "..@@@@.",
        ],
        "cross": [
            "...@...",
            "..@@@..",
            "...@...",
        ],
        "elbow": [
            "....@..",
            "....@..",
            "..@@@..",
        ],
        "column": [
            "..@....",
            "..@....",
            "..@....",
            "..@....",
        ],
        "square": [
            "..@@...",
            "..@@...",
        ]
    }

    def __init__(self):
        self.shaft: list[list[str]] = []
        self.jet = jet_stream()

    @property
    def shaft_height(self) -> int:
        return len(self.shaft)

    def drop(self, shape: str):
        self.shaft = self.shapes[shape] + \
            [
                ".......",
                ".......",
                ".......",
            ] + self.shaft

        while True:
            shape_rows = [i for i in range(self.shaft_height) if "@" in self.shaft[i]]
            gust = next(self.jet)
            if gust == "<" and all(".@" in self.shaft[r] for r in shape_rows):
                for r in shape_rows:
                    s = re.search(r"([^@]*)\.(@+)([^@]*)", self.shaft[r])
                    self.shaft[r] = s.group(1) + s.group(2) + "." + s.group(3)
            elif gust == ">" and all("@." in self.shaft[r] for r in shape_rows):
                for r in shape_rows:
                    s = re.search(r"([^@]*)(@+)\.([^@]*)", self.shaft[r])
                    self.shaft[r] = s.group(1) + "." + s.group(2) + s.group(3)
            if max(shape_rows) < self.shaft_height - 1:
                can_fall = True
                for i in shape_rows:
                    for j in range(7):
                        if self.shaft[i][j] == "@" and self.shaft[i + 1][j] == "#":
                            can_fall = False
                if can_fall:
                    for i in reversed(shape_rows):
                        for j in range(7):
                            if self.shaft[i][j] == "@":
                                self.shaft[i + 1] = self.shaft[i + 1][:j] + "@" + self.shaft[i + 1][j + 1:]
                                new_row = list(self.shaft[i])
                                new_row[j] = "." if i == 0 else self.shaft[i - 1][j]
                                self.shaft[i] = "".join(new_row)
                    if self.shaft[0] == ".......":
                        self.shaft.pop(0)
                else:
                    break
            else:
                break
        for i in shape_rows:
            self.shaft[i] = self.shaft[i].replace("@", "#")


def part_1() -> int:
    shaft = Shaft()

    shape = itertools.cycle(Shaft.shapes)
    for i in range(13):
        shaft.drop(next(shape))
        print(shaft.shaft_height)


    shaft.drop(next(shape))


    return shaft.shaft_height


def part_2() -> int:
    data = get_daily_input(DAY)
    return len(list(data))


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
