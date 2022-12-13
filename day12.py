"""
Advent of Code 2022 Day 12
"""
import sys

from dataclasses import dataclass, field
from itertools import product
from typing import Iterable

from advent_tools import get_daily_input

DAY = 12

DEBUG = sys.argv[1] == "debug" if len(sys.argv) > 1 else False

DEBUG_DATA = """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""

if DEBUG:
    def get_daily_input(_):
        for line in DEBUG_DATA.strip().split("\n"):
            yield line.strip("\n")


@dataclass
class Coordinate:
    x: int
    y: int


@dataclass
class MapPoint:
    height: int
    visited: bool = False
    cost_to_reach: int = None
    previous_point: Coordinate = None


@dataclass
class HeightMap:
    start: Coordinate = None
    end: Coordinate = None
    points: list[list[MapPoint]] = field(default_factory=list)

    def reachable_points(self, origin: Coordinate) -> Iterable[Coordinate]:

        possible_moves = [
            Coordinate(x, y) for (x, y) in [
                (origin.x - 1, origin.y), (origin.x + 1, origin.y),
                (origin.x, origin.y - 1), (origin.x, origin.y + 1)
            ] if 0 <= x < len(self.points[0]) and 0 <= y < len(self.points)
        ]
        max_height = self.points[origin.y][origin.x].height + 1

        for point in possible_moves:
            if self.point_at(point).height <= max_height:
                yield point

    def point_at(self, coordinate: Coordinate):
        return self.points[coordinate.y][coordinate.x]

    def walk(self, queue: list[tuple[int, Coordinate, Coordinate]] = None) -> None:
        if not queue:
            queue = [(0, self.start, self.start)]
        while queue:
            curr_cost, curr_point, prev_point = queue.pop(0)
            if not self.point_at(curr_point).visited:
                self.point_at(curr_point).cost_to_reach = curr_cost
                self.point_at(curr_point).visited = True
                self.point_at(curr_point).previous_point = prev_point
                if curr_point == self.end:
                    break
                else:
                    curr_cost += 1
                    for next_point in self.reachable_points(curr_point):
                        queue.append((curr_cost, next_point, curr_point))
                    queue.sort(key=lambda l: l[0])


def load_map() -> HeightMap:
    height_map = HeightMap()
    for row in get_daily_input(DAY):
        height_map.points.append([])
        for point in row:
            if point == "S":
                height_map.start = Coordinate(
                    x=len(height_map.points[-1]),
                    y=len(height_map.points) - 1
                )
                point = "a"
            elif point == "E":
                height_map.end = Coordinate(
                    x=len(height_map.points[-1]),
                    y=len(height_map.points) - 1
                )
                point = "z"
            height_map.points[-1].append(MapPoint(height=ord(point) - ord("a")))
    return height_map


def part_1() -> int:
    m = load_map()
    m.walk()
    return m.point_at(m.end).cost_to_reach


def part_2() -> int:
    m = load_map()
    queue = []
    for (x, y) in product(range(len(m.points[0])), range(len(m.points))):
        coord = Coordinate(x, y)
        if m.point_at(coord).height == 0:
            queue.append((0, coord, coord))
    m.walk(queue=queue)
    return m.point_at(m.end).cost_to_reach


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
