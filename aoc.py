# aoc helper functions, mostly for input, inspired by:
# https://blog.keiruaprod.fr/2021/11/23/getting-ready-for-adventofcode-in-python.html

from typing import List
import re

def input_string(filename:str) -> str:
    """
    returns the content of the input file as a string
    """
    with open(filename) as f:
        return f.read().rstrip('\n')

def lines(filename:str) -> List[str]:
    """
    Return a list where each line in the input file
    is an element of the list
    """
    return input_string(filename).split('\n')

# One integer per line
def ints(filename:str) -> List[int]:
    """
    Return a list where each line in the input file is
    an element of the list converted into an integer
    Example:
    1
    2
    3
    returns [1, 2, 3]
    """
    lns = lines(filename)
    # remove empty lines
    while '' in lns:
        lns.remove('')
    line_as_int = lambda l: int(l.rstrip('\n'))
    return list(map(line_as_int, lines))

# Return list of ints on one line
def ints(s:str) -> List[int]:
    """
    Takes input as string
    returns list of ints
    Example:
    '  a330  b143  c338'
    returns [330, 143, 338]
    """
    list_as_str = re.findall(r'([-+]?\d+)', s)
    return list(map(int, list_as_str))


def line_of_ints(filename:str) -> List[int]:
    """
    Read line of ints from file
    Example:
    'a1, b2, a3, c4'
    returns [1, 2, 3, 4]
    """
    return ints(input_string(filename))

def lines_of_ints(filename:str) -> List[List[int]]:
    """
    lines with integers on each line, separated by whatever
    Example:
    1 2
    3 4
    returns [[1, 2], [3, 4]]
    """
    a = []
    for line in lines(filename):
        a.append(ints(line))
    return a

# LetterIntegers on one line
def line_of_letterints(filename:str) -> List[tuple]:
    """
    Example:
    'L5, R1'
    returns [('L', 5), ('R', 1)]
    """
    s = input_string(filename)
    ints = re.findall(r'([-+]?\d+)', s)
    letters = re.findall(r'([A-Z]+)', s)

    return list(zip(letters, map(int, ints)))

def char_matrix(filename:str) -> List[List[str]]:
    """
    Read input as a matrix.
    Split each line into chars.
    Example:
    abc
    def
    returns [['a', 'b', 'c'], ['d', 'e', 'f']]
    """
    lineslist = lines(filename)
    return [list(x) for x in lineslist]

def transpose(matrix):
    """
    Example:
    [[1, 2, 3], [4, 5, 6]]
    returns [[1, 4], [2, 5], [3, 6]]
    """
    return [list(group) for group in zip(*matrix)]