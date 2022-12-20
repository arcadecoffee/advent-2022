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


class RockPile:

    rock_shapes = {
        "line": [
            "0011110",
        ],
        "cross": [
            "0001000",
            "0011100",
            "0001000",
        ],
        "elbow": [
            "0000100",
            "0000100",
            "0011100",
        ],
        "column": [
            "0010000",
            "0010000",
            "0010000",
            "0010000",
        ],
        "square": [
            "0011000",
            "0011000",
        ]
    }

    def __init__(self, wind_directions: str):
        self.wind_direction = cycle(wind_directions)
        self.rock_shape = cycle(self.rock_shapes)
        self.pile: list[int] = []

    @property
    def height(self) -> int:
        return len(self.pile)

    def drop_next(self) -> None:
        rock = [int(i, 2) for i in self.rock_shapes[next(self.rock_shape)]]
        self.pile = [0] * (3 + len(rock)) + self.pile
        for s in range(len(self.pile)):
            direction = next(self.wind_direction)
            if direction == ">":
                can_shift = True
                for r in range(len(rock)):
                    if (rock[r] & 1) or (rock[r] >> 1 & self.pile[s + r]):
                        can_shift = False
                        break
                if can_shift:
                    for r in range(len(rock)):
                        rock[r] = rock[r] >> 1
            elif direction == "<":
                can_shift = True
                for r in range(len(rock)):
                    if (rock[r] & 2**6) or (rock[r] << 1 & self.pile[s + r]):
                        can_shift = False
                        break
                if can_shift:
                    for r in range(len(rock)):
                        rock[r] = rock[r] << 1

            can_fall = True
            for r in range(len(rock)):
                if (s + r >= len(self.pile) - 1) or (rock[r] & self.pile[s + r + 1]):
                    can_fall = False
                    break
            if not can_fall:
                for r in range(len(rock)):
                    self.pile[s + r] = self.pile[s + r] | rock[r]
                break
        while self.pile[0] == 0:
            self.pile.pop(0)

    def dump(self) -> str:
        output = ""
        for r in self.pile:
            output += "|" + \
                      "".join(["#" if c == "1" else "." for c in format(r, "07b")]) + \
                      "|\n"
        output += "+-------+"
        return output


def find_pattern(data: list[int]) -> tuple[list[int], list[int]]:
    for i in range(len(data)):
        h = data[i:]
        for x in range(2, len(h) // 2):
            if h[0:x] == h[x:2 * x]:
                pass
                if all([(h[0:x] == h[y:y + x]) for y in range(x, len(h) - x, x)]):
                    return data[:i], data[i:i + x]
            else:
                x += 1
    return [], []


def part_1() -> int:
    pile = RockPile(next(get_daily_input(DAY)))
    for _ in range(2022):
        pile.drop_next()
    return pile.height


def part_2() -> int:
    num_rocks = 1000000000000
    sample_size = 10000

    pile = RockPile(next(get_daily_input(DAY)))

    height_deltas = []
    for _ in range(sample_size):
        prev_height = pile.height
        pile.drop_next()
        height_deltas.append(pile.height - prev_height)

    preamble, repetition = find_pattern(height_deltas)
    p_len = len(preamble)
    r_len = len(repetition)

    return sum(preamble) \
        + sum(repetition) * ((num_rocks - p_len) // r_len) \
        + sum(repetition[:((num_rocks - p_len) % r_len)])


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
