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


def part_1() -> int:
    points = [Point(*[int(i) for i in s.split(",")]) for s in get_daily_input(DAY)]

    total_sides = len(points) * 6

    for p_i in range(len(points)):
        p = points[p_i]
        for r_i in range(p_i + 1, len(points)):
            r = points[r_i]
            total_sides -= 2 * sum([
                p.x == r.x and p.y == r.y and p.z == r.z + 1,
                p.x == r.x and p.y == r.y and p.z == r.z - 1,
                p.x == r.x and p.y == r.y + 1 and p.z == r.z,
                p.x == r.x and p.y == r.y - 1 and p.z == r.z,
                p.x == r.x + 1 and p.y == r.y and p.z == r.z,
                p.x == r.x - 1 and p.y == r.y and p.z == r.z,
            ])

    return total_sides


def part_2() -> int:
    data = get_daily_input(DAY)
    return len(list(data))


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
