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
    def get_daily_input(_) -> list[str]:
        for line in DEBUG_DATA.strip().split("\n"):
            yield line.strip("\n")


class Valve:
    def __init__(self, name: str, flow_rate: int, tunnels: list[str]):
        self.name = name
        self.flow_rate = flow_rate
        self.tunnels = tunnels


def build_distance_matrix(valves: dict[str, Valve]) -> dict[str, [dict[str, int]]]:
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

    return {
        k: {
            j: v for j, v in matrix[k].items() if valves[j].flow_rate and k != j
        } for k in matrix
    }


def find_paths(valves: dict[str, Valve], start: str, time_limit: int) \
        -> list[tuple[int, list[str]]]:
    distances = build_distance_matrix(valves)
    stack = [(time_limit, 0, [start])]
    paths = []
    while stack:
        time, pressure, path = stack.pop()
        curr_loc = path[-1]

        next_locs = [
            (valve, distance) for valve, distance in distances[curr_loc].items()
            if distance <= time - 2 and valve not in path
        ]

        if next_locs:
            for next_loc, dist in next_locs:
                if dist <= time - 2 and next_loc not in path:
                    next_time = time - dist - 1
                    next_pressure = pressure + valves[next_loc].flow_rate * next_time
                    stack.append((next_time, next_pressure, path + [next_loc]))
        else:
            paths.append((pressure, path[1:]))
    return paths


def part_1() -> int:
    valves: dict[str, Valve] = {}
    for row in [re.findall(r"[A-Z]{2}|\d+", d) for d in get_daily_input(DAY)]:
        valves[row[0]] = Valve(row[0], int(row[1]), row[2:])

    paths = find_paths(valves, "AA", 30)

    return max(paths)[0]


def part_2() -> int:
    valves: dict[str, Valve] = {}
    for row in [re.findall(r"[A-Z]{2}|\d+", d) for d in get_daily_input(DAY)]:
        valves[row[0]] = Valve(row[0], int(row[1]), row[2:])

    paths = sorted(find_paths(valves, "AA", 26), reverse=True)
    j_max = 1
    while any(x in paths[j_max][1] for x in paths[0][1]):
        j_max += 1
    ans = paths[0][0] + paths[j_max][0]
    for i in range(1, j_max):
        for j in range(i + 1, j_max + 1):
            if not any(x in paths[j][1] for x in paths[i][1]):
                ans = max(ans, paths[j][0] + paths[i][0])
    return ans


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
