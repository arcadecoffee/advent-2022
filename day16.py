"""
Advent of Code 2022 Day 16
"""
import re
import sys

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
    def get_daily_input(_):
        for line in DEBUG_DATA.strip().split("\n"):
            yield line.strip("\n")


class Valve:
    def __init__(self, name: str, flow_rate: int, tunnels: list[str]):
        self.name = name
        self.flow_rate = flow_rate
        self.tunnels = tunnels


def build_distance_matrix(valves):
    matrix = {}
    for v in valves.values():
        matrix[v.name] = {v.name: 0}
        for t in v.tunnels:
            matrix[v.name][t] = 1
    for v in matrix:
        keep_going = True
        while keep_going:
            keep_going = False
            for w in [i for i in matrix[v] if i != v]:
                for x in matrix[w]:
                    new_distance = matrix[w][x] + matrix[v][w]
                    if x not in matrix[v] or matrix[v][x] > new_distance:
                        matrix[v][x] = new_distance
                        keep_going = True
    return matrix


def get_costs_to_close(distances, valves, open):
    costs = {}
    for v, d in distances.items():
        if valves[v].flow_rate != 0 and v not in open:
            costs[v] = sum([valves[v].flow_rate * (d + 1) for v in valves])
    return costs


def part_1() -> int:
    valves: dict[str, Valve] = {}
    for row in [re.findall(r"[A-Z]{2}|\d+", d) for d in get_daily_input(DAY)]:
        valves[row[0]] = Valve(row[0], int(row[1]), row[2:])

    distance_matrix = build_distance_matrix(valves)

    queue = [(0, 0, "AA", {})]
    visited = set()
    while queue:
        unreleased_pressure, time, location, opened = queue.pop(0)

        if (unreleased_pressure, time, location, str(opened)) not in visited:
            visited.add((unreleased_pressure, time, location, str(opened)))
            unopened = [v for v in valves if v not in opened and valves[v].flow_rate != 0]

            print(f"\r{unreleased_pressure} : {time}", end="")

            if time >= 30 or not unopened:
                print("")
                return sum([(30 - v) * valves[k].flow_rate for k, v in opened.items()])
            else:
                for next_valve in unopened:
                    time_to_next = distance_matrix[location][next_valve] + 1
                    unreleased_pressure_before_next = \
                        sum(time_to_next * valves[v].flow_rate for v in unopened)
                    queue.append((
                        unreleased_pressure + unreleased_pressure_before_next,
                        time + time_to_next,
                        next_valve,
                        {**opened, next_valve: time + time_to_next}
                    ))
                queue.sort(key=lambda l: (l[0], 30 - l[1]))

    return 0


def part_2() -> int:
    data = get_daily_input(DAY)
    return 0


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
