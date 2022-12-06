"""
Advent of Code 2022 Day 6
"""
import sys

from advent_tools import get_daily_input

DAY = 6

DEBUG = sys.argv[1] == "debug" if len(sys.argv) > 1 else False

DEBUG_DATA = """
mjqjpqmgbljsphdztnvjfqwrcgsmlb
bvwbjplbgvbhsrlpgdmjqwftvncz
nppdvjthqldpwncqszvftbrmjlhg
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw
"""

if DEBUG:
    def get_daily_input(x):
        for line in DEBUG_DATA.strip().split("\n"):
            yield line.strip()


def find_signal(marker_length: int) -> list[int]:
    result = []
    for data in get_daily_input(DAY):
        for i in range(len(data) - (marker_length - 1)):
            if len(set(data[i:i + marker_length])) == marker_length:
                result.append(i + marker_length)
                break
    return result


def part_1() -> str:
    return ", ".join([str(i) for i in find_signal(4)])


def part_2() -> str:
    return ", ".join([str(i) for i in find_signal(14)])


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
