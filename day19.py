"""
Advent of Code 2022 Day 19
"""
import re
import sys
from copy import deepcopy
from dataclasses import dataclass, field

from advent_tools import get_daily_input

DAY = 19

TEST = sys.argv[1] == "test" if len(sys.argv) > 1 else False

TEST_DATA = """
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
"""

if TEST:
    def get_daily_input(_):
        for line in TEST_DATA.strip().split("\n"):
            yield line.strip("\n")


class Blueprint:
    def __init__(self, input_string: str) -> None:
        vals = [int(i) for i in re.findall(r"\d+", input_string)]
        self.id = vals[0]
        self.cost = {
            "ore": {"ore": vals[1]},
            "clay": {"ore": vals[2]},
            "obsidian": {"ore": vals[3], "clay": vals[4]},
            "geode": {"ore": vals[5], "obsidian": vals[6]}
        }
        self.useful = {
            "ore": max(self.cost["clay"]["ore"], self.cost["obsidian"]["ore"], self.cost["geode"]["ore"]),
            "clay": self.cost["obsidian"]["clay"],
            "obsidian": self.cost["geode"]["obsidian"],
            "geode": float("inf")
        }


class State:
    def __init__(self, robots: dict = None, resources: dict = None, ignored: list = None):
        self.robots = robots.copy() if robots else {
            "ore": 1, "clay": 0, "obsidian": 0, "geode": 0
        }
        self.resources = resources.copy() if resources else {
            "ore": 0, "clay": 0, "obsidian": 0, "geode": 0
        }
        self.ignored = ignored.copy() if ignored else []

    def copy(self) -> "State":
        return State(self.robots, self.resources, self.ignored)

    def __gt__(self, other):
        return self.resources["geode"] > other.resources["geode"]


def evaluate_options(blueprint: Blueprint, prior_states: list[State], timelimit: int = 26) -> [tuple[int, list]]:
    curr_state = prior_states[-1]

    # determine options for what to build in the next state
    options: list[str] = []
    results = []
    if len(prior_states) <= timelimit:
        # look for something affordable and useful and not ignored last time
        for robot, cost in blueprint.cost.items():
            if curr_state.robots[robot] < blueprint.useful[robot] and \
                    all(curr_state.resources[k] >= v for k, v in cost.items()) and \
                    robot not in curr_state.ignored:
                options.append(robot)

        # geodes before anything else, don't bother with other types at the end
        if "geode" in options:
            options = ["geode"]
        elif timelimit - len(prior_states) < 2:
            options = []

        next_state = curr_state.copy()
        for r, n in next_state.robots.items():
            next_state.resources[r] += n

        # the 'do nothing' option
        next_state.ignored += options
        results = [evaluate_options(blueprint, prior_states + [next_state], timelimit)]

        for opt in options:
            next_state_opt = next_state.copy()
            next_state_opt.ignored = []
            next_state_opt.robots[opt] += 1
            for r, n in blueprint.cost[opt].items():
                next_state_opt.resources[r] -= n
            results.append(evaluate_options(blueprint, prior_states + [next_state_opt], timelimit))

        return max(results)

    return prior_states[-1].resources["geode"], prior_states


def part_1() -> int:
    blueprints = [Blueprint(bp) for bp in get_daily_input(DAY)]
    result = 0
    for bp in blueprints:
        r = evaluate_options(bp, [State()], 24)
        result += r[0] * bp.id
    return result


def part_2() -> int:
    blueprints = [Blueprint(bp) for bp in get_daily_input(DAY)]
    result = 0
    for bp in [blueprints[0]]:
        r = evaluate_options(bp, [State()], 32)
        result += r[0] * bp.id
    return result


def main():
    print(f"Part 1: {part_1()}")
    # print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()

"""
Part 1: 1127 is right
"""