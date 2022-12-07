"""
Advent of Code 2022 Day 7
"""
import sys

from advent_tools import get_daily_input

DAY = 7

DEBUG = sys.argv[1] == "debug" if len(sys.argv) > 1 else False

DEBUG_DATA = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""

if DEBUG:
    def get_daily_input(x):
        for line in DEBUG_DATA.strip().split("\n"):
            yield line.strip("\n")


def part_1() -> int:
    pwd: str = ""
    dirs: dict[str, int] = {"/": 0}

    for line in get_daily_input(DAY):
        if line == "$ ls":
            continue
        elif line == "$ cd ..":
            pwd = "/".join(pwd.split("/")[:-2]) + "/"
        elif line.startswith("$ cd"):
            pwd = "/" if line == "$ cd /" else pwd + line.split(" ")[-1] + "/"
        elif line.startswith("dir "):
            dirname = line.split(" ")[-1]
            dirs[pwd + dirname + "/"] = 0
        else:
            size = line.split(" ")[0]
            dirs[pwd] += int(size)

    dir_sizes = {k: sum([dirs[l] for l in dirs if l.startswith(k)]) for k in dirs}

    return sum([dir_sizes[d] for d in dir_sizes if dir_sizes[d] <= 100000])


def part_2() -> int:
    data = get_daily_input(DAY)
    return 0


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == "__main__":
    main()
