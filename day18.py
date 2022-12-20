"""
Advent of Code 2022 Day 18
"""
import sys

from advent_tools import get_daily_input

DAY = 18

TEST = sys.argv[1] == "test" if len(sys.argv) > 1 else False

TEST_DATA = """
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""

if TEST:
    def get_daily_input(_):
        for line in TEST_DATA.strip().split("\n"):
            yield line.strip("\n")


class Point:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z
        self.up = self.down = self.left = self.right = self.front = self.back = True

    @property
    def open_sides(self) -> int:
        return sum([self.up, self.down, self.left, self.right, self.front, self.back])

    def __repr__(self):
        return f"{self.x}, {self.y}, {self.z}"


def part_1() -> int:
    points = [Point(*[int(i) for i in s.split(",")]) for s in get_daily_input(DAY)]

    for p_i in range(len(points)):
        p = points[p_i]
        for r_i in range(p_i + 1, len(points)):
            r = points[r_i]
            if p.x == r.x and p.y == r.y and p.z == r.z + 1:
                p.up = r.down = False
            if p.x == r.x and p.y == r.y and p.z == r.z - 1:
                p.down = r.up = False
            if p.x == r.x and p.y == r.y + 1 and p.z == r.z:
                p.left = r.right = False
            if p.x == r.x and p.y == r.y - 1 and p.z == r.z:
                p.right = r.left = False
            if p.x == r.x + 1 and p.y == r.y and p.z == r.z:
                p.front = r.back = False
            if p.x == r.x - 1 and p.y == r.y and p.z == r.z:
                p.back = r.front = False

    return sum(p.open_sides for p in points)


def part_2() -> int:
    points = [tuple(int(i) for i in s.split(",")) for s in get_daily_input(DAY)]

    min_range = min(min(i) for i in points) - 1
    max_range = max(max(i) for i in points) + 2

    faces = 0
    outside_points = [(min_range, min_range, min_range)]
    visited = []
    while outside_points:
        x, y, z = outside_points.pop()
        if (x, y, z) not in visited:
            visited.append((x, y, z))

            for ox, oy, oz in [(x + 1, y, z), (x - 1, y, z),
                               (x, y + 1, z), (x, y - 1, z),
                               (x, y, z + 1), (x, y, z - 1)]:
                if all(min_range <= i <= max_range for i in (ox, oy, oz)):
                    if (ox, oy, oz) in points:
                        faces += 1
                    else:
                        outside_points.append((ox, oy, oz))

    return faces


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
