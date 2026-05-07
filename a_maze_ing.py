import sys
import random


class UsageError(Exception):
    def __init__(self, message: str = "Usage Error: python3 a_maze_ing.py "
                 "config.txt") -> None:
        super().__init__(message)


try:
    if len(sys.argv) != 2:
        raise UsageError
    if sys.argv[1] != "config.txt":
        raise UsageError
    with open(sys.argv[1]) as file:
        config = {key.strip(): value.strip() for key, value in
                  (line.split("=", 1) for line in file)}
    maze: list[list[int]] = []
    for x in range(int(config["HEIGHT"])):
        maze.append([])
        for y in range(int(config["WIDTH"])):
            maze[x].append(random.randint(0, 15))
    print(maze)

except UsageError as e:
    print(e)
except FileNotFoundError:
    print("config.txt file not present")
