"""
Advent of Code 2022 Day 15
"""
import re
import sys

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


class Sensor:
    def __init__(
            self,
            sensor_x: int = 0,
            sensor_y: int = 0,
            beacon_x: int = 0,
            beacon_y: int = 0
    ) -> None:
        self.sensor_x = sensor_x
        self.sensor_y = sensor_y
        self.beacon_x = beacon_x
        self.beacon_y = beacon_y
        self.range = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)

    def range_at_y(self, y: int) -> tuple[int, int] | None:
        if abs(self.sensor_y - y) <= self.range:
            return (self.sensor_x - (self.range - abs(self.sensor_y - y)),
                    self.sensor_x + (self.range - abs(self.sensor_y - y)))
        else:
            return None


def load_input() -> list[Sensor]:
    sensors: [Sensor] = []
    for data in get_daily_input(DAY):
        s = re.split(r"[=,:]", data)
        sensors.append(Sensor(*[int(s[i]) for i in [1, 3, 5, 7]]))
    return sensors


def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    merged = [sorted(ranges)[0]]
    for start, end in sorted(ranges)[1:]:
        if merged[-1][1] >= start - 1:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return merged


def part_1() -> int:
    sensors = load_input()
    target = 10 if TEST else 2000000
    ranges = [r for r in [s.range_at_y(target) for s in sensors] if r]
    merged_ranges = merge_ranges(ranges)
    return sum([abs(r[0] - r[1]) for r in merged_ranges])


def part_2() -> int:
    sensors = load_input()
    max_target = 20 if TEST else 4000000
    for y in range(max_target + 1):
        x_ranges = merge_ranges([r for r in [s.range_at_y(y) for s in sensors] if r])
        if len(x_ranges) > 1:
            x = sorted(x_ranges)[0][1] + 1
            return x * 4000000 + y
    return 0


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
