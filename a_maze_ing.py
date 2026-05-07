import sys
from random import randint


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


"""
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
"""


def cell_verification(rand: int, comp: int, direction: str) -> bool:
    if direction == "north":
        if rand % 2 != (comp >> 2) % 2:
            return False
    elif direction == "west":
        if (rand >> 3) % 2 != (comp >> 1) % 2:
            return False
    return True


def cell_generation(x: int, y: int, maze: list[list[int]]) -> int:
    if x == 0 and y == 0:
        while not border_check(x, y, maze):
            attempt = randint(0, 14)
            maze[x].append(randint(0, 14))
    nbrs = [x for x in range(14)]
    while nbrs:
        attempt = nbrs.pop(randint(0, len(nbrs)))
        if border_check(x, y, maze):
            if x > 0 and y > 0:
                if cell_verification(attempt, maze[x-1][y], direction="north") and cell_verification(attempt, maze[x][y-1], direction="west"):
                    return attempt
            elif y == 0:
                if cell_verification(attempt, maze[x-1][y], direction="north"):
                    return attempt
            elif x == 0:
                if cell_verification(attempt, maze[x][y-1], direction="west"):
                    return attempt
    return -1


def maze_generation(config: dict[str, str]) -> list[list[int]]:
    maze: list[list[int]] = []
    for x in range(int(config["HEIGHT"])):
        maze.append([])
        for y in range(int(config["WIDTH"])):
            maze[x].append(cell_generation(x, y, maze))
    return maze


def main() -> None:
    try:
        if len(sys.argv) != 2:
            raise UsageError
        if sys.argv[1] != "config.txt":
            raise UsageError
        with open(sys.argv[1]) as file:
            config = {key.strip(): value.strip() for key, value in
                      (line.split("=", 1) for line in file)}
        maze: list[list[int]] = maze_generation(config)
        print(maze)
        if config["ENTRY"] == config["EXIT"]:
            raise EntryExitError
    except UsageError as e:
        print(e)
    except FileNotFoundError:
        print("config.txt file not present")
    except EntryExitError as e:
        print(e)


if __name__ == "__main__":
    main()
