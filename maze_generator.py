from random import randint, seed
from queue import Queue

def is_valid(row: int, col: int, vis: list[list[bool]],
             height: int, width: int) -> bool:
    if (row >= 0 and col >= 0 and row < height and col < width
            and vis[row][col] is False):
        return True
    return False


def get_direction(drow: int, dcol: int) -> str:
    if dcol == 0 and drow == -1:
        return "north"
    elif dcol == 1 and drow == 0:
        return "east"
    elif dcol == 0 and drow == 1:
        return "south"
    else:
        return "west"


def open_wall(maze: list[list[list[int]]], curr: tuple[int, int],
              row: int, col: int, direction: str):
    if direction == "north":
        maze[curr[0]][curr[1]][3] = 0
        maze[row][col][1] = 0
    elif direction == "east":
        maze[curr[0]][curr[1]][2] = 0
        maze[row][col][0] = 0
    elif direction == "south":
        maze[curr[0]][curr[1]][1] = 0
        maze[row][col][3] = 0
    else:
        maze[curr[0]][curr[1]][0] = 0
        maze[row][col][2] = 0


def dfs_rec(maze: list[list[list[int]]], vis: list[list[bool]], height: int,
            width: int, row: int, col: int) -> None:
    drow = [0, 1, 0, -1]
    dcol = [-1, 0, 1, 0]
    vis[row][col] = True
    while drow:
        change = randint(0, len(drow) - 1)
        direction = get_direction(drow[change], dcol[change])
        if is_valid(row + drow[change], col + dcol[change],
                    vis, height, width):
            curr = (row, col)
            row = row + drow[change]
            col = col + dcol[change]
            open_wall(maze, curr, row, col, direction)
            dfs_rec(maze, vis, height, width, row, col)
        drow.pop(change)
        dcol.pop(change)


def bin_to_hex(bin: list[int]) -> str:
    dec = 1 * bin[3] + 2 * bin[2] + 4 * bin[1] + 8 * bin[0]
    hexa = hex(dec)
    return hexa


def output_file(maze: list[list[list[int]]], config: dict[str, str]) -> None:
    with open("output_maze.txt", "w+") as f:
        for x in maze:
            for y in x:
                f.write(bin_to_hex(y)[2:].capitalize())
            f.write("\n")
        f.write(f"\n{config['ENTRY']}")
        f.write(f"\n{config['EXIT']}")


def generator(config: dict[str, str]):
    height = int(config["HEIGHT"])
    width = int(config["WIDTH"])
    vis = [[False for i in range(width)] for j in range(height)]
    maze = [[[1 for _ in range(4)] for y in range(width)]
            for x in range(height)]
    seed(int(config["SEED"]))
    dfs_rec(maze, vis, height, width, 0, 0)
    if config["PERFECT"] == "False":

    output_file(maze, config)


def find_path(maze: )