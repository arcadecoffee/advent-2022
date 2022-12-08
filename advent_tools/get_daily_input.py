"""
Fetch, cache, and access your input data from Advent of Code
https://adventofcode.com
"""
from os import makedirs
from os.path import exists
from typing import Iterable
from urllib.request import Request, urlopen


_URL_TEMPLATE = "https://adventofcode.com/2022/day/{day}/input"
_SESSION_FILENAME = ".aocsession"
_CACHE_DIRECTORY = ".aoccache"


def _cache_filename(day: int):
    return f"{_CACHE_DIRECTORY}/{day}.txt"


def download_daily_input(day: int = 1, session_id: str = None) -> None:
    """
    Yield lines from the day's input set
    """
    if not session_id:
        with open(_SESSION_FILENAME, mode="rt") as dot_aocsession:
            useragent = dot_aocsession.readline().strip()
            session_id = dot_aocsession.readline().strip()

    with urlopen(Request(
            url=_URL_TEMPLATE.format(day=day),
            headers={"Cookie": f"session={session_id}", "User-Agent": useragent}
        )) as response:
        if response.status == 200:
            makedirs(_CACHE_DIRECTORY, exist_ok=True)
            with open(_cache_filename(day), mode="wt") as outfile:
                for line in response:
                    outfile.write(line.decode())


def get_daily_input(day: int = 1, session_id: str = None, force_download=False) -> Iterable[str]:
    if force_download or not exists(_cache_filename(day)):
        download_daily_input(day, session_id)
    with open(_cache_filename(day), mode="rt") as infile:
        for line in infile:
            yield line.strip("\n")
