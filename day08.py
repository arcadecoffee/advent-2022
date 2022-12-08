"""
Advent of Code 2022 Day 8
"""
import sys

from typing import Iterable, NamedTuple

from advent_tools import get_daily_input

DAY = 8

DEBUG = sys.argv[1] == "debug" if len(sys.argv) > 1 else False

DEBUG_DATA = """
30373
25512
65332
33549
35390
"""

if DEBUG:
    def get_daily_input(x) -> Iterable[str]:
        for line in DEBUG_DATA.strip().split("\n"):
            yield line.strip("\n")


Position = NamedTuple("Position", [("row", int), ("column", int)])


class Forest:
    def __init__(self, data: Iterable[str] = None):
        self.trees = []
        for data_row in data:
            self.trees.append([int(tree) for tree in data_row])

        self.visibility = self.get_visibility()
        self.total_visibility = sum(sum(v) for v in self.visibility)

        self.scores = self.get_scores()
        self.max_score = max(max(s) for s in self.scores)

    def count_visible(self, position: Position, direction: str) -> int:
        count = 0
        for tree in self.look(position, direction):
            count += 1
            if tree >= self.trees[position.row][position.column]:
                break
        return count

    def get_scores(self) -> list[list[int]]:
        scores = [[0] * len(self.trees[0])]
        for row in range(1, len(self.trees) - 1):
            scores.append([0] + [1] * (len(self.trees[row]) - 2) + [0])
            for col in range(1, len(self.trees[row]) - 1):
                position = Position(row, col)
                for d in self.directions:
                    scores[row][col] *= self.count_visible(position, d)
        scores.append([0] * len(self.trees[-1]))
        return scores

    def get_visibility(self) -> list[list[bool]]:
        visibility = [[True] * len(self.trees[0])]
        for row in range(1, len(self.trees) - 1):
            visibility.append([True] + [False] * (len(self.trees[row]) - 2) + [True])
            for col in range(1, len(self.trees[row]) - 1):
                position = Position(row, col)
                visibility[row][col] = self.trees[row][col] > min(
                    [max(self.look(position, d)) for d in self.directions]
                )
        visibility.append([True] * len(self.trees[-1]))
        return visibility

    directions = ["north", "south", "east", "west"]

    def look(self, position: Position, direction: str) -> list[int]:
        if direction == "north":
            return [c[position.column] for c in reversed(self.trees[:position.row])]
        elif direction == "south":
            return [c[position.column] for c in self.trees[position.row + 1:]]
        elif direction == "east":
            return [c for c in self.trees[position.row][position.column + 1:]]
        elif direction == "west":
            return [c for c in reversed(self.trees[position.row][:position.column])]
        else:
            raise ValueError(f"Unknown direction {direction}")


def main():
    forest = Forest(get_daily_input(DAY))
    print(f"Part 1: {forest.total_visibility}")
    print(f"Part 2: {forest.max_score}")


if __name__ == "__main__":
    main()
