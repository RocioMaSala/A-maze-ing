import sys
from mazegen.maze_generator import MazeGenerator
from typing import Generator
from random import seed
from representation import representation


class UsageError(Exception):
    """
    Exception raised when the program is executed with invalid arguments.
    """

    def __init__(self, message: str = "Usage Error: python3 a_maze_ing.py "
                 "config.txt") -> None:
        """
        Initialize the exception with a custom error message.

        Args:
            message (str): Error message to display.

        Returns:
            None
        """
        super().__init__(message)


class ConfigSyntaxError(Exception):
    """
    Exception raised when the configuration file syntax is invalid.
    """

    def __init__(self, message: str = "Invalid config file syntax.") -> None:
        """
        Initialize the exception with a custom error message.

        Args:
            message (str): Error message to display.

        Returns:
            None
        """
        super().__init__(message)


class MissingConfigKeyError(Exception):
    """
    Exception raised when a required key
    is missing from the configuration file.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class ConfigValueError(Exception):
    """
    Exception raised when a configuration key has an invalid value type.
    """

    def __init__(self, message: str) -> None:
        """Initialize the exception with a custom error message.

        Args:
            message (str): Error message to display.
        """
        super().__init__(message)


class MazeError(Exception):
    """
    Custom exception for invalid maze configurations.
    """

    def __init__(self, message: str = "Invalid maze configuration") -> None:
        """
        Initialize the exception with a custom error message.

        Args:
            message (str): Explanation of the error.
                Defaults to "Invalid maze configuration".

        Returns:
            None
        """
        super().__init__(message)


def parse_config_line(line: str) -> tuple[str, str]:
    """
    Parse a configuration line into a key-value pair.

    The expected format is:

        KEY=VALUE

    Args:
        line (str): Configuration line to parse.

    Returns:
        tuple[str, str]: Parsed key and value.

    Raises:
        ConfigSyntaxError: If the line format is invalid.
    """
    parts = line.split("=", 1)
    if len(parts) != 2:
        raise ConfigSyntaxError(f"Invalid config format: '{line.strip()}'. "
                                "Expected 'KEY=VALUE'")
    key, value = parts
    if not key.strip():
        raise ConfigSyntaxError(
            f"Missing key in config line: '{line.strip()}'")
    return key.strip(), value.strip()


def random_generator(
        config: dict[str, str]
    ) -> Generator[
        tuple[list[list[list[int]]], str],
        None,
        None
]:
    """
    Generate mazes indefinitely using different random seeds.

    Args:
        config (dict[str, str]): Maze configuration settings.

    Yields:
        Generator[list[list[list[int]]], str], None, None]: Generator
        yielding tuples
        containing a maze and its corresponding route.
    """

    if int(config["WIDTH"]) <= 7 or int(config["HEIGHT"]) <= 5:
        print("To show the 42, the maze mmust be larger than 7x5")
    try:
        maze_gen = MazeGenerator(config)
    except Exception:
        raise MazeError
    seed_val = 1
    while True:
        seed(seed_val)
        maze, route = maze_gen.generate_maze(config)
        seed_val += 1
        yield maze, route


def menu(
    generate: Generator[
        tuple[list[list[list[int]]], str],
        None, None
    ],
    config: dict[str, str]
) -> None:
    """
    Display and manage the interactive maze menu.

    The menu allows the user to:
    - Generate a new maze
    - Show or hide the solution path
    - Change wall colors
    - Exit the program

    Args:
        generate (Generator[None, None, None]): Generator that
            produces maze data.
        config (dict[str, str]): Maze configuration settings.

    Returns:
        None
    """
    show_path = False
    wall_index = 0
    path_index = 1
    current_maze, current_route = next(generate)
    color_wall = "\033[32m"
    color_path = "\033[33m"
    representation(
        current_maze, config, current_route, show_path, color_wall, color_path
    )

    while True:
        print("== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze wall colors")
        print("4. Quit")

        option = input("Choice? (1-4): ")

        while option not in ("1", "2", "3", "4"):
            option = input("Invalid choice. Try again (1-4): ")

        if option == "1":
            current_maze, current_route = next(generate)
            representation(
                current_maze,
                config,
                current_route,
                show_path,
                color_wall,
                color_path
            )

        elif option == "2":
            show_path = not show_path
            representation(
                current_maze,
                config,
                current_route,
                show_path,
                color_wall,
                color_path
            )

        elif option == "3":
            COLORS = [
                "\033[34m",
                "\033[31m",
                "\033[32m",
                "\033[33m",
                "\033[38;2;255;105;180m"
            ]
            print("Let's rotate the colors")
            color_wall = COLORS[wall_index]
            color_path = COLORS[path_index]
            wall_index = (wall_index + 1) % len(COLORS)
            path_index = (path_index + 1) % len(COLORS)
            representation(
                current_maze,
                config,
                current_route,
                show_path,
                color_wall,
                color_path
            )

        elif option == "4":
            print("Thank you! Bye Bye")
            return


def main() -> None:
    """Execute the maze application main loop.

    The function handles the complete orchestration:
    - Validates command-line arguments.
    - Loads and parses the configuration file.
    - Validates missing keys and values (`PERFECT`).
    - Verifies entry/exit bounds and prevents overlap with the '42' drawing.
    - Triggers the user interactive menu.

    Returns:
        None

    Raises:
        UsageError: If the number of command-line arguments is incorrect
            or the configuration file name is not 'config.txt'.
        FileNotFoundError: If the specified configuration file does not exist.
        MissingConfigKeyError: If any of the required keys (WIDTH, HEIGHT,
            ENTRY, EXIT, OUTPUT_FILE, PERFECT) are missing from the
            configuration file.
        ConfigValueError: If the 'PERFECT' key has a value other than 'True'
        or 'False'.
        EntryExitError: If the entry and exit coordinates are identical.
        EntryError: If the entry coordinates are out of the maze boundaries.
        ExitError: If the exit coordinates are out of the maze boundaries.
        SizeError: If the maze dimensions are 7 or less for width, or 5 or
        less for height.
        ValueError: If there is an error converting coordinate or dimension
            strings into integers.
    """
    try:
        if len(sys.argv) != 2:
            raise UsageError
        if sys.argv[1] != "config.txt":
            raise UsageError
        with open(sys.argv[1]) as file:
            config = {key.strip(): value.strip() for key, value in
                      (parse_config_line(line) for line in file if
                       line.strip() and not line.strip().startswith("#"))}
        REQUIRED_KEYS = {
            "WIDTH",
            "HEIGHT",
            "ENTRY",
            "EXIT",
            "OUTPUT_FILE",
            "PERFECT"
        }
        missing_keys = [
            req_key for req_key in REQUIRED_KEYS if req_key not in config
        ]
        if missing_keys:
            keys_str = ', '.join(missing_keys)
            msg = f"Config Error: Missing required keys:{keys_str}"
            raise MissingConfigKeyError(msg)

        if config["PERFECT"] not in ("True", "False"):
            raise ConfigValueError(
                f"Config Error: Invalid value for 'PERFECT'. "
                f"Expected 'True' or 'False', got '{config['PERFECT']}'."
            )
        generate = random_generator(config)
        menu(generate, config)
    except UsageError as e:
        print(e)
    except FileNotFoundError:
        print("config.txt file not present")
    except MissingConfigKeyError as e:
        print(e)
    except ConfigValueError as e:
        print(e)
    except ConfigSyntaxError as e:
        print(e)
    except ValueError:
        print(
            "ValueError: Entry and exit coordinates must only contain numbers"
        )
    except MazeError:
        return


if __name__ == "__main__":
    main()
