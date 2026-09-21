from mazegenerator import MazeGenerator



def print_maze(m):
    maze = m.maze
    width = len(maze[0])
    height = len(maze)

    print("+---" * width + "+")

    for y in range(height):
        line = ""

        for x in range(width):
            cell = maze[y][x]

            if cell == 15:
                content = "42 "
            elif (x, y) == m.maze_entry:
                content = " S "
            elif (x, y) == m.maze_exit:
                content = " E "
            else:
                content = "   "

            line += "|" if cell & 8 else " "
            line += content

        line += "|" if maze[y][-1] & 2 else " "

        print(line)

        line = ""

        for x in range(width):
            cell = maze[y][x]

            if cell & 4:
                line += "+---"
            else:
                line += "+   "

        line += "+"
        print(line)


maze = MazeGenerator(
    size=(15, 15),
    seed=34,
    perfect=True
)

print_maze(maze)


# m = MazeGenerator(size=(5, 5), seed=42)

cell = maze.maze[0][0]

m = MazeGenerator(size=(5, 5), seed=42)

for y, row in enumerate(m.maze):
    for x, cell in enumerate(row):
        print((x, y), cell)
# print(maze.maze)
print("Entry:", maze.maze_entry)
print("Exit:", maze.maze_exit)
print("Shortest path:", maze.shortest_path)

for row in maze.maze:
    print(row)
