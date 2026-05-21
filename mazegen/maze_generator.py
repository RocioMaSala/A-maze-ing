from random import randint, shuffle
from queue import Queue


class EntryError(Exception):
    """
    Exception raised when entry coordinates are outside maze boundaries.
    """

    def __init__(self, message: str = "Entry coordinates must be within maze"
                 " boundaries.") -> None:
        """
        Initialize the exception with a custom error message.

        Args:
            message (str): Error message to display.

        Returns:
            None
        """
        super().__init__(message)


class ExitError(Exception):
    """
    Exception raised when exit coordinates are outside maze boundaries.
    """

    def __init__(self, message: str = "Exit coordinates must be within maze"
                 " boundaries.") -> None:
        """
        Initialize the exception with a custom error message.

        Args:
            message (str): Error message to display.

        Returns:
            None
        """
        super().__init__(message)


class EntryExitError(Exception):
    """
    Exception raised when entry and exit coordinates are identical.
    """

    def __init__(self, message: str = "Entry Exit Error: Entry and exit "
                 "points need to be in different positions.") -> None:
        """
        Initialize the exception with a custom error message.

        Args:
            message (str): Error message to display.

        Returns:
            None
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


class MazeGenerator:
    """
    A manager class responsible for generating and solving customized mazes.

    Supports depth-first search generation, custom structural layouts (such as
    embedding an easter-egg shape), loop-injection for imperfect mazes, and
    breadth-first search pathfinding.
    """

    def __init__(self, config: dict[str, str]) -> None:
        """
        Initialize and validate the maze configuration.

        Args:
            config (dict[str, str]): A dictionary containing maze settings
                                     with keys:
                - "ENTRY": Comma-separated x,y coordinates for the entry point.
                - "EXIT": Comma-separated x,y coordinates for the exit point.
                - "WIDTH": The width of the maze.
                - "HEIGHT": The height of the maze.

        Raises:
            EntryExitError: If entry and exit coordinates are identical.
            EntryError: If the entry point is outside the maze boundaries.
            ExitError: If the exit point is outside the maze boundaries.
            SizeError: If the maze dimensions are too small (width <= 7 or
                       height <= 5).
            MazeError: If any of the above errors are caught during validation.

        Returns:
            None
        """
        try:
            if len(config["ENTRY"].split(",")) != 2:
                raise EntryError("Entry coordintes syntax must be a,b")
            if len(config["EXIT"].split(",")) != 2:
                raise ExitError("Exit coordintes syntax must be a,b")
            ENTRY = [int(x.strip()) for x in config["ENTRY"].split(",")]
            EXIT = [int(x.strip()) for x in config["EXIT"].split(",")]
            if ENTRY == EXIT:
                raise EntryExitError
            if (ENTRY[0] >= int(config["WIDTH"]) or ENTRY[0] < 0 or
                    ENTRY[1] >= int(config["HEIGHT"]) or ENTRY[1] < 0):
                raise EntryError

            if (EXIT[0] >= int(config["WIDTH"]) or EXIT[0] < 0 or
                    EXIT[1] >= int(config["HEIGHT"]) or EXIT[1] < 0):
                raise ExitError

            if int(config["WIDTH"]) > 7 and int(config["HEIGHT"]) > 5:
                self.entry_exit_in_42(config)
        except (EntryError, ExitError, EntryExitError) as e:
            print(e)
            raise MazeError
        except ValueError:
            print(
                "ValueError: Non numeric characters included "
                "in numeric positions")
            raise MazeError

    def entry_exit_in_42(self, config: dict[str, str]) -> None:
        """
        Verify if the entry or exit points fall inside the '42' text drawing
        layout.

        Args:
            config (dict[str, str]): Maze configuration settings.

        Raises:
            EntryExitError: If the entry or exit coordinates overlap with the
            predefined '42' coordinate masks.
        """
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
            raise EntryExitError("Entry Exit Error: Entry cannot be "
                                 "inside the 42 drawing")
        if (exit_x - x, exit_y - y) in targets:
            raise EntryExitError("Entry Exit Error: Exits cannot be "
                                 "inside the 42 drawing")

    def generate_maze(self, config: dict[str, str]) -> tuple:
        """
        Generate a maze grid and find its solution pathway based on a
        configuration layout.

        Parameters:
        config (dict[str, str]): Configuration settings containing string
                                 values for 'HEIGHT', 'WIDTH', 'PERFECT',
                                 'OUTPUT_FILE', 'ENTRY', and 'EXIT'.

        Returns:
        tuple: A tuple containing:
            - maze (list[list[list[int]]]): The generated 3D maze grid array.
            - route (str): The string sequence of directions
              ('N', 'E', 'S', 'W') representing the solved path.
        """
        height = int(config["HEIGHT"])
        width = int(config["WIDTH"])
        vis = [[False for i in range(width)] for j in range(height)]
        maze = [[[1 for _ in range(4)] for y in range(width)]
                for x in range(height)]
        if int(config["WIDTH"]) > 7 and int(config["HEIGHT"]) > 5:
            self.draw_42(vis)
        self.dfs_rec(maze, vis, height, width, 0, 0)
        self.output_file(maze, config)
        vis = [[False for i in range(width)] for j in range(height)]
        route = ""
        if config["PERFECT"] == "True":
            route = self.bfs(maze, config, vis)
        elif config["PERFECT"] == "False":
            route = self.imperfect_maze(maze, config, vis)
        return maze, route

    def is_valid_dfs(self, row: int, col: int, vis: list[list[bool]],
                     height: int, width: int) -> bool:
        """
        Determine if a target coordinate is valid for DFS traversal.

        Parameters:
        row (int): The row index of the target cell.
        col (int): The column index of the target cell.
        vis (list[list[bool]]): 2D matrix tracking visited states.
        height (int): The total height boundary of the maze grid.
        width (int): The total width boundary of the maze grid.

        Returns:
        bool: True if the cell is inside boundaries and has not been visited,
              False otherwise.
        """
        if (row >= 0 and col >= 0 and row < height and col < width
                and vis[row][col] is False):
            return True
        return False

    def get_direction(self, drow: int, dcol: int) -> str:
        """
        Convert a coordinate delta movement vector into a cardinal direction
        character string.

        Parameters:
        drow (int): Row offset value (-1, 0, or 1).
        dcol (int): Column offset value (-1, 0, or 1).

        Returns:
        str: A single character ('N', 'E', 'S', or 'W') corresponding to the
             vector.
        """
        if dcol == 0 and drow == -1:
            return "N"
        elif dcol == 1 and drow == 0:
            return "E"
        elif dcol == 0 and drow == 1:
            return "S"
        else:
            return "W"

    def open_wall(self, maze: list[list[list[int]]], curr: tuple[int, int],
                  row: int, col: int, direction: str) -> None:
        """
        Carve an opening through a wall between two adjacent cells in the maze
        matrix.

        Parameters:
        maze (list[list[list[int]]]): The 3D matrix representing the maze
                                      framework.
        curr (tuple[int, int]): Coordinates (row, col) of the current origin
                                cell.
        row (int): Row index of the target neighboring cell.
        col (int): Column index of the target neighboring cell.
        direction (str): Cardinal direction string ('N', 'E', 'S', or 'W')
                         leading out of curr.

        Returns:
        None
        """
        if direction == "N":
            maze[curr[0]][curr[1]][3] = 0
            maze[row][col][1] = 0
        elif direction == "E":
            maze[curr[0]][curr[1]][2] = 0
            maze[row][col][0] = 0
        elif direction == "S":
            maze[curr[0]][curr[1]][1] = 0
            maze[row][col][3] = 0
        else:
            maze[curr[0]][curr[1]][0] = 0
            maze[row][col][2] = 0

    def dfs_rec(self, maze: list[list[list[int]]], vis: list[list[bool]],
                height: int, width: int, row: int, col: int) -> None:
        """
        Generate a maze structure recursively utilizing a Randomized
        Depth-First Search.

        Parameters:
        maze (list[list[list[int]]]): The 3D matrix tracking structural cell
                                      walls.
        vis (list[list[bool]]): 2D matrix tracking visited coordinates.
        height (int): Total height boundary of the maze grid.
        width (int): Total width boundary of the maze grid.
        row (int): The current cell's row index.
        col (int): The current cell's column index.

        Returns:
        None
        """
        drow = [0, 1, 0, -1]
        dcol = [-1, 0, 1, 0]
        vis[row][col] = True
        while drow:
            change = randint(0, len(drow) - 1)
            direction = self.get_direction(drow[change], dcol[change])
            if self.is_valid_dfs(row + drow[change], col + dcol[change],
                                 vis, height, width):
                new_row = row + drow[change]
                new_col = col + dcol[change]
                self.open_wall(maze, (row, col), new_row, new_col, direction)
                self.dfs_rec(maze, vis, height, width, new_row, new_col)
            drow.pop(change)
            dcol.pop(change)

    def bin_to_hex(self, bin: list[int]) -> str:
        """
        Convert a 4-bit wall representation list into its hexadecimal string
        equivalent.

        Parameters:
        bin (list[int]): A list containing four binary integers [W, S, E, N]
                         where 1 is wall, 0 is path.

        Returns:
        str: Hexadecimal string prefixed with '0x' representing the decimal
             value of the bits.
        """
        dec = 1 * bin[3] + 2 * bin[2] + 4 * bin[1] + 8 * bin[0]
        hexa = hex(dec)
        return hexa

    def output_file(self, maze: list[list[list[int]]],
                    config: dict[str, str]) -> None:
        """
        Serialize the maze architecture matrix and configuration points to an
        external file.

        Parameters:
        maze (list[list[list[int]]]): The 3D array layout tracking the maze
                                      grid.
        config (dict[str, str]): Configuration tracking metadata values
                                 including 'OUTPUT_FILE', 'ENTRY', and 'EXIT'.

        Returns:
        None
        """
        with open(config["OUTPUT_FILE"], "w+") as f:
            for x in maze:
                for y in x:
                    f.write(self.bin_to_hex(y)[2:].capitalize())
                f.write("\n")
            f.write(f"\n{config['ENTRY']}")
            f.write(f"\n{config['EXIT']}")

    def draw_42(self, vis: list[list[bool]]) -> None:
        """
        Carve out an unvisitable mask block mimicking the shape of the number
        '42' in the center grid.

        Parameters:
        vis (list[list[bool]]): 2D matrix tracking visited states to be
                                modified.

        Returns:
        None
        """
        y = round((len(vis) - 5) / 2)
        x = round((len(vis[0]) - 7) / 2)
        vis[y][x] = True
        vis[y+1][x] = True
        vis[y+2][x] = True
        vis[y+2][x+1] = True
        vis[y+2][x+2] = True
        vis[y+3][x+2] = True
        vis[y+4][x+2] = True
        vis[y][x+4] = True
        vis[y][x+5] = True
        vis[y][x+6] = True
        vis[y+1][x+6] = True
        vis[y+2][x+6] = True
        vis[y+2][x+5] = True
        vis[y+2][x+4] = True
        vis[y+3][x+4] = True
        vis[y+4][x+4] = True
        vis[y+4][x+5] = True
        vis[y+4][x+6] = True

    def valid_direction(self, maze: list[list[list[int]]],
                        curr: tuple[int, ...], next: tuple[int, int],
                        direction: str) -> bool:
        """
        Check if a corridor layout allows transition through shared borders
        without wall interference.

        Parameters:
        maze (list[list[list[int]]]): The 3D matrix representing the maze map
                                      layout.
        curr (tuple[int, ...]): Spatial tuple indexes (row, col) of the
                                current origin cell.
        next (tuple[int, int]): Spatial tuple indexes (row, col) of the
                                targeted neighbor cell.
        direction (str): The direction vector key string ('N', 'E', 'S', 'W')
                         connecting both nodes.

        Returns:
        bool: True if both cells have mutual open space connections (zeros) at
              the border index, False otherwise.
        """
        if direction == "N" and maze[curr[0]][curr[1]][3] == 0 and maze[
                next[0]][next[1]][1] == 0:
            return True
        elif direction == "E" and maze[curr[0]][curr[1]][2] == 0 and maze[
                next[0]][next[1]][0] == 0:
            return True
        elif direction == "S" and maze[curr[0]][curr[1]][1] == 0 and maze[
                next[0]][next[1]][3] == 0:
            return True
        elif direction == "W" and maze[curr[0]][curr[1]][0] == 0 and maze[
                next[0]][next[1]][2] == 0:
            return True
        return False

    def is_valid_bfs(self, next: tuple[int, int], curr: tuple[int, ...],
                     vis: list[list[bool]], height: int, width: int,
                     direction: str, maze: list[list[list[int]]]) -> bool:
        """
        Validate if an unvisited neighboring cell can be transitioned into
        during BFS execution.

        Parameters:
        next (tuple[int, int]): Index tuple (row, col) representing the
                                destination grid coordinates.
        curr (tuple[int, ...]): Index tuple (row, col) representing the source
                                grid coordinates.
        vis (list[list[bool]]): 2D matrix tracking visited locations during
                                runtime.
        height (int): Total row array ceiling height boundary value.
        width (int): Total column array frame width boundary value.
        direction (str): Cardinal tracking identification string map key
                         ('N', 'E', 'S', 'W').
        maze (list[list[list[int]]]): Core 3D configuration data layout
                                      mapping walls.

        Returns:
        bool: True if the adjacent space resides within the map parameters,
              remains unvisited, and has open paths.
        """
        if (next[0] >= 0 and next[1] >= 0 and next[0] < height and
            next[1] < width and vis[next[0]][next[1]] is False and
                self.valid_direction(maze, curr, next, direction)):
            return True
        return False

    def bfs(self, maze: list[list[list[int]]], config: dict[str, str],
            vis: list[list[bool]]) -> str:
        """
        Calculate the shortest path solution across a maze via Breadth-First
        Search traversal.

        Parameters:
        maze (list[list[list[int]]]): Multi-dimensional tracking database map
                                      matching wall bits.
        config (dict[str, str]): Setup variables providing keys 'ENTRY',
                                 'EXIT', 'HEIGHT', 'WIDTH', and 'OUTPUT_FILE'.
        vis (list[list[bool]]): 2D configuration grid reflecting visited cells.

        Returns:
        str: Formatted string processing directions (e.g., 'EESNW')
             representing the solution, or empty string if unreachable.
        """
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        entry_rev = tuple(int(x) for x in config["ENTRY"].split(","))
        exit_rev = tuple(int(x) for x in config["EXIT"].split(","))
        entry = entry_rev[::-1]
        exit = exit_rev[::-1]
        height = int(config["HEIGHT"])
        width = int(config["WIDTH"])
        vis[entry[0]][entry[1]] = True
        shortest_length = None
        queue: Queue[tuple[tuple[int, ...], list[str], set]] = Queue()
        queue.put((entry, [], {entry}))
        while not queue.empty():
            (cell, path, path_vis) = queue.get()
            if shortest_length is not None and len(path) >= shortest_length:
                continue
            for drow, dcol in directions:
                direction = self.get_direction(drow, dcol)
                next_cell = (cell[0] + drow, cell[1] + dcol)
                if (next_cell == exit and
                        self.valid_direction(maze, cell, next_cell,
                                             direction)):
                    candidate = path + [direction]
                    if shortest_length is None:
                        shortest_length = len(candidate)
                    route_str = "".join(candidate)
                    with open(config["OUTPUT_FILE"], "a") as f:
                        f.write("\n")
                        f.write(route_str)
                        f.write("\n")
                    return route_str
                if self.is_valid_bfs(next_cell, cell, vis, height,
                                     width, direction, maze):
                    vis[next_cell[0]][next_cell[1]] = True
                    queue.put((next_cell, path + [direction], path_vis))
        return ""

    def is_wall(self, curr_cell: list[int], next_cell: list[int],
                direction: tuple[int, int]) -> bool:
        """
        Verify if an obstacle blocking passage exists between two targeted
        coordinates.

        Parameters:
        curr_cell (list[int]): Binary wall list properties tracking the origin
                               index space.
        next_cell (list[int]): Binary wall list properties tracking the
                               recipient index space.
        direction (tuple[int, int]): A step representation vector tracking
                                     delta offsets (drow, dcol).

        Returns:
        bool: True if a wall is actively established between the specified
              borders, False otherwise.
        """
        dir_str = self.get_direction(direction[0], direction[1])
        if dir_str == "N":
            if curr_cell[3] == 1 and next_cell[1] == 1:
                return True
        elif dir_str == "E":
            if curr_cell[2] == 1 and next_cell[0] == 1:
                return True
        elif dir_str == "S":
            if curr_cell[1] == 1 and next_cell[3] == 1:
                return True
        else:
            if curr_cell[0] == 1 and next_cell[2] == 1:
                return True
        return False

    def add_wall(self, maze: list[list[list[int]]], x: int, y: int,
                 dir: tuple[int, int]) -> None:
        """
        Erect an active shared obstacle dividing two neighboring cells.

        Parameters:
        maze (list[list[list[int]]]): Target matrix where adjustments occur.
        x (int): Horizontal spatial column indicator.
        y (int): Vertical spatial row indicator.
        dir (tuple[int, int]): Direction representation vector tracking
                               (drow, dcol).

        Returns:
        None
        """
        dir_str = self.get_direction(dir[0], dir[1])
        if dir_str == "N":
            maze[y][x][3] = 1
            maze[y + dir[0]][x + dir[1]][1] = 1
        elif dir_str == "E":
            maze[y][x][2] = 1
            maze[y + dir[0]][x + dir[1]][0] = 1
        elif dir_str == "S":
            maze[y][x][1] = 1
            maze[y + dir[0]][x + dir[1]][3] = 1
        else:
            maze[y][x][0] = 1
            maze[y + dir[0]][x + dir[1]][2] = 1

    def remove_wall(self, maze: list[list[list[int]]], x: int, y: int,
                    dir: tuple[int, int]) -> None:
        """
        Demolish a shared partition barrier to link two neighboring cells.

        Parameters:
        maze (list[list[list[int]]]): Target matrix where adjustments occur.
        x (int): Horizontal spatial column indicator.
        y (int): Vertical spatial row indicator.
        dir (tuple[int, int]): Direction representation vector tracking
                               (drow, dcol).

        Returns:
        None
        """
        dir_str = self.get_direction(dir[0], dir[1])
        if dir_str == "N":
            maze[y][x][3] = 0
            maze[y+dir[0]][x+dir[1]][1] = 0
        elif dir_str == "E":
            maze[y][x][2] = 0
            maze[y+dir[0]][x+dir[1]][0] = 0
        elif dir_str == "S":
            maze[y][x][1] = 0
            maze[y+dir[0]][x+dir[1]][3] = 0
        else:
            maze[y][x][0] = 0
            maze[y+dir[0]][x+dir[1]][2] = 0

    def is_in_42(self, height: int, width: int, cell_x: int,
                 cell_y: int) -> bool:
        """
        Identify whether a specific coordinate falls inside the bounds of the
        '42' mask.

        Parameters:
        height (int): Maze framework height limitation scale.
        width (int): Maze framework width limitation scale.
        cell_x (int): Targeted column testing value coordinate.
        cell_y (int): Targeted row testing value coordinate.

        Returns:
        bool: True if the coordinates coincide inside the masked area
              boundaries, False otherwise.
        """
        y = round((height - 5) / 2)
        x = round((width - 7) / 2)

        targets = {
            (0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (3, 2), (4, 2),
            (0, 4), (0, 5), (0, 6), (1, 6), (2, 6),
            (2, 5), (2, 4), (3, 4), (4, 4), (4, 5), (4, 6)
        }

        y_offset = cell_y - y
        x_offset = cell_x - x
        if (y_offset, x_offset) in targets:
            return True
        return False

    def creates_large_open_area(self, maze: list[list[list[int]]], x: int,
                                y: int, dir: tuple[int, int],
                                height: int, width: int) -> bool:
        """
        Determine if knocking down a wall creates a wide open space larger
        than standard corridors.

        This functions by test-removing a wall, inspecting if an unbroken 2x2
        clear space loop is introduced, and then reconstructing the wall
        configuration before returning.

        Parameters:
        maze (list[list[list[int]]]): Main 3D tracking map matrix structure.
        x (int): Horizontal cell column axis component.
        y (int): Vertical cell row axis component.
        dir (tuple[int, int]): Traversal step trajectory configuration array
                               mapping (drow, dcol).
        height (int): Total height limits constraint index parameter.
        width (int): Total width limits constraint index parameter.

        Returns:
        bool: True if removing the wall violates corridor design by
              constructing an open 2x2 grid, False otherwise.
        """
        self.remove_wall(maze, x, y, dir)
        ny, nx = y + dir[0], x + dir[1]
        cells_to_check = [(y, x), (ny, nx)]
        for cy, cx in cells_to_check:
            for dy in range(-1, 1):
                for dx in range(-1, 1):
                    top_y, top_x = cy + dy, cx + dx
                    if 0 <= top_y < height - 1 and 0 <= top_x < width - 1:
                        if (maze[top_y][top_x][2] == 0 and
                                maze[top_y][top_x + 1][0] == 0 and
                                maze[top_y][top_x][1] == 0 and
                                maze[top_y + 1][top_x][3] == 0 and
                                maze[top_y][top_x + 1][1] == 0 and
                                maze[top_y + 1][top_x + 1][3] == 0 and
                                maze[top_y + 1][top_x][2] == 0 and
                                maze[top_y + 1][top_x + 1][0] == 0):
                            self.add_wall(maze, x, y, dir)
                            return True
        self.add_wall(maze, x, y, dir)
        return False

    def imperfect_maze(self, maze: list[list[list[int]]],
                       config: dict[str, str], vis: list[list[bool]]) -> str:
        """
        Inject alternative pathways and loops into a maze by randomly knocking
        down non-critical walls.

        Parameters:
        maze (list[list[list[int]]]): Core multi-dimensional list tracking
                                      structural configurations.
        config (dict[str, str]): Setup parameters configuration map providing
                                 dimension settings and exit coordinates.
        vis (list[list[bool]]): 2D tracking system tracking visited items.

        Returns:
        str: Route character map matching the shortest solution path
             calculated over the modified grid.
        """
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        height = int(config["HEIGHT"])
        width = int(config["WIDTH"])

        removable = []
        for y in range(height):
            for x in range(width):
                if self.is_in_42(height, width, x, y):
                    continue
                for drow, dcol in directions:
                    ny, nx = y + drow, x + dcol
                    if (0 <= ny < height and 0 <= nx < width and
                            not self.is_in_42(height, width, nx, ny)):
                        if self.is_wall(maze[y][x], maze[ny][nx],
                                        (drow, dcol)):
                            if not self.creates_large_open_area(maze, x, y,
                                                                (drow, dcol),
                                                                height, width):
                                removable.append((x, y, drow, dcol))

        shuffle(removable)
        num_to_remove = max(1, len(removable) // 10)

        for i in range(num_to_remove):
            if i < len(removable):
                x, y, drow, dcol = removable[i]
                self.remove_wall(maze, x, y, (drow, dcol))

        vis = [[False] * width for _ in range(height)]
        return self.bfs(maze, config, vis)
