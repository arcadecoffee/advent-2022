"""
Advent of Code 2022 Day 1
"""
from advent_tools import get_daily_input

SESSION_ID = "foo"

def part_1() -> int:
    """
    Total calories carried by the elf with the most calories
    """
    elves = [0]
    for line in get_daily_input(1, SESSION_ID):
        if line == "":
            elves.append(0)
        else:
            elves[-1] += int(line)
    return max(elves)

def part_2() -> int:
    """
    Total calories carried by the three elves with the most calories
    """
    elves = [0]
    for line in get_daily_input(1, SESSION_ID):
        if line == "":
            elves.append(0)
        else:
            elves[-1] += int(line)
    elves.sort(reverse=True)
    return sum(elves[0:3])

print(f"Part 1: {part_1()}")
print(f"Part 2: {part_2()}")
