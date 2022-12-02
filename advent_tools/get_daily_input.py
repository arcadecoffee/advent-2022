"""
Tools and utilities for use with the Advent of Code
https://adventofcode.com
"""
from typing import Iterable

from urllib.request import Request, urlopen


def get_daily_input(day: int = 1, session_id: str = None) -> Iterable[str]:
    """
    Yield lines from the day's input set
    """
    with urlopen(Request(
            url=f"https://adventofcode.com/2022/day/{day}/input",
            headers={"Cookie": f"session={session_id}"}
        )) as response:
        if response.status == 200:
            for line in response.readlines():
                yield line.decode().strip()
