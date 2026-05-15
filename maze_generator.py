from random import randint, shuffle
from queue import Queue


class MazeGenerator:
    def generate_maze(self, config: dict[str, str]) -> tuple:
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
        if (row >= 0 and col >= 0 and row < height and col < width
                and vis[row][col] is False):
            return True
        return False

    def get_direction(self, drow: int, dcol: int) -> str:
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
        dec = 1 * bin[3] + 2 * bin[2] + 4 * bin[1] + 8 * bin[0]
        hexa = hex(dec)
        return hexa

    def output_file(self, maze: list[list[list[int]]],
                    config: dict[str, str]) -> None:
        with open("output_maze.txt", "w+") as f:
            for x in maze:
                for y in x:
                    f.write(self.bin_to_hex(y)[2:].capitalize())
                f.write("\n")
            f.write(f"\n{config['ENTRY']}")
            f.write(f"\n{config['EXIT']}")

    def draw_42(self, vis: list[list[bool]]) -> None:
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
        if (next[0] >= 0 and next[1] >= 0 and next[0] < height and
            next[1] < width and vis[next[0]][next[1]] is False and
                self.valid_direction(maze, curr, next, direction)):
            return True
        return False

    def bfs(self, maze: list[list[list[int]]], config: dict[str, str],
            vis: list[list[bool]]) -> str:
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
                    with open("output_maze.txt", "a") as f:
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
