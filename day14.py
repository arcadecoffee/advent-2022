"""
Advent of Code 2022 Day 14
"""
import os
import sys

from dataclasses import dataclass, field

from advent_tools import get_daily_input

DAY = 14

DEBUG = sys.argv[1] == "debug" if len(sys.argv) > 1 else False

DEBUG_DATA = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""

if DEBUG:
    def get_daily_input(_):
        for line in DEBUG_DATA.strip().split("\n"):
            yield line.strip("\n")


@dataclass
class Coordinate:
    x: int = 0
    y: int = 0

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other) -> "Coordinate":
        return Coordinate(self.x - other.x, self.y - other.y)


@dataclass
class Line:
    points: list[Coordinate] = field(default_factory=list)

    @property
    def num_points(self) -> int:
        return len(self.points)

    @property
    def point_pairs(self) -> list[tuple[Coordinate, ...]]:
        return [tuple(self.points[i:i + 2]) for i in range(self.num_points - 1)]

    def set_origin(self, top_left_corner: Coordinate) -> "Line":
        return Line(points = [p - top_left_corner for p in self.points])

    @classmethod
    def line_from_text(cls, input: str) -> "Line":
        line = Line()
        for point in input.split(" -> "):
            x, y = [int(n) for n in point.split(",")]
            line.points.append(Coordinate(x, y))
        return line


class CaveMap:
    def __init__(self, width: int, height: int, lines: list[Line]) -> None:
        self.map: list[list[str]] = []
        for _ in range(height):
            self.map.append(["."] * width)

        for line in lines:
            self.draw_line(line)

    def __repr__(self) -> str:
        return "\n".join(["".join(r) for r in self.map])

    def draw_line(self, line: Line) -> None:
        for start, end in line.point_pairs:
            increment = 1 if start.x < end.x or start.y < end.y else -1
            if start.x != end.x:
                for i in range(start.x, end.x + increment, increment):
                    self.map[start.y][i] = "#"
            else:
                for i in range(start.y, end.y + increment,  increment):
                    self.map[i][start.x] = "#"

    def at(self, coordinate: Coordinate) -> str:
        return self.map[coordinate.y][coordinate.x]

    def vacant(self, coordinate: Coordinate) -> bool:
        return self.at(coordinate) == "."

    def drop_sand(self, location: Coordinate) -> Coordinate | None:
        if location.y >= len(self.map) - 1:
            return None
        elif self.vacant(location + Coordinate(0, 1)):
            return self.drop_sand(location + Coordinate(0, 1))
        elif location.x == 0:
            return None
        elif self.vacant(location + Coordinate(-1, 1)):
            return self.drop_sand(location + Coordinate(-1, 1))
        elif location.x >= len(self.map[0]):
            return None
        elif self.vacant(location + Coordinate(1, 1)):
            return self.drop_sand(location + Coordinate(1, 1))
        else:
            self.map[location.y][location.x] = "o"
            return location


def part_1() -> int:
    lines = [Line.line_from_text(i) for i in get_daily_input(DAY)]
    top_left_corner = Coordinate(min([p.x for i in lines for p in i.points]), 0)
    sand_origin = Coordinate(500, 0) - top_left_corner
    lines = [i.set_origin(top_left_corner) for i in lines]
    cave_map = CaveMap(width=max([p.x for i in lines for p in i.points]) + 1,
                       height=max([p.y for i in lines for p in i.points]) + 1,
                       lines=lines)

    grains = 0
    while cave_map.drop_sand(sand_origin):
        grains += 1
    return grains


def part_2() -> int:
    data = get_daily_input(DAY)
    return len(list(data))


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
