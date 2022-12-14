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
    def __init__(self, lines: list[Line], sand_origin: Coordinate) -> None:
        top_left_corner = Coordinate(min([p.x for i in lines for p in i.points]), 0)
        adjusted_lines = [i.set_origin(top_left_corner) for i in lines]

        self.sand_origin = sand_origin - top_left_corner
        self.width = max([p.x for i in adjusted_lines for p in i.points]) + 1
        self.height = max([p.y for i in adjusted_lines for p in i.points]) + 1
        self.map: list[list[str]] = []

        for _ in range(self.height):
            self.map.append(["."] * self.width)

        for line in adjusted_lines:
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

    def drop_sand(self, location: Coordinate = None) -> bool:
        location = location if location else self.sand_origin
        if location.y < self.height - 1 and 0 < location.x < self.width:
            if self.vacant(location + Coordinate(0, 1)):
                return self.drop_sand(location + Coordinate(0, 1))
            elif self.vacant(location + Coordinate(-1, 1)):
                return self.drop_sand(location + Coordinate(-1, 1))
            elif self.vacant(location + Coordinate(1, 1)):
                return self.drop_sand(location + Coordinate(1, 1))
            else:
                self.map[location.y][location.x] = "o"
                return True
        return False


def simulate_sand_falling(lines, visualize: bool = False):
    cave_map = CaveMap(lines=lines, sand_origin=Coordinate(500, 0))
    grains = 0
    while cave_map.at(cave_map.sand_origin) == "." and cave_map.drop_sand():
        if visualize:
            os.system("clear")
            print(cave_map)
        grains += 1
    return grains


def part_1() -> int:
    lines = [Line.line_from_text(i) for i in get_daily_input(DAY)]
    return simulate_sand_falling(lines, DEBUG)


def part_2() -> int:
    lines = [Line.line_from_text(i) for i in get_daily_input(DAY)]
    largest_y = max([p.y for i in lines for p in i.points]) + 2
    lines.append(Line([Coordinate(500 - largest_y, largest_y),
                       Coordinate(500 + largest_y, largest_y)]))
    return simulate_sand_falling(lines, DEBUG)


def main():
    print(f"Part 1: {part_1()}")
    if DEBUG:
        input("Press Enter to continue to Part 2")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
