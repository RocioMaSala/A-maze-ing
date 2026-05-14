import sys
from maze_generator import MazeGenerator
from typing import Generator
from random import seed


class UsageError(Exception):
    def __init__(self, message: str = "Usage Error: python3 a_maze_ing.py "
                 "config.txt") -> None:
        super().__init__(message)


class EntryExitError(Exception):
    def __init__(self, message: str = "Entry Exit Error: Entry and exit "
                 "points need to be in different positions.") -> None:
        super().__init__(message)


class ConfigSyntaxError(Exception):
    def __init__(self, message: str = "Invalid config file syntax.") -> None:
        super().__init__(message)


class EntryError(Exception):
    def __init__(self, message: str = "Entry coordinates must be within maze"
                 " boundaries.") -> None:
        super().__init__(message)


class ExitError(Exception):
    def __init__(self, message: str = "Exit coordinates must be within maze"
                 " boundaries.") -> None:
        super().__init__(message)

class SizeError(Exception):
    def  __init__(self, message: str = "To show the 42, the maze must be "
                  "larger than 7x5") -> None:
        super().__init__(message)


def parse_config_line(line: str) -> tuple[str, str]:
    parts = line.split("=", 1)
    if len(parts) != 2:
        raise ConfigSyntaxError(f"Invalid config format: '{line.strip()}'. "
                                "Expected 'KEY=VALUE'")
    key, value = parts
    if not key.strip():
        raise ConfigSyntaxError(
            f"Missing key in config line: '{line.strip()}'")
    return key.strip(), value.strip()


def random_generator(config: dict[str, str]) -> Generator[None, None, None]:
    maze = MazeGenerator()
    seed_val = 1
    while True:
        seed(seed_val)
        maze.generate_maze(config)
        seed_val += 1
        yield


def is_in_42(config: dict[str, str]) -> None:
    vis = [[False for i in range(int(config["WIDTH"]))]
           for j in range(int(config["HEIGHT"]))]
    y = round((len(vis) - 5) / 2)
    x = round((len(vis[0]) - 7) / 2)

    entry_x, entry_y = tuple(int(x) for x in config["ENTRY"].split(","))
    exit_x, exit_y = tuple(int(x) for x in config["EXIT"].split(","))

    targets = [
        (0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (2, 4),
        (4, 0), (5, 0), (6, 0), (6, 1), (6, 2), (5, 2), (4, 2),
        (4, 3), (4, 4), (5, 4), (6, 4)
    ]
    if (entry_x - x, entry_y - y) in targets:
        raise EntryExitError("Entry Exit Error: Entry and exits cannot be "
                             "inside the 42 drawing")


def menu(generate: Generator[None, None, None]):

    while True:
        print("== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")

        option = input("Choice? (1-4): ")

        while option not in ("1", "2", "3", "4"):
            option = input("Invalid choice. Try again (1-4): ")
        if option == "1":
            next(generate)
        elif option == "2":
            if show:  # hacer un interruptor
                print("Hide!")
            else:
                print("Show!")
        elif option == "3":
            print("Let's rotate the colors")
        elif option == "4":
            print("Thank you! Bye Bye")
            return


def main() -> None:
    try:
        if len(sys.argv) != 2:
            raise UsageError
        if sys.argv[1] != "config.txt":
            raise UsageError
        with open(sys.argv[1]) as file:
            config = {key.strip(): value.strip() for key, value in
                      (parse_config_line(line) for line in file if
                       line.strip())}
        if config["ENTRY"] == config["EXIT"]:
            raise EntryExitError
        ENTRY = [int(x) for x in config["ENTRY"].split(",")]
        EXIT = [int(x) for x in config["EXIT"].split(",")]
        if ENTRY[0] > int(config["WIDTH"]) or ENTRY[0] < 0 or ENTRY[1] > int(
                config["HEIGHT"]) or ENTRY[1] < 0:
            raise EntryError
        if EXIT[0] > int(config["WIDTH"]) or EXIT[0] < 0 or EXIT[1] > int(
                config["HEIGHT"]) or EXIT[1] < 0:
            raise ExitError
        if int(config["WIDTH"]) > 7 and int(config["HEIGHT"]) > 5:
            is_in_42(config)
        generate = random_generator(config)
        next(generate)
        if int(config["WIDTH"]) <= 7 or int(config["HEIGHT"]) <= 5:
            raise SizeError
        menu(generate)

    except UsageError as e:
        print(e)
    except FileNotFoundError:
        print("config.txt file not present")
    except EntryExitError as e:
        print(e)
    except EntryError as e:
        print(e)
    except ExitError as e:
        print(e)
    except SizeError as e:
        print(e)
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
