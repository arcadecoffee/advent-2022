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


def next_position_2d(mm: list[str], r: int, c: int, f: str) -> tuple[int, int]:
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


def next_position_3d(mm: list[str], s: int, r: int, c: int, f: str) -> tuple[int, int, str]:

    map_height = len(mm)
    map_width = len(mm[0])

    # TEST
    # face_map = [
    #     [None, None, ("u", "rflb"), None],
    #     [("b", "ldru"), ("l", "fdbu"), ("f", "rdlu"), None],
    #     [None, None, ("d", "rblf"), ("r", "ubdf")],
    # ]
    face_map = [
        [None, ("u", "rflb"), ("r", "dfub")],
        [None, ("f", "rdlu"), None],
        [("l", "dbuf"), ("d", "rblf"), None],
        [("b", "drul"), None, None]
    ]

    def find_face(target_face: str) -> tuple[int, int]:
        for i in range(len(face_map)):
            for j in range(len(face_map[i])):
                if face_map[i][j] and face_map[i][j][0] == target_face:
                    return i, j

    nr, nc, nf = r, c, f
    if f == ">" and c + 1 < map_width and mm[r][c + 1] != " ":
        nc += 1
    elif f == "<" and c > 0 and mm[r][c - 1] != " ":
        nc -= 1
    elif f == "^" and r > 0 and mm[r - 1][c] != " ":
        nr -= 1
    elif f == "v" and r + 1 < map_height and mm[r + 1][c] != " ":
        nr += 1
    else:
        cf_name, cf_edges = face_map[r // s][c // s]
        nf_name = cf_edges[FACINGS.find(f)]
        nf_map_row, nf_map_col = find_face(nf_name)
        nf_edges = face_map[nf_map_row][nf_map_col][1]

        nf = FACINGS[nf_edges.find(cf_name) - 2]
        nr = nf_map_row * s + ((s - 1) if nf == "^" else 0)
        nc = nf_map_col * s + ((s - 1) if nf == "<" else 0)

        if (f == ">" and nf == "v") or (f == "<" and nf == "^"):   # 90 cw h to v
            nc += s - 1 - r % s
        elif (f == "^" and nf == ">") or (f == "v" and nf == "<"):  # 90 cw v to h
            nr += c % s
        elif (f == ">" and nf == "^") or (f == "<" and nf == "v"):  # 90 ccw h to v
            nc += r % s
        elif (f == "v" and nf == ">") or (f == "^" and nf == "<"):  # 90 ccw v to h
            nr += s - 1 - c % s
        elif (f == ">" and nf == "<") or (f == "<" and nf == ">"):  # 180 horiz
            nr += s - 1 - r % s
        elif (f == "^" and nf == "v") or (f == "v" and nf == "^"):  # 180 vert
            nc += s - 1 - c % s
        elif (f == "<" and nf == "<") or (f == ">" and nf == ">"):  # 0 horiz
            nr += r % s
        elif (f == "^" and nf == "^") or (f == "v" and nf == "v"):  # 0 vert
            nc += c % s

    if mm[nr][nc] == ".":
        r, c, f = nr, nc, nf

    return r, c, f


def part_1() -> int:
    monkey_map, path, _ = load_data()
    row, column = 0, monkey_map[0].find(".")
    facing = ">"

    for p in path:
        if p.isnumeric():
            for _ in range(int(p)):
                row, column = next_position_2d(monkey_map, row, column, facing)
        elif p == "L":
            facing = FACINGS[FACINGS.find(facing) - 1]
        else:
            facing = FACINGS[(FACINGS.find(facing) + 1) % 4]

    return 1000 * (row + 1) + 4 * (column + 1) + FACINGS.find(facing)


class MonkeyMapCubeNet:
    adjacent = {
        "u": "rflb", "d": "rblf",
        "f": "rdlu", "b": "ldru",
        "l": "fdbu", "r": "bdfu"
    }

    def __init__(self, mm):
        self.map = mm
        self.height = len(mm)
        self.width = len(mm[0])
        self.face_size = self.find_face_size(self.height, self.width)

        self.face_map: list[list[tuple[str, str] | None]] = [
            [None for _ in range(self.width // self.face_size)]
            for _ in range(self.height // self.face_size)
        ]

        first_face = (0, re.search(r"[.#]", self.map[0]).start() // self.face_size)
        self.face_map[0][first_face[1]] = ("u", "rflb")
        self._add_sides(*first_face)

    def _add_sides(self, r: int, c: int) -> None:
        cf = self.face_map[r][c][0]
        if r > 0 and not self.face_map[r - 1][c] and self.map[(r - 1) * self.face_size][c * self.face_size] != " ":
            nf = self.face_map[r][c][1][3]
            ne = self.adjacent[nf]
            while ne[1] != cf:
                ne = ne[1:] + ne[0]
            self.face_map[r - 1][c] = (nf, ne)
            self._add_sides(r - 1, c)
        if r + 1 < len(self.face_map) and not self.face_map[r + 1][c] and self.map[(r + 1) * self.face_size][c * self.face_size] != " ":
            nf = self.face_map[r][c][1][1]
            ne = self.adjacent[nf]
            while ne[3] != cf:
                ne = ne[1:] + ne[0]
            self.face_map[r + 1][c] = (nf, ne)
            self._add_sides(r + 1, c)
        if c > 0 and not self.face_map[r][c - 1] and self.map[r * self.face_size][(c - 1) * self.face_size] != " ":
            nf = self.face_map[r][c][1][2]
            ne = self.adjacent[nf]
            while ne[0] != cf:
                ne = ne[1:] + ne[0]
            self.face_map[r][c - 1] = (nf, ne)
            self._add_sides(r, c - 1)
        if c + 1 < len(self.face_map[r]) and not self.face_map[r][c + 1] and self.map[r * self.face_size][(c + 1) * self.face_size] != " ":
            nf = self.face_map[r][c][1][0]
            ne = self.adjacent[nf]
            while ne[2] != cf:
                ne = ne[1:] + ne[0]
            self.face_map[r][c + 1] = (nf, ne)
            self._add_sides(r, c + 1)

    @classmethod
    def find_face_size(cls, h, w) -> int:
        for x, y in [(2,5), (3,4), (4,3), (5,2)]:
            if h // x == w // y:
                return h // x


def part_2() -> int:
    monkey_map, path, size = load_data()
    row, column = 0, monkey_map[0].find(".")
    facing = ">"

    mm = MonkeyMapCubeNet(monkey_map)

    for p in path:
        # print(f"{row}, {column} - {facing}")
        if p.isnumeric():
            for _ in range(int(p)):
                row, column, facing = \
                    next_position_3d(monkey_map, size, row, column, facing)
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
Part 2: 108311
"""