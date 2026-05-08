def full_maze_generation(config: dict[str, str]) -> list[list[list[int]]]:
    maze: list[list[list[int]]] = []
    for x in range(int(config["HEIGHT"])):
        maze.append([])
        for y in range(int(config["WIDTH"])):
            maze[x].append([])
            for _ in range(4):
                maze[x][y].append(1)
    return maze


def dfsRec(maze, visted)
