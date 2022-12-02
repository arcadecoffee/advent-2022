"""
Advent of Code 2022 Day 1
"""
from advent_tools import get_daily_input

DAY = 2


def calculate_score(a: str, b: str) -> int:
    """
    Calculate tournament score with Part 1 strategy
    """
    win_loss_values = {
        "rock": {"rock": 3, "paper": 6, "scissors": 0},
        "paper": {"rock": 0, "paper": 3, "scissors": 6},
        "scissors": {"rock": 6, "paper": 0, "scissors": 3}
    }

    move_played_values = {"rock": 1, "paper": 2, "scissors": 3}

    return win_loss_values[a][b] + move_played_values[b]


def part_1() -> int:
    """
    Solve part 1
    """
    translation = ["rock", "paper", "scissors"]

    total_score = 0
    for line in get_daily_input(DAY):
        a, b = line.split(" ")
        total_score += calculate_score(
            translation[ord(a) - ord("A")], translation[ord(b) - ord("X")]
        )

    return total_score


def part_2() -> int:
    """
    Solve part 2
    """
    move_translation = ["rock", "paper", "scissors"]
    outcome_translation = [-1, 0, 1]

    total_score = 0
    for line in get_daily_input(DAY):
        a, b = line.split(" ")
        a_move = ord(a) - ord("A")
        b_move = a_move + outcome_translation[ord(b) - ord("X")]
        if b_move > 2:
            b_move = 0

        total_score += calculate_score(
            move_translation[a_move], move_translation[b_move]
        )

    return total_score


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
