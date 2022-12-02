"""
Advent of Code 2022 Day 1
"""
from advent_tools import get_daily_input


def sum_n_most_calories(number_of_elves: int = 1):
    """
    Find total calories carried by the 'number_of_elves' carrying the most calories
    """
    elves = [0] * number_of_elves
    current_elf = 0
    for line in get_daily_input(1):
        if line == "":
            elves.sort()
            if current_elf > elves[0]:
                elves[0] = current_elf
            current_elf = 0
        else:
            current_elf += int(line)
    return sum(elves)


def part_1() -> int:
    """
    Total calories carried by the elf with the most calories
    """
    return sum_n_most_calories(1)


def part_2() -> int:
    """
    Total calories carried by the three elves with the most calories
    """
    return sum_n_most_calories(3)


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
