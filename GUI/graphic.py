import pygame
import sys
from INIT.structs import Obj_animation
from mazegenerator import MazeGenerator


pygame.init()

pacman_frames = [
    pygame.image.load("images/pac-man/pacman_open.png"),
    pygame.image.load("images/pac-man/pacman_half_open.png"),
    pygame.image.load("images/pac-man/pacman_closed.png")  # Changed to .png
    # pygame.image.load("images/pac-man/pacman_half_open.png"),
    # pygame.image.load("images/pac-man/pacman_closed.png")

]

screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
pygame.display.set_caption("Pac-Man")

clock = pygame.time.Clock()

menu_background = pygame.image.load("start_image.png").convert()
ichtioui_background = pygame.image.load("ichtioui.jpeg").convert()
menu_background = pygame.transform.scale(menu_background, (1920, 1080))
ichtioui_background = pygame.transform.scale(ichtioui_background, (1920, 1080))

maze = MazeGenerator((25, 15))
maze.generate()
print(maze.maze)

cell_size = 50
wall_width = 10
TILE_SIZE = 2

# Make sure this path is correct for your machine
original_image = pygame.image.load(
    "/home/ichtioui/Documents/pac-man/bacman.gif").convert_alpha()

# Shrink by 50%
pacman_image = Obj_animation(pacman_frames)


def start_game():
    print("Game started!")

    running = True
    cell_size = 40
    wall_width = 4  # Adjust thickness as needed

    maze_width = len(maze.maze[0]) * cell_size
    maze_height = len(maze.maze) * cell_size

    x_offset = (screen.get_width() - maze_width) // 2
    y_offset = (screen.get_height() - maze_height) // 2

    # Track Pac-Man's position on the grid instead of raw pixels
    player_col = 0
    player_row = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                # Generate new maze and reset position
                if event.key == pygame.K_1:
                    maze.generate()
                    player_col = 0
                    player_row = 0

                # --- WASD MOVEMENT LOGIC ---
                # The maze generator uses bitwise flags for walls: 1=TOP, 2=RIGHT, 4=BOTTOM, 8=LEFT
                # We check the current cell's walls before allowing movement.

                if event.key == pygame.K_w:  # UP
                    if not (maze.maze[player_row][player_col] & 1):
                        player_row -= 1

                elif event.key == pygame.K_d:  # RIGHT
                    if not (maze.maze[player_row][player_col] & 2):
                        player_col += 1

                elif event.key == pygame.K_s:  # DOWN
                    if not (maze.maze[player_row][player_col] & 4):
                        player_row += 1

                elif event.key == pygame.K_a:  # LEFT
                    if not (maze.maze[player_row][player_col] & 8):
                        player_col -= 1

        # Clear screen every frame
        screen.fill((0, 0, 0))

        # Draw continuous maze walls using lines
        for row, line in enumerate(maze.maze):
            for col, cell in enumerate(line):

                x = x_offset + col * cell_size
                y = y_offset + row * cell_size

                if cell & 1:  # TOP
                    pygame.draw.line(screen, (0, 0, 255), (x, y),
                                     (x + cell_size, y), wall_width)

                if cell & 2:  # RIGHT
                    pygame.draw.line(screen, (0, 0, 255), (x + cell_size, y),
                                     (x + cell_size, y + cell_size), wall_width)

                if cell & 4:  # BOTTOM
                    pygame.draw.line(screen, (0, 0, 255), (x, y + cell_size),
                                     (x + cell_size, y + cell_size), wall_width)

                if cell & 8:  # LEFT
                    pygame.draw.line(screen, (0, 0, 255), (x, y),
                                     (x, y + cell_size), wall_width)

        # Draw Pac-Man (Moved outside the wall loop for performance)
        # Calculate pixel position based on grid row/col and center the image inside the cell
        px = x_offset + player_col * cell_size + \
            (cell_size - 25) // 2
        py = y_offset + player_row * cell_size + \
            (cell_size - 30) // 2

        # screen.blit(pacman_image, (px, py))
        pacman_image.update_animation()
        pacman_image.draw(screen, px, py)
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
