"""
Tools and utilities for use with the Advent of Code
https://adventofcode.com
"""
from os import makedirs
from os.path import exists
from typing import Iterable
from urllib.request import Request, urlopen


def download_daily_input(day: int = 1, session_id: str = None) -> None:
    """
    Yield lines from the day's input set
    """
    if not session_id:
        with open(".aocsession", mode="rt") as dot_aocsession:
            session_id = dot_aocsession.readline().strip()

    with urlopen(Request(
            url=f"https://adventofcode.com/2022/day/{day}/input",
            headers={"Cookie": f"session={session_id}"}
        )) as response:
        if response.status == 200:
            makedirs(".aoccache", exist_ok=True)
            with open(f".aoccache/{day}.txt", mode="wt") as outfile:
                for line in response:
                    outfile.write(line.decode())


def get_daily_input(day: int = 1, session_id: str = None, force_download=False) -> Iterable[str]:
    if force_download or not exists(f".aoccache/{day}.txt"):
        download_daily_input(day, session_id)
    with open(f".aoccache/{day}.txt", mode="rt") as infile:
        for line in infile:
            yield line.strip()
