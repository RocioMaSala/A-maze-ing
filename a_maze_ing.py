import sys
import random


class UsageError(Exception):
    def __init__(self, message: str = "Usage Error: python3 a_maze_ing.py "
                 "config.txt") -> None:
        super().__init__(message)


class EntryExitError(Exception):
    def __init__(self, message: str = "Entry Exit Error: Entry and exit "
                 "points need to be in different positions") -> None:
        super().__init__(message)


def border_check(x: int, y: int, maze: list[list[int]]) -> bool:
    if y == 0 and (maze[x][y] >> 3) == 0:
        return False
    elif y == len(maze[x]) - 1 and (maze[x][y] >> 1) % 2 == 0:
        return False
    elif x == 0 and maze[x][y] % 2 == 0:
        return False
    elif x == len(maze) - 1 and (maze[x][y] >> 2) % 2 == 0:
        return False
    return True


def maze_verification(maze: list[list[int]]) -> bool:
    if not maze:
        return False
    for x in range(len(maze)):
        for y in range(len(maze[x])):
            if not border_check(x, y, maze):
                return False
            if y > 0 and y < len(maze[x]) - 1 and (maze[x][y] >> 3) % 2 != (maze[x][y-1] >> 1) % 2:
                return False
            elif y > 0 and y < len(maze[x]) - 1 and (maze[x][y] >> 1) % 2 != (maze[x][y+1] >> 1) % 2:
                return False
            elif x > 0 and x < len(maze) - 1 and (maze[x][y] >> 2) % 2 != maze[x-1][y] % 2:
                return False
            elif x > 0 and x < len(maze) - 1 and maze[x][y] % 2 != (maze[x+1][y] >> 2) % 2:
                return False
    return True


def maze_generation() -> list[list[int]]:
    maze: list[list[int]] = []
    while not maze_verification(maze):
        for x in range(int(config["HEIGHT"])):
            maze.append([])
            for y in range(int(config["WIDTH"])):
                maze[x].append(random.randint(0, 14))
    return maze


try:
    if len(sys.argv) != 2:
        raise UsageError
    if sys.argv[1] != "config.txt":
        raise UsageError
    with open(sys.argv[1]) as file:
        config = {key.strip(): value.strip() for key, value in
                  (line.split("=", 1) for line in file)}
    maze: list[list[int]] = maze_generation()
    if config["ENTRY"] == config["EXIT"]:
        raise EntryExitError
except UsageError as e:
    print(e)
except FileNotFoundError:
    print("config.txt file not present")
except EntryExitError as e:
    print(e)
