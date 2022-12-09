"""
Advent of Code 2022 Day 9
"""
import sys

from dataclasses import dataclass, field

from advent_tools import get_daily_input

DAY = 9

DEBUG = sys.argv[1] == "debug" if len(sys.argv) > 1 else False

DEBUG_DATA = """
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""

if DEBUG:
    def get_daily_input(_):
        for line in DEBUG_DATA.strip().split("\n"):
            yield line.strip("\n")


@dataclass(frozen=True)
class Coordinate:
    x: int = 0
    y: int = 0

    def adjacent(self, other) -> bool:
        distance = self - other
        return abs(distance.x) <= 1 and abs(distance.y) <= 1

    def __add__(self, other) -> "Coordinate":
        return Coordinate(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other) -> "Coordinate":
        return Coordinate(x=self.x - other.x, y=self.y - other.y)


@dataclass
class Rope:
    num_knots: int = 2

    knot_paths: list[list[Coordinate]] = field(init=False)

    def __post_init__(self):
        self.knot_paths = []
        for k in range(self.num_knots):
            self.knot_paths.append([Coordinate(0,0)])

    @classmethod
    def _trinary(cls, a: int, b: int):
        return 1 if a > b else -1 if a < b else 0

    def move_head(self, offset: Coordinate) -> None:
        self.knot_paths[0].append(self.knot_paths[0][-1] + offset)
        for k in range(1, self.num_knots):
            curr_knot = self.knot_paths[k][-1]
            prev_knot = self.knot_paths[k - 1][-1]
            if not curr_knot.adjacent(prev_knot):
                knot_offset = Coordinate(self._trinary(prev_knot.x, curr_knot.x),
                                         self._trinary(prev_knot.y, curr_knot.y))
                self.knot_paths[k].append(curr_knot + knot_offset)


DIRECTIONS = {
    "R": Coordinate(1, 0),
    "L": Coordinate(-1, 0),
    "U": Coordinate(0, 1),
    "D": Coordinate(0, -1)
}


def part_1() -> int:
    rope = Rope()

    for row in get_daily_input(DAY):
        d, n = row.split(" ")
        for _ in range(int(n)):
            rope.move_head(DIRECTIONS[d])

    return len(set(rope.knot_paths[-1]))


def part_2() -> int:
    rope = Rope(num_knots=10)

    for row in get_daily_input(DAY):
        d, n = row.split(" ")
        for _ in range(int(n)):
            rope.move_head(DIRECTIONS[d])
        pass

    return len(set(rope.knot_paths[-1]))


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
