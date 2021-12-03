# Input functions taken from:
# https://blog.keiruaprod.fr/2021/11/23/getting-ready-for-adventofcode-in-python.html

from typing import List
import re

def input_as_string(filename:str) -> str:
    """returns the content of the input file as a string"""
    with open(filename) as f:
        return f.read().rstrip("\n")

def input_as_lines(filename:str) -> List[str]:
    """Return a list where each line in the input file is an element of the list"""
    return input_as_string(filename).split("\n")

# One integer per line
def input_as_ints(filename:str) -> List[int]:
    """Return a list where each line in the input file is an element of the list, converted into an integer"""
    lines = input_as_lines(filename)
    # remove empty lines
    while '' in lines:
        lines.remove('')
    line_as_int = lambda l: int(l.rstrip('\n'))
    return list(map(line_as_int, lines))

# Integers on one line, comma or space or whatever-separated
def input_as_line_of_ints(filename:str) -> List[int]:
    s = input_as_string(filename)
    list_as_str = re.findall(r'([-+]?\d+)', s)
    return list(map(int, list_as_str))
