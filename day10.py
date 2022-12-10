"""
Advent of Code 2022 Day 10
"""
import sys

from advent_tools import get_daily_input

DAY = 10

DEBUG = sys.argv[1] == "debug" if len(sys.argv) > 1 else False

DEBUG_DATA = """
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""

# DEBUG_DATA = """
# noop
# addx 3
# addx -5
# """

if DEBUG:
    def get_daily_input(_):
        for line in DEBUG_DATA.strip().split("\n"):
            yield line.strip("\n")


class CPU:
    registers: dict[str, int] = {"x": 1}
    history: list[dict[str, int]] = [registers.copy()]

    def tick(self, num: int = 1):
        for _ in range(num):
            self.history.append(self.registers.copy())

    def process_instruction(self, instruction: str):
        if instruction == "noop":
            self.tick(1)
        elif instruction.startswith("add"):
            self.tick(2)
            operation, argument = instruction.split(" ")
            self.registers[operation[-1]] += int(argument)


def part_1() -> int:
    cpu = CPU()
    for instruction in get_daily_input(DAY):
        cpu.process_instruction(instruction)
    return sum([(cpu.history[n]["x"] * n) for n in [20, 60, 100, 140, 180, 220]])


def part_2() -> int:
    data = get_daily_input(DAY)
    return len(list(data))


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
