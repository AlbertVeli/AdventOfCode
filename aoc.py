# aoc helper functions, mostly for input, inspired by:
# https://blog.keiruaprod.fr/2021/11/23/getting-ready-for-adventofcode-in-python.html

from collections import deque
from typing import Dict, List, Optional
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

# Some basic functions

def bfs(graph: Dict[str, List[str]], root: str, goal: str) -> bool:
    """
    Perform a breadth-first search to determine if there is a path from root to goal in the graph.

    Args:
        graph (Dict[str, List[str]]): A dictionary representing the graph. Each key is a node,
                                      and the value is a list of nodes it can reach.
        root (str): The starting node of the search.
        goal (str): The target node to find.

    Returns:
        bool: True if there is a path from root to goal, False otherwise.
    """
    queue = deque()
    seen = set()

    queue.appendleft(root)
    seen.add(root)

    while queue:
        current = queue.popleft()
        if current == goal:
            return True
        for neighbor in graph.get(current, []):
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)

    return False

def bfs_with_path(graph: Dict[str, List[str]], root: str, goal: str) -> Optional[List[str]]:
    """
    Perform a breadth-first search to determine if there is a path from root to goal
    in the graph and return the path if found.

    Args:
        graph (Dict[str, List[str]]): A dictionary representing the graph. Each key is a node,
                                      and the value is a list of nodes it can reach.
        root (str): The starting node of the search.
        goal (str): The target node to find.

    Returns:
        Optional[List[str]]: A list of nodes representing the path from root to goal if found,
                             None otherwise.
    """
    queue = deque()
    seen = set()
    parent = {}

    queue.appendleft(root)
    seen.add(root)
    parent[root] = None  # Root has no parent

    while queue:
        current = queue.popleft()
        if current == goal:
            # Reconstruct the path from root to goal
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]  # Reverse to get path from root to goal

        for neighbor in graph.get(current, []):
            if neighbor not in seen:
                seen.add(neighbor)
                parent[neighbor] = current  # Track the parent of the neighbor
                queue.append(neighbor)
    # Goal not found
    return None

def dfs(graph: Dict[str, List[str]], root: str, goal: str) -> bool:
    """
    Perform an iterative depth-first search to determine if there is a path from root to goal
    in the graph.

    Args:
        graph (Dict[str, List[str]]): A dictionary representing the graph. Each key is a node,
                                      and the value is a list of nodes it can reach.
        root (str): The starting node of the search.
        goal (str): The target node to find.

    Returns:
        bool: True if there is a path from root to goal, False otherwise.
    """
    stack = [root]
    seen = set()

    while stack:
        current = stack.pop()

        if current == goal:
            return True

        if current not in seen:
            seen.add(current)
            for neighbor in graph.get(current, []):
                if neighbor not in seen:
                    stack.append(neighbor)

    return False

def dfs_with_path(graph: Dict[str, List[str]], root: str, goal: str) -> Optional[List[str]]:
    """
    Perform an iterative depth-first search to determine if there is a path from root to goal
    in the graph and return the path if found.

    Args:
        graph (Dict[str, List[str]]): A dictionary representing the graph. Each key is a node,
                                      and the value is a list of nodes it can reach.
        root (str): The starting node of the search.
        goal (str): The target node to find.

    Returns:
        Optional[List[str]]: A list of nodes representing the path from root to goal if found,
                             None otherwise.
    """
    stack = [root]
    seen = set()
    parent = {}

    parent[root] = None  # Root has no parent

    while stack:
        current = stack.pop()

        if current == goal:
            # Reconstruct the path from root to goal
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]  # Reverse to get path from root to goal

        if current not in seen:
            seen.add(current)
            for neighbor in graph.get(current, []):
                if neighbor not in seen:
                    parent[neighbor] = current  # Track the parent of the neighbor
                    stack.append(neighbor)

    return None  # Goal not found