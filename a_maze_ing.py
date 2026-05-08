import sys
from random import randint
from maze_generation import full_maze_generation


class UsageError(Exception):
    def __init__(self, message: str = "Usage Error: python3 a_maze_ing.py "
                 "config.txt") -> None:
        super().__init__(message)


class EntryExitError(Exception):
               def __init__(self, message: str = "Entry Exit Error: Entry and exit "
                 "points need to be in different positions") -> None:
        super().__init__(message)


def maze_generation(config: dict[str, str]) -> list[list[int]]:
    maze = full_maze_generation(config)
    
    return 


def main() -> None:
    try:
        if len(sys.argv) != 2:
            raise UsageError
        if sys.argv[1] != "config.txt":
            raise UsageError
        with open(sys.argv[1]) as file:
            config = {key.strip(): value.strip() for key, value in

                      (line.split("=", 1) for line in file)}
        if config["ENTRY"] == config["EXIT"]:
            raise EntryExitError
        maze: list[list[int]] = maze_generation(config)
        print(maze)
    except UsageError as e:
        print(e)
    except FileNotFoundError:
        print("config.txt file not present")
    except EntryExitError as e:
        print(e)


if __name__ == "__main__":
    main()
