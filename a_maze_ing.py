import sys


class UsageError(Exception):
    def __init__(self, message: str = "Usage Error: python3 a_maze_ing.py "
                 "config.txt") -> None:
        super().__init__(message)


try:
    if len(sys.argv) != 2:
        raise UsageError
    if sys.argv[1] != "config.txt":
        raise UsageError
    open("config.txt")
except UsageError as e:
    print(e)
except FileNotFoundError:
    print("config.txt file not present")
