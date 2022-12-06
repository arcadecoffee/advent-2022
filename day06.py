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


def part_1() -> str:
    result = []
    data = get_daily_input(DAY)
    for line in data:
        for i in range(len(line) - 3):
            if len(set(line[i:i + 4])) == 4:
                result.append(str(i + 4))
                break
    return ", ".join(result)


def part_2() -> int:
    data = get_daily_input(DAY)
    return 0

def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
