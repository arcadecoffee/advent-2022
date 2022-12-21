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


@dataclass(eq=True, frozen=True)
class Robot:
    type: str = None
    cost: dict[str, int] = field(default_factory=dict)

    def can_build(self, resources: dict[str, int]) -> bool:
        return all(self.cost[r] <= resources[r] for r in self.cost)

    def __hash__(self):
        return hash(("type", self.type) + tuple(sorted(self.cost.items())))

@dataclass
class RobotSet:
    ore: Robot
    clay: Robot
    obsidian: Robot
    geode: Robot
    none: Robot = Robot("none")

    @property
    def all(self) -> list[Robot]:
        return [self.ore, self.clay, self.obsidian, self.geode, self.none]


@dataclass
class Blueprint:
    id: int
    robots: RobotSet

    def max_cost(self, resource: str) -> int:
        return max([r.cost.get(resource, 0) for r in self.robots.all if r.type != resource])

    @classmethod
    def create_from_input(cls, input_string: str) -> "Blueprint":
        vals = [int(i) for i in re.findall(r"\d+", input_string)]
        return Blueprint(
            id=vals[0],
            robots=RobotSet(
                ore=Robot(type="ore", cost={"ore": vals[1]}),
                clay=Robot(type="clay", cost={"ore": vals[2]}),
                obsidian=Robot(type="obsidian", cost={"ore": vals[3], "clay": vals[4]}),
                geode=Robot(type="geode", cost={"ore": vals[5], "obsidian": vals[6]})
            )
        )


class Simulation:
    def __init__(self, blueprint: Blueprint, turn: int = 0, turn_limit: int = 24):
        self.blueprint = blueprint
        self.turn = turn
        self.turn_limit = turn_limit

        self.resources: dict[str, int] = {
            "ore": 0, "clay": 0, "obsidian": 0, "geode": 0
        }

        self.robots: dict[str, int] = {
            "ore": 1, "clay": 0, "obsidian": 0, "geode": 0
        }

        self.next_build: Robot = blueprint.robots.none
        self.passed_on: set[Robot] = set()
        self.steps = []

    def run(self):
        # start building
        self.steps.append(self.next_build.type)
        for k, v in self.next_build.cost.items():
            self.resources[k] -= v

        # collect resources
        for k, v in self.robots.items():
            self.resources[k] += v

        # building complete
        if self.next_build.type != "none":
            self.robots[self.next_build.type] += 1

        self.turn += 1

        # move on to next step

        # these are dead-ends if we don't have these robots by this deadline
        if ((self.turn > self.turn_limit - 2 and self.robots["geode"] == 0) or
            (self.turn > self.turn_limit - 4 and self.robots["obsidian"] == 0) or
            (self.turn > self.turn_limit - 6 and self.robots["clay"] == 0) or
                self.turn >= self.turn_limit):
            return self.resources["geode"], self.steps

        options = {r for r in self.blueprint.robots.all if r.can_build(self.resources)}

        # if we passed on building these robots last turn, pass again now
        if self.next_build.type == "none":
            options -= self.passed_on

        # don't bother building these if there are only t minutes left
        for t, r in [(1, self.blueprint.robots.geode),
                     (3, self.blueprint.robots.obsidian),
                     (5, self.blueprint.robots.clay),
                     (7, self.blueprint.robots.ore)]:
            if self.turn >= self.turn_limit - t:
                options -= {r}

        # it doesn't do any good to have more than n of these robots
        for n, r in [("ore", self.blueprint.robots.ore),
                     ("clay", self.blueprint.robots.clay),
                     ("obsidian", self.blueprint.robots.obsidian)]:
            if self.robots[n] >= self.blueprint.max_cost(n):
                options -= {r}

        # build a geode robot if we can or build first obsidian asap
        if self.blueprint.robots.geode in options:
            options = {self.blueprint.robots.geode}
        elif self.blueprint.robots.obsidian in options and self.robots["obsidian"] == 0:
            options = {self.blueprint.robots.obsidian}

        next_turns = []
        for opt in options:
            self.next_build = opt
            self.passed_on = options - {opt}
            next_turns.append(deepcopy(self).run())
        return max(next_turns)


def part_1() -> int:
    blueprints = [Blueprint.create_from_input(bp) for bp in get_daily_input(DAY)]
    results = []
    for bp in blueprints:
        r = Simulation(bp).run()
        print((bp.id * r[0], r))
        results.append((bp.id * r[0], r))
    return sum(r[0] for r in results)


def part_2() -> int:
    blueprints = [Blueprint.create_from_input(bp) for bp in get_daily_input(DAY)]
    results = []
    for bp in [blueprints[0]]:
        r = Simulation(bp, turn_limit=32).run()
        results.append((bp.id * r[0], r))
    return sum(r[0] for r in results)


def main():
    print(f"Part 1: {part_1()}")
    # print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()

"""
Part 1: 1127 is right
"""