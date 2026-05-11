from queue import Queue


def get_direction(drow: int, dcol: int) -> str:
    if dcol == 0 and drow == -1:
        return "N"
    elif dcol == 1 and drow == 0:
        return "E"
    elif dcol == 0 and drow == 1:
        return "S"
    else:
        return "W"


def valid_direction(maze: list[list[list[int]]], curr: tuple[int, int],
                    next: tuple[int, int], direction: str) -> bool:
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


def is_valid(next: tuple[int, int], curr: tuple[int, int], vis: list[list[bool]],
             height: int, width: int, direction: str, maze:
             list[list[list[int]]]) -> bool:
    if (next[0] >= 0 and next[1] >= 0 and next[0] < height and next[1] < width
            and vis[next[0]][next[1]] is False and valid_direction(maze, curr, next, direction)):
        return True
    return False


def bfs(maze: list[list[list[int]]], config: dict[str, str], vis: list[list[bool]]) -> None:
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    entry_rev = tuple(int(x) for x in config["ENTRY"].split(","))
    exit_rev = tuple(int(x) for x in config["EXIT"].split(","))
    entry = entry_rev[::-1]
    exit = exit_rev[::-1]
    height = int(config["HEIGHT"])
    width = int(config["WIDTH"])
    vis[entry[0]][entry[1]] = True
    queue = Queue()
    queue.put((entry, []))
    while not queue.empty():
        (cell, path) = queue.get()
        for dx, dy in directions:
            direction = get_direction(dx, dy)
            next_cell = (cell[0]+dx, cell[1]+dy)
            if next_cell == exit and valid_direction(maze, cell, next_cell, direction):
                path = path + [direction]
                with open("output_maze.txt", "a") as f:
                    route = "".join(path)
                    f.write("\n")
                    f.write(route)
                    return
            if is_valid(next_cell, cell, vis, height, width, direction, maze):
                vis[next_cell[0]][next_cell[1]] = True
                queue.put((next_cell, path + [direction]))
