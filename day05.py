"""
Advent of Code 2022 Day 5
"""
import copy
import re
import sys

from advent_tools import get_daily_input

DAY = 5

DEBUG = sys.argv[1] == "debug" if len(sys.argv) > 1 else False

DEBUG_DATA = """
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""

if DEBUG:
    def get_daily_input(x):
        for line in DEBUG_DATA[1:].split("\n"):
            yield line.strip("\n")


def process_input() -> tuple[dict, list]:
    stacks = {}
    instructions = []
    input = get_daily_input(DAY)
    for line in input:
        if not line:
            break
        if not line.startswith(" 1"):
            for i in range(1, len(line), 4):
                if not line[i] == " ":
                    stack_number = int(1 + (i - 1) / 4)
                    stacks[stack_number] = [line[i]] + stacks.get(stack_number, [])
    for line in input:
        if line:
            instructions.append([int(i) for i in re.findall(r"\d+", line)])
    return stacks, instructions


def process_instructions(stacks: dict, instructions: list) -> dict:
    stacks = copy.deepcopy(stacks)
    for num, source, destination in instructions:
        for _ in range(num):
            stacks[destination].append(stacks[source].pop())
    return stacks


def process_instructions_v2(stacks: dict, instructions: list) -> dict:
    stacks = copy.deepcopy(stacks)
    for num, source, destination in instructions:
        stacks[destination] += stacks[source][-1 * num:]
        del stacks[source][-1 * num:]
    return stacks


def part_1() -> str:
    start_stack, instructions = process_input()
    end_stack = process_instructions(start_stack, instructions)
    return "".join([end_stack[i][-1] for i in sorted(end_stack.keys())])


def part_2() -> str:
    start_stack, instructions = process_input()
    end_stack = process_instructions_v2(start_stack, instructions)
    return "".join([end_stack[i][-1] for i in sorted(end_stack.keys())])


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
