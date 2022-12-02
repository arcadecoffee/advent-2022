"""
Advent of Code 2022 Day 1
"""
from advent_tools import get_daily_input

DAY = 2


def calculate_score() -> int:
    """
    Calculate tournament score with Part 1 strategy
    """
    win_loss_values = {
        "A": {"X": 3, "Y": 6, "Z": 0},
        "B": {"X": 0, "Y": 3, "Z": 6},
        "C": {"X": 6, "Y": 0, "Z": 3}
    }

    move_played_values = {"X": 1, "Y": 2, "Z": 3}

    total_score = 0
    for line in get_daily_input(DAY):
        opponent, me = line.split(" ")
        total_score += win_loss_values[opponent][me] + move_played_values[me]

    return total_score

def part_1() -> int:
    """
    Total calories carried by the elf with the most calories
    """
    return calculate_score()


def part_2() -> int:
    """
    Total calories carried by the three elves with the most calories
    """
    return 0


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
