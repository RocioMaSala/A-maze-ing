
COLORS = {
    "blue": "\033[34m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "pink": "\033[38;2;255;105;180m"
}

def get_color_wall():
    color = input(
        "Choose a color for Walls (blue, red, green, yellow, pink): ").strip().lower()
    return COLORS.get(color, COLORS["green"])


def get_color_corner():
    color = input(
        "Choose a color for Corners (blue, red, green, yellow, pink): ").strip().lower()
    return COLORS.get(color, COLORS["blue"])


def coordinates_path(route: str) -> list[tuple[int, int]]:
    directions = []
    for x in route:
        if x == "N":
            directions.append((0, -1))
        elif x == "S":
            directions.append((0, 1))
        elif x == "E":
            directions.append((1, 0))
        elif x == "W":
            directions.append((-1, 0))
    return (directions)

def representation(maze: list[list[list[int]]], config: dict[str, str], route: str) -> None:
    
    COLOR_WALL = get_color_wall()
    COLOR_CORNER = get_color_corner()
    COLOR_42 = "\033[43m"
    COLOR_PATH = "\033[45m"
    COLOR_ENTRY= "\033[1;97;44m"
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
    
    # Para marcar el path del maze
    current_x, current_y = ENTRY
    steps = coordinates_path(route)
    path_coords = [[current_x, current_y]]
    for dx, dy in steps:
        current_x += dx
        current_y += dy
        path_coords.append([current_x, current_y]) 

    # Dibujar paredes y esquinas / inicio y final
    top_line = ""
    for cell in maze[0]:
        top_line += f"{COLOR_CORNER}+{RESET}"
        top_line += f"\033[1m{COLOR_WALL}───{RESET}"
    top_line += f"{COLOR_CORNER}+{RESET}"
    print(top_line)

    # con "enumerate" puedes recorrer lista por índice y por contenido
    for i, row in enumerate(maze):
        middle_line = ""
        for j, cell in enumerate(row):
            is_solid = all(cell)
            middle_line += f"\033[1m{COLOR_WALL}│{RESET}" if cell[0] else " "
            if [j, i] == ENTRY:
                middle_line += f"{COLOR_ENTRY} S {RESET}"
            elif [j, i] == EXIT:
                middle_line += f"{COLOR_EXIT} F {RESET}"
            elif [j, i] in path_coords:
                    middle_line += f"-+-"
            else:
                if is_solid:
                    middle_line += f"{COLOR_42}   {RESET}"    
                else:
                    middle_line += "   "
        middle_line += f"\033[1m{COLOR_WALL}│{RESET}"
        print(middle_line)

        bottom_line = ""
        for cell in row:
            bottom_line += f"{COLOR_CORNER}+{RESET}"
            if is_solid:
                bottom_line += f"{COLOR_42}   {RESET}"
            else:
                bottom_line += f"\033[1m{COLOR_WALL}───{RESET}" if cell[1] else "   "
        bottom_line += f"{COLOR_CORNER}+{RESET}"
        print(bottom_line)






