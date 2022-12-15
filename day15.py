"""
Advent of Code 2022 Day 15
"""
import re
import sys

from dataclasses import dataclass

from advent_tools import get_daily_input

DAY = 15

TEST = "test" in sys.argv

TEST_DATA = """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""

if TEST:
    def get_daily_input(_):
        for line in TEST_DATA.strip().split("\n"):
            yield line.strip("\n")


@dataclass
class Sensor:
    sensor_x: int = 0
    sensor_y: int = 0
    beacon_x: int = 0
    beacon_y: int = 0

    @property
    def range(self) -> int:
        return abs(self.sensor_x - self.beacon_x) + abs(self.sensor_y - self.beacon_y)

    def range_at_x(self, x: int) -> tuple[int, int] | None:
        if abs(self.sensor_x - x) <= self.range:
            return (self.sensor_y - (self.range - abs(self.sensor_x - x)),
                    self.sensor_y + (self.range - abs(self.sensor_x - x)))
        else:
            return None

    def range_at_y(self, y: int) -> tuple[int, int] | None:
        if abs(self.sensor_y - y) <= self.range:
            return (self.sensor_x - (self.range - abs(self.sensor_y - y)),
                    self.sensor_x + (self.range - abs(self.sensor_y - y)))
        else:
            return None

    def point_excluded(self, x: int, y: int) -> bool:
        distance = abs(self.sensor_x - x) + abs(self.sensor_y - y)
        return distance <= self.range

    def edge_points(self) -> list[tuple[int, int]]:
        yield self.sensor_x, self.sensor_y + self.range + 1
        yield self.sensor_x, self.sensor_y - self.range - 1
        yield self.sensor_x + self.range + 1, self.sensor_y
        yield self.sensor_x - self.range - 1, self.sensor_y
        for i in range(1, self.range + 1):
            width = self.range - i
            yield self.sensor_x - width - 1, self.sensor_y + i
            yield self.sensor_x + width + 1, self.sensor_y + i
            yield self.sensor_x - width - 1, self.sensor_y - i
            yield self.sensor_x + width + 1, self.sensor_y - i


def load_input() -> list[Sensor]:
    sensors: [Sensor] = []
    for data in get_daily_input(DAY):
        s = re.split(r"[=,:]", data)
        sensors.append(Sensor(*[int(s[i]) for i in [1, 3, 5, 7]]))
    return sensors


def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    ranges = ranges.copy()
    go_again = True
    while go_again:
        go_again = False
        curr_range = ranges.pop()
        next_ranges = []
        for curr_raw_range in ranges:
            if curr_range[0] - 1 <= curr_raw_range[0] <= curr_range[1] + 1 or \
                    curr_range[0] - 1 <= curr_raw_range[1] <= curr_range[1] + 1 or \
                    curr_raw_range[0] - 1 <= curr_range[0] <= curr_raw_range[1] + 1 or \
                    curr_raw_range[0] - 1 <= curr_range[1] <= curr_raw_range[1] + 1:
                curr_range = (min([curr_range[0], curr_raw_range[0]]),
                              max([curr_range[1], curr_raw_range[1]]))
                go_again = True
            else:
                next_ranges.append(curr_raw_range)
        ranges = [curr_range] + next_ranges
    return ranges


def part_1() -> int:
    sensors = load_input()
    target = 10 if TEST else 2000000
    ranges = [r for r in [s.range_at_y(target) for s in sensors] if r]
    merged_ranges = merge_ranges(ranges)
    return sum([abs(r[0] - r[1]) for r in merged_ranges])


def part_2_edge_scan() -> int:
    sensors = load_input()
    max_target = 20 if TEST else 4000000
    for sensor in sensors:
        for p in sensor.edge_points():
            if 0 <= p[0] <= max_target and 0 <= p[1] <= max_target:
                if True not in [s.point_excluded(*p) for s in sensors]:
                    return p[0] * 4000000 + p[1]
    return 0


def part_2() -> int:
    sensors = load_input()
    max_target = 20 if TEST else 4000000
    for y in range(max_target + 1):
        x_ranges = merge_ranges([r for r in [s.range_at_y(y) for s in sensors] if r])
        if len(x_ranges) > 1:
            for i in range(len(x_ranges) - 1):
                return ((sorted(x_ranges)[i][1] + 1) * 4000000) + y
    return 0


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
