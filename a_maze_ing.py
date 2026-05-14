import sys
from maze_generator import MazeGenerator
from typing import Generator
from random import seed
from representation import representation

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


def random_generator(config: dict[str, str]) -> Generator[tuple, None, None]:
    maze_gen = MazeGenerator()
    seed_val = 1
    while True:
        seed(seed_val)
        maze, route = maze_gen.generate_maze(config, False)
        seed_val += 1
        yield maze, route

def menu(generate: Generator[None, None, None], config: dict[str, str]):
    
    show_path = False
    current_maze, current_route = next(generate)
    representation(current_maze, config, current_route, show_path)

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
            current_maze, current_route = next(generate)
            representation(current_maze, config, current_route, show_path)

        elif option == "2":
            show_path = not show_path
            representation(current_maze, config, current_route, show_path)

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
        generate = random_generator(config)
        menu(generate, config)
        

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


if __name__ == "__main__":
    main()
