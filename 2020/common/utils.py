import typing
import re

# Add things that are repeatedly needed here.

# functions below copied from users mcpower / mserrano
def lmap(func, *iterables):
    return list(map(func, *iterables))

def ints(s: str) -> typing.List[int]:
    return lmap(int, re.findall(r"-?\d+", s))

def positive_ints(s: str) -> typing.List[int]:
    return lmap(int, re.findall(r"\d+", s))

def floats(s: str) -> typing.List[float]:
    return lmap(float, re.findall(r"-?\d+(?:\.\d+)?", s))

def positive_floats(s: str) -> typing.List[float]:
    return lmap(float, re.findall(r"\d+(?:\.\d+)?", s))

def words(s: str) -> typing.List[str]:
    return re.findall(r"[a-zA-Z]+", s)
