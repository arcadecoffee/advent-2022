"""
Advent of Code 2022 Day 3
"""
from advent_tools import get_daily_input

DAY = 3

DEBUG = False
if DEBUG:
    def get_daily_input(x):
        rows = [
            "vJrwpWtwJgWrhcsFMMfFFhFp",
            "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
            "PmmdzqPrVvPwwTWBwg",
            "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
            "ttgJtRGJQctTZtZT",
            "CrZsJsPPZsGzwwsLwLmpwMDw"
        ]
        for row in rows:
            yield row


def calculate_priority(item: str) -> int:
    return ord(item.lower()) - ord("a") + (27 if item.isupper() else 1)


def part_1() -> int:
    """
    Solve part 1
    """
    total = 0
    for rucksack in get_daily_input(DAY):
        left = rucksack[:int(len(rucksack) / 2)]
        right = rucksack[int(len(rucksack) / 2):]
        for item in left:
            if item in right:
                total += calculate_priority(item)
                break
    return total


def part_2() -> int:
    """
    Solve part 2
    """
    total = 0
    elves = get_daily_input(DAY)
    for elf_a in elves:
        elf_b, elf_c = next(elves), next(elves)
        for item in elf_a:
            if item in elf_b and item in elf_c:
                total += calculate_priority(item)
                break
    return total


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
