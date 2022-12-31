"""
Advent of Code 2022 Day 22
"""
import re
import sys

from advent_tools import get_daily_input

DAY = 22

TEST = sys.argv[1] == "test" if len(sys.argv) > 1 else False

TEST_DATA = """
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""

if TEST:
    def get_daily_input(_):
        for line in TEST_DATA.strip("\n").split("\n"):
            yield line.strip("\n")


def load_data() -> tuple[list[str], list[str], int]:
    data_stream = get_daily_input(DAY)
    map_data: list[str] = []
    path_data: list[str] = []
    for d in data_stream:
        if d:
            map_data.append(d)
        else:
            path_data = re.findall(r"\d+|[LR]", next(data_stream))
    width = max(len(m) for m in map_data)
    height = len(map_data)
    if width * 4 == height * 3:
        face_size = width // 3
    elif width * 3 == height * 4:
        face_size = width // 4
    elif width * 2 == height * 6:
        face_size = width // 6
    else:
        face_size = width // 2

    return list([m.ljust(width) for m in map_data]), path_data, face_size


FACINGS = ">v<^"


def next_position_v1(mm: list[str], r: int, c: int, f: str) -> tuple[int, int]:
    if f == ">":
        points = mm[r]
        offset = c
    elif f == "<":
        points = "".join(reversed(mm[r]))
        offset = len(points) - c - 1
    elif f == "v":
        points = "".join([m[c] for m in mm])
        offset = r
    else:
        points = "".join([m[c] for m in reversed(mm)])
        offset = len(points) - r - 1

    if offset < len(points) - 1 and points[offset + 1] == ".":
        offset = offset + 1
    elif offset >= len(points) - 1 or points[offset + 1] == " ":
        for new_offset in range(offset - 1, -2, -1):
            if new_offset < 0 or points[new_offset] == " ":
                if points[new_offset + 1] == ".":
                    offset = new_offset + 1
                break

    if f == ">":
        return r, offset
    elif f == "<":
        return r, len(points) - offset - 1
    elif f == "v":
        return offset, c
    else:
        return len(points) - offset - 1, c


def is_vertex(mm, r, c) -> bool:
    return 0 < r < len(mm) - 1 and 0 < c < len(mm[r]) - 1 and \
        1 == sum([mm[i][j] == " " for i, j in [(r - 1, c - 1), (r - 1, c + 1),
                                               (r + 1, c- 1), (r + 1, c + 1)]])


def next_position_v2(mm: list[str], s: int, r: int, c: int, f: str) -> tuple[int, int, str]:
    map_height = len(mm)
    map_width = len(mm[0])

    face_map = [
        [None, None, ("u", "rflb"), None],
        [("b", "ldru"), ("l", "fdbu"), ("f", "rdlu"), None],
        [None, None, ("d", "rblf"), ("r", "ubdf")],
    ]

    if f == ">":
        points = mm[r]
        offset = c
    elif f == "<":
        points = "".join(reversed(mm[r]))
        offset = len(points) - c - 1
    elif f == "v":
        points = "".join([m[c] for m in mm])
        offset = r
    else:
        points = "".join([m[c] for m in reversed(mm)])
        offset = len(points) - r - 1

    if offset < len(points) - 1 and points[offset + 1] == ".":
        offset = offset + 1
        if f == ">":
            return r, offset, f
        elif f == "<":
            return r, len(points) - offset - 1, f
        elif f == "v":
            return offset, c, f
        else:
            return len(points) - offset - 1, c, f

    elif offset >= len(points) - 1 or points[offset + 1] == " ":
        # we're on the edge!
        curr_face, curr_edges = face_map[r // s][c // s]
        next_face = curr_edges[FACINGS.find(f)]

        next_fm = None
        for i in range(len(face_map)):
            for j in range(len(face_map[0])):
                if face_map[i][j] and face_map[i][j][0] == next_face:
                    next_fm = i, j
                    break
            if next_fm:
                break

        next_edges = face_map[next_fm[0]][next_fm[1]][1]
        next_facing = FACINGS[next_edges.find(curr_face) - 2]

        nr = next_fm[0] * s + ((s - 1) if next_facing == "^" else 0)
        nc = next_fm[1] * s + ((s -1 ) if next_facing == "<" else 0)

        if (next_facing == "v" and f == ">") or (next_facing == "^" and f == "<"):
            nc = nc + s - 1 - r % s
        elif (next_facing == "v" and f == "<") or (next_facing == "^" and f == "<"):
            nc = nc + r % s
        elif (next_facing == "v" and f == "^") or (next_facing == "^" and f == "v"):
            nc = nc + s - 1 - c % s
        elif (next_facing == ">" and f == "^") or (next_facing == "<" and f == "v"):
            nr = nr + c % s
        elif (next_facing == ">" and f == "v") or (next_facing == "<" and f == "^"):
            nr = nr + s - 1 - c % s
        elif (next_facing == ">" and f == "<") or (next_facing == "<" and f == ">"):
            nr = nr + s - 1 - c % s

        if mm[nr][nc] == ".":
            return nr, nc, next_facing

    return r, c, f


def part_1() -> int:
    monkey_map, path, _ = load_data()
    row, column = 0, monkey_map[0].find(".")
    facing = ">"

    for p in path:
        if p.isnumeric():
            for _ in range(int(p)):
                row, column = next_position_v1(monkey_map, row, column, facing)
        elif p == "L":
            facing = FACINGS[FACINGS.find(facing) - 1]
        else:
            facing = FACINGS[(FACINGS.find(facing) + 1) % 4]

    return 1000 * (row + 1) + 4 * (column + 1) + FACINGS.find(facing)


def part_2() -> int:
    monkey_map, path, size = load_data()
    row, column = 0, monkey_map[0].find(".")
    facing = ">"

    for p in path:
        if p.isnumeric():
            for _ in range(int(p)):
                row, column, facing = \
                    next_position_v2(monkey_map, size, row, column, facing)
        elif p == "L":
            facing = FACINGS[FACINGS.find(facing) - 1]
        else:
            facing = FACINGS[(FACINGS.find(facing) + 1) % 4]

    return 1000 * (row + 1) + 4 * (column + 1) + FACINGS.find(facing)


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()

"""
Part 1: 75254
"""