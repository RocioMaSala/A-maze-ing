from random import choice


def full_maze_generation(height: int, width: int) -> list[list[list[int]]]:
    maze = [[[1 for _ in range(4)] for y in range(width)]
            for x in range(height)]
    return maze


def is_valid(row: int, col: int, vis: list[list[bool]],
             height: int, width: int) -> bool:
    if (row < 0 or col < 0 or row >= height or col >= width):
        return False
    if (vis[row][col]):
        return False
    return True


"""def dfs(maze: list[list[list[int]]], vis: list[list[bool]], height: int,
        width: int):
    drow = [0, 1, 0, -1]
    dcol = [-1, 0, 1, 0]
    st = []
    st.append([0, 0])

    row = 0
    col = 0
    while len(st) > 0:
        curr = choice(st)
        st.remove(curr)
        row = curr[0]
        col = curr[1]

        if not is_valid(row, col, vis, height, width):
            continue

        vis[row][col] = True
        print(maze[row][col], end=" ")

        for i in range(4):
            adjx = row + drow[i]
            adjy = col + dcol[i]
            st.append([adjx, adjy])"""


def dfs(maze: list[list[list[int]]], vis: list[list[bool]], height: int,
        width: int, row: int, col: int) -> list[list[list[int]]]:
    drow = [0, 1, 0, -1]
    dcol = [-1, 0, 1, 0]
    vis[row][col] = True
    while False in vis:

        if not is_valid(row, col, vis, height, width):
            continue

        print(maze[row][col], end=" ")

        for i in range(4):
            adjx = row + drow[i]
            adjy = col + dcol[i]
            st.append([adjx, adjy])
    return maze


def perfect(config: dict[str, str]):
    height = int(config["HEIGHT"])
    width = int(config["WIDTH"])
    vis = [[False for i in range(width)] for j in range(height)]
    maze = full_maze_generation(height, width)
    dfs(maze, vis, height, width, 0, 0)
