def coordinates_path(route: str) -> list[tuple[int, int]]:
    """
    Convert a route string into coordinate movements.

    Each character in the route represents a cardinal direction:
    - "N" → north
    - "S" → south
    - "E" → east
    - "W" → west

    The function translates these directions into `(x, y)` coordinate
    displacements.

    Args:
        route (str): String containing movement directions.

    Returns:
        list[tuple[int, int]]: List of coordinate displacements
        corresponding to the given route.
    """
    directions = []
    index = 0
    for x in route:
        if x == "N":
            directions.append((0, -1))
        elif x == "S":
            directions.append((0, 1))
        elif x == "E":
            directions.append((1, 0))
        elif x == "W":
            directions.append((-1, 0))
        index += 1
    return (directions)


def get_path_char(prev: tuple[int, int], next: tuple[int, int]) -> str:
    """Determine the ASCII character to represent a path segment.

    Selects a box-drawing character (e.g., straight line or turn) based on
    the incoming (prev) and outgoing (next) movement directions.

    Args:
        prev (tuple[int, int]): The preceding movement vector, or None.
        next (tuple[int, int]): The subsequent movement vector, or None.

    Returns:
        str: A 3-character string containing the visual representation of
            the path segment.
    """
    if next is None and next is not None:
        return " | " if next in [(0, -1), (0, 1)] else "───"
    if next is None and prev is not None:
        return " | " if prev in [(0, -1), (0, 1)] else "───"
    if next is None or next is None:
        return " # "
    if prev in [(0, -1), (0, 1)] and next in [(0, -1), (0, 1)]:
        return " | "
    if prev in [(1, 0), (-1, 0)] and next in [(1, 0), (-1, 0)]:
        return "───"
    if ((prev == (-1, 0) or next == (1, 0)) and
       (prev == (0, 1) or next == (0, -1))):
        return " └─"
    if ((prev == (1, 0) or next == (-1, 0)) and
       (prev == (0, 1) or next == (0, -1))):
        return "─┘ "
    if ((prev == (-1, 0) or next == (1, 0)) and
       (prev == (0, -1) or next == (0, 1))):
        return " ┌─"
    if ((prev == (1, 0) or next == (-1, 0)) and
       (prev == (0, -1) or next == (0, 1))):
        return "─┐ "
    return " * "


def representation(
        maze: list[list[list[int]]],
        config: dict[str, str],
        route: str, show_path: bool, color_wall: str,
        color_path: str
        ) -> None:
    """
    Display a graphical representation of the maze in the terminal.

    The function renders maze walls, entry and exit points, solid blocks,
    and optionally the solution path using ASCCI escape color codes.

    Args:
        maze (list[list[list[int]]]): Matrix representing the maze
            structure and walls.
        config (dict[str, str]): Dictionary containing maze configuration,
            including entry and exit coordinates.
        route (str): String describing the movement path through the maze.
        show_path (bool): If True, the solution path is displayed.
        color_wall (str): ASCII color code used to draw maze walls.

    Returns:
        None
    """
    COLOR_CORNER = "\033[34m"
    COLOR_42 = "\033[43m"
    COLOR_ENTRY = "\033[1;97;44m"
    COLOR_EXIT = "\033[1;97;41m"
    RESET = "\033[0m"
    ENTRY_STR = config["ENTRY"].split(",")
    EXIT_STR = config["EXIT"].split(",")
    ENTRY = []
    EXIT = []

    for x in ENTRY_STR:
        ENTRY.append(int(x))
    for x in EXIT_STR:
        EXIT.append(int(x))

    current_x, current_y = ENTRY
    steps = coordinates_path(route)
    path_coords = [[current_x, current_y]]
    for dx, dy in steps:
        current_x += dx
        current_y += dy
        path_coords.append([current_x, current_y])

    path_directions: dict[tuple, tuple] = {}
    for i, coord in enumerate(path_coords):
        if i > 0:
            prev_dir = steps[i-1]
        else:
            prev_dir = None
        if i < len(steps):
            next_dir = steps[i]
        else:
            next_dir = None
        path_directions[tuple(coord)] = (prev_dir, next_dir)

    top_line = ""
    for cell in maze[0]:
        top_line += f"{COLOR_CORNER}+{RESET}"
        top_line += f"\033[1m{color_wall}───{RESET}"
    top_line += f"{COLOR_CORNER}+{RESET}"
    print(top_line)

    for i, row in enumerate(maze):
        middle_line = ""
        is_solid = False
        for j, cell in enumerate(row):
            is_solid = all(cell)
            middle_line += f"\033[1m{color_wall}│{RESET}" if cell[0] else " "
            if [j, i] == ENTRY:
                middle_line += f"{COLOR_ENTRY} S {RESET}"
            elif [j, i] == EXIT:
                middle_line += f"{COLOR_EXIT} F {RESET}"
            elif show_path and [j, i] in path_coords:
                prev_dir, next_dir = path_directions.get(
                    tuple([j, i]), (None, None)
                    )
                path_char = get_path_char(prev_dir, next_dir)
                middle_line += f"{color_path}{path_char}{RESET}"
            elif is_solid:
                middle_line += f"{COLOR_42}   {RESET}"
            else:
                middle_line += "   "
        middle_line += f"\033[1m{color_wall}│{RESET}"
        print(middle_line)

        bottom_line = ""
        for cell in row:
            bottom_line += f"{COLOR_CORNER}+{RESET}"
            if is_solid:
                bottom_line += f"{COLOR_42}   {RESET}"
            else:
                bottom_line += (
                    f"\033[1m{color_wall}───{RESET}"
                    if cell[1]
                    else "   "
                )
        bottom_line += f"{COLOR_CORNER}+{RESET}"
        print(bottom_line)
