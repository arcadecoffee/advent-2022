"""
Advent of Code 2022 Day 0
"""
import re
import sys

from copy import deepcopy
from itertools import cycle

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

empty_line = "......."


class Shaft:
    def __init__(self):
        self.jet = cycle(next(get_daily_input(DAY)))
        self.rock_shape = cycle(shapes)
        self.shaft = []

    def drop_rock(self):
        rock = next(self.rock_shape)
        self.shaft = [empty_line] + shapes[rock] + [empty_line] * 3 + self.shaft
        rock_rows = list(range(1, len(shapes[rock]) + 1))
        while True:
            jet_dir = next(self.jet)
            if jet_dir == ">":
                if all("@." in self.shaft[r] for r in rock_rows):
                    for r in rock_rows:
                        self.shaft[r] = self.shaft[r].replace("@.", "@@")
                        self.shaft[r] = re.sub(r"([^@])@|^@", r"\1.", self.shaft[r])
            elif jet_dir == "<":
                if all(".@" in self.shaft[r] for r in rock_rows):
                    for r in rock_rows:
                        self.shaft[r] = self.shaft[r].replace(".@", "@@")
                        self.shaft[r] = re.sub(r"@([^@])|@$", r".\1", self.shaft[r])

            can_fall = True
            for r in rock_rows:
                for i in range(7):
                    if self.shaft[r][i] == "@" and \
                            (r + 1 >= len(self.shaft) or
                             self.shaft[r + 1][i] == "#"):
                        can_fall = False
            if can_fall:
                for r in reversed(rock_rows):
                    for i in range(7):
                        if self.shaft[r][i] == "@":
                            self.shaft[r + 1] = self.shaft[r + 1][:i] + \
                                                self.shaft[r][i] + \
                                                self.shaft[r + 1][i + 1:]
                            if self.shaft[r - 1][i] != "#":
                                self.shaft[r] = self.shaft[r][:i] + \
                                                self.shaft[r - 1][i] + \
                                                self.shaft[r][i + 1:]
                            else:
                                if self.shaft[r - 1][i] != "#":
                                    self.shaft[r] = self.shaft[r][:i] + \
                                                    "." + \
                                                    self.shaft[r][i + 1:]
                rock_rows = [r + 1 for r in rock_rows]
            else:
                break

        while self.shaft[0] == empty_line:
            self.shaft.pop(0)

        for i in range(len(self.shaft)):
            self.shaft[i] = self.shaft[i].replace("@", "#")


def part_1() -> int:
    s = Shaft()
    for _ in range(6):
        s.drop_rock()
    for _ in s.shaft:
        print(_)
    s.drop_rock()
    return len(s.shaft)


def part_2() -> int:
    data = get_daily_input(DAY)
    return len(list(data))


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
