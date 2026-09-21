import pygame
import sys
from mazegenerator import MazeGenerator

pygame.init()

screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
# screen = pygame.display.set_mode((700, 400), pygame.RESIZABLE)
pygame.display.set_caption("Pac-Man")

clock = pygame.time.Clock()

menu_background = pygame.image.load("start_image.png").convert()
ichtioui_background = pygame.image.load("ichtioui.jpeg").convert()
menu_background = pygame.transform.scale(menu_background, (1920, 1080))
ichtioui_background = pygame.transform.scale(ichtioui_background, (1920, 1080))



maze = MazeGenerator((25, 15))

maze.generate()
print(maze.maze)

# exit()

cell_size = 50
wall_width = 10

maze_width = len(maze.maze[0]) * cell_size
maze_height = len(maze.maze) * cell_size

x_offset = (screen.get_width() - maze_width) // 2
y_offset = (screen.get_height() - maze_height) // 2

def start_game():
    print("Game started!")

    running = True

    cell_size = 40
    wall_width = 4  # Adjust thickness as needed

    maze_width = len(maze.maze[0]) * cell_size
    maze_height = len(maze.maze) * cell_size

    x_offset = (screen.get_width() - maze_width) // 2
    y_offset = (screen.get_height() - maze_height) // 2

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Clear screen every frame
        screen.fill((0, 0, 0))

        # Draw continuous maze walls using lines
        for row, line in enumerate(maze.maze):
            for col, cell in enumerate(line):

                x = x_offset + col * cell_size
                y = y_offset + row * cell_size

                if cell & 1:  # TOP
                    pygame.draw.line(screen, (0, 0, 255), (x, y), (x + cell_size, y), wall_width)

                if cell & 2:  # RIGHT
                    pygame.draw.line(screen, (0, 0, 255), (x + cell_size, y), (x + cell_size, y + cell_size), wall_width)

                if cell & 4:  # BOTTOM
                    pygame.draw.line(screen, (0, 0, 255), (x, y + cell_size), (x + cell_size, y + cell_size), wall_width)

                if cell & 8:  # LEFT
                    pygame.draw.line(screen, (0, 0, 255), (x, y), (x, y + cell_size), wall_width)

        pygame.display.flip()
        clock.tick(60)



start_game()

# def high_scores():
#     print("High scores")
#     screen.fill((0, 0, 0))
#     pygame.display.flip()


# def instructions():
#     print("Instructions")
#     screen.fill((0, 0, 0))
#     pygame.display.flip()

# def any_fun():
#     running = True

#     while running:
#         for event in pygame.event.get():

#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()

#             if event.type == pygame.KEYDOWN:

#                 if event.key == pygame.K_1:
#                     start_game()

#                 if event.key == pygame.K_2:
#                     high_scores()

#                 if event.key == pygame.K_3:
#                     instructions()

#                 if event.key == pygame.K_4:
#                     pygame.quit()
#                     sys.exit()

#         screen.blit(menu_background, (0, 0))
#         pygame.display.flip()
#         clock.tick(60)


# any_fun()
