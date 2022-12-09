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
        return abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1

    def __add__(self, other) -> "Coordinate":
        return Coordinate(x=self.x + other.x, y=self.y + other.y)


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
        def _compare(a: int, b: int):
            return (a > b) - (a < b)

        self.knot_paths[0].append(self.knot_paths[0][-1] + offset)
        for k in range(1, self.num_knots):
            curr_knot = self.knot_paths[k][-1]
            prev_knot = self.knot_paths[k - 1][-1]
            if not curr_knot.adjacent(prev_knot):
                knot_offset = Coordinate(_compare(prev_knot.x, curr_knot.x),
                                         _compare(prev_knot.y, curr_knot.y))
                self.knot_paths[k].append(curr_knot + knot_offset)


def pull_rope(num_knots: int = 2):
    directions = {
        "R": Coordinate(1, 0),
        "L": Coordinate(-1, 0),
        "U": Coordinate(0, 1),
        "D": Coordinate(0, -1)
    }

    rope = Rope(num_knots=num_knots)

    for row in get_daily_input(DAY):
        d, n = row.split(" ")
        for _ in range(int(n)):
            rope.move_head(directions[d])

    return rope


def main():
    rope = pull_rope(num_knots=10)
    print(f"Part 1: {len(set(rope.knot_paths[1]))}")
    print(f"Part 2: {len(set(rope.knot_paths[-1]))}")


if __name__ == "__main__":
    main()
