"""
Advent of Code 2022 Day 11
"""
import sys

from dataclasses import dataclass
from math import prod

from advent_tools import get_daily_input

DAY = 11

DEBUG = sys.argv[1] == "debug" if len(sys.argv) > 1 else False

DEBUG_DATA = """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""

if DEBUG:
    def get_daily_input(_):
        for line in DEBUG_DATA.strip().split("\n"):
            yield line.strip("\n")


@dataclass(kw_only=True)
class Monkey:
    items: list[int]
    operation: str
    test_divisible: int
    if_true: int
    if_false: int
    all_monkeys: list["Monkey"]
    inspected_count: int = 0

    def __post_init__(self):
        self.operation_func = lambda old: eval(self.operation)

    def process_items(self):
        for item in self.items:
            item = self.operation_func(item)
            item = int(item / 3)
            if item % self.test_divisible == 0:
                self.all_monkeys[self.if_true].items.append(item)
            else:
                self.all_monkeys[self.if_false].items.append(item)
            self.inspected_count += 1
        self.items = []


def load_monkeys() -> list[Monkey]:
    monkeys: list[Monkey] = []

    monkey_data: list[str] = [""]
    for line in get_daily_input(DAY):
        if not line:
            monkey_data.append("")
        else:
            monkey_data[-1] += line + "\n"

    for monkey in monkey_data:
        rows = monkey.split("\n")
        items = eval("[" + rows[1].split(": ")[1] + "]")
        operation = rows[2].split(" = ")[1]
        test_divisible = int(rows[3].split(" by ")[1])
        if_true = int(rows[4].split(" monkey ")[1])
        if_false = int(rows[5].split(" monkey ")[1])
        monkeys.append(
            Monkey(
                items=items,
                operation=operation,
                test_divisible=test_divisible,
                if_true=if_true,
                if_false=if_false,
                all_monkeys=monkeys
            )
        )
    
    return monkeys


def part_1() -> int:
    monkeys = load_monkeys()
    
    for _ in range(20):
        for monkey in monkeys:
            monkey.process_items()
    return prod(sorted([m.inspected_count for m in monkeys], reverse=True)[0:2])


def part_2() -> int:
    data = get_daily_input(DAY)
    return len(list(data))


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
