"""
Advent of Code 2022 Day 16
"""
import re
import sys

from dataclasses import dataclass
from itertools import combinations

from advent_tools import get_daily_input

DAY = 16

DEBUG = sys.argv[1] == "test" if len(sys.argv) > 1 else False

DEBUG_DATA = """
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"""

if DEBUG:
    def get_daily_input(_) -> list[str]:
        for line in DEBUG_DATA.strip().split("\n"):
            yield line.strip("\n")


@dataclass
class Valve:
    name: str
    flow_rate: int
    tunnels: list[str]


@dataclass(order=True)
class Route:
    pressure_released: int
    time_remaining: int
    route: list[str]


def build_distance_matrix(valves: dict[str, Valve]) -> dict[str, [dict[str, int]]]:
    matrix = {}
    for v in valves:
        matrix[v] = {i: 1 for i in valves[v].tunnels}

    for valve_a in matrix:
        for valve_b in [v for v in matrix if v != valve_a and valve_a in matrix[v]]:
            for destination, distance in matrix[valve_a].items():
                matrix[valve_b][destination] = min(
                    matrix[valve_b][valve_a] + distance,
                    matrix[valve_b].get(destination, len(valves))
                )

    return {
        s: {
            k: v for k, v in d.items() if valves[k].flow_rate
        } for s, d in matrix.items()
    }


def load_input() -> dict[str, Valve]:
    valves: dict[str, Valve] = {}
    for row in [re.findall(r"[A-Z]{2}|\d+", d) for d in get_daily_input(DAY)]:
        valves[row[0]] = Valve(row[0], int(row[1]), row[2:])
    return valves


def find_routes(valves: dict[str, Valve], time_limit: int) -> list[Route]:
    distances = build_distance_matrix(valves)
    routes: list[Route] = []
    stack: list[Route] = [Route(0, time_limit, ["AA"])]
    while stack:
        curr_route = stack.pop()
        curr_loc = curr_route.route[-1]
        for next_loc, next_dist in distances[curr_loc].items():
            if next_loc not in curr_route.route \
                    and next_dist < curr_route.time_remaining - 2:
                next_time_remaining = curr_route.time_remaining - next_dist - 1
                next_score = curr_route.pressure_released + \
                             next_time_remaining * valves[next_loc].flow_rate
                next_route = curr_route.route + [next_loc]
                stack.append(Route(next_score, next_time_remaining, next_route))
        routes.append(curr_route)
    return routes


def part_1() -> int:
    routes = find_routes(load_input(), 30)
    return max(routes).pressure_released


def part_2() -> int:
    routes = sorted(find_routes(load_input(), 26), reverse=True)

    best = (0, 0, len(routes))

    for a in range(len(routes) - 1):
        for b in range(a + 1, best[2]):
            if set(routes[a].route) & set(routes[b].route) == {"AA"}:
                score = routes[a].pressure_released + routes[b].pressure_released
                if score > best[0]:
                    best = (score, a, b)
                    break

    return best[0]


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
