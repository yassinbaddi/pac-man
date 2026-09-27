import pygame
import sys
import time
from INIT.structs import Obj_animation
from mazegenerator import MazeGenerator


pygame.init()

pacman_right_frames = [
    pygame.image.load("images/pac-man/right/pacman_open.png"),
    pygame.image.load("images/pac-man/right/pacman_half_open.png"),
    pygame.image.load("images/pac-man/right/pacman_closed.png")
    # pygame.image.load("images/pac-man/pacman_half_open.png"),
    # pygame.image.load("images/pac-man/pacman_closed.png")

]

pacman_left_frames = [
    pygame.image.load("images/pac-man/left/pacman_open.png"),
    pygame.image.load("images/pac-man/left/pacman_half_open.png"),
    pygame.image.load("images/pac-man/left/pacman_closed.png")

]

pacman_up_frames = [
    pygame.image.load("images/pac-man/up/pacman_open.png"),
    pygame.image.load("images/pac-man/up/pacman_half_open.png"),
    pygame.image.load("images/pac-man/up/pacman_closed.png")

]

pacman_down_frames = [
    pygame.image.load("images/pac-man/down/pacman_open.png"),
    pygame.image.load("images/pac-man/down/pacman_half_open.png"),
    pygame.image.load("images/pac-man/down/pacman_closed.png")

]

ori = pygame.image.load("images/ghosts/red.png")
ne = pygame.transform.scale(ori, (25, 25))
ori_1 = pygame.image.load("images/ghosts/cyan.png")
ne_1 = pygame.transform.scale(ori_1, (25, 25))
ori_2 = pygame.image.load("images/ghosts/pinky.png")
ne_2 = pygame.transform.scale(ori_2, (25, 25))
ori_3 = pygame.image.load("images/ghosts/orange.png")
ne_3 = pygame.transform.scale(ori_3, (25, 25))
red_ghost_frames = [
    ne,
    ne_1,
    ne_2,
    ne_3
]

pacgum_frames = [
    pygame.image.load("images/gum/pill.png"),
    pygame.image.load("images/gum/power_pill.png"),
    pygame.image.load("images/gum/pill.png")
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
# original_image = pygame.image.load(
#     "/home/ichtioui/Documents/pac-man/bacman.gif").convert_alpha()

# # Shrink by 50%
# original_image = pygame.transform.scale(original_image, (original_image.get_width() // 2, original_image.get_height() // 2))

pacman_right_image = Obj_animation(pacman_right_frames)
pacman_left_image = Obj_animation(pacman_left_frames)
pacman_up_image = Obj_animation(pacman_up_frames)
pacman_down_image = Obj_animation(pacman_down_frames)
pacgum_image = Obj_animation(pacgum_frames)
red_image = Obj_animation(red_ghost_frames)


def start_game():
    print("Game started!")

    running = True
    cell_size = 40
    wall_width = 4

    maze_width = len(maze.maze[0]) * cell_size
    maze_height = len(maze.maze) * cell_size

    x_offset = (screen.get_width() - maze_width) // 2
    y_offset = (screen.get_height() - maze_height) // 2

    # --- FLOAT POSITION & TARGET GRID POSITIONS ---
    player_x = 0.0  # Current float grid position (e.g. 1.0, 1.1, 1.2)
    player_y = 0.0
    target_col = 0  # Grid cell Pac-Man is moving toward
    target_row = 0

    speed = 0.08  # Fraction of grid cell moved per frame at 60 FPS (higher = faster)

    # Animation timing
    last_anim_time = 0
    anim_delay = 100  # Milliseconds per animation frame

    animation = pacman_right_image
    direction = {"up": False, "right": True, "down": False, "left": False}

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_1:
                    maze.generate()
                    player_x = 0.0
                    player_y = 0.0
                    target_col = 0
                    target_row = 0

                # Set intended direction on keypress
                if event.key == pygame.K_w:
                    direction = {"up": True, "right": False, "down": False, "left": False}
                elif event.key == pygame.K_d:
                    direction = {"up": False, "right": True, "down": False, "left": False}
                elif event.key == pygame.K_s:
                    direction = {"up": False, "right": False, "down": True, "left": False}
                elif event.key == pygame.K_a:
                    direction = {"up": False, "right": False, "down": False, "left": True}

        screen.fill((0, 0, 0))

        # --- DRAW MAZE ---
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

        # --- 1. SET NEXT TARGET CELL WHEN ALIGNED WITH CURRENT TARGET ---
        if abs(player_x - target_col) < 0.01 and abs(player_y - target_row) < 0.01:
            # Lock exact float position to target integer
            player_x = float(target_col)
            player_y = float(target_row)

            # Check wall collisions before advancing target_col / target_row
            if direction["right"] and not (maze.maze[target_row][target_col] & 2):
                target_col += 1
                animation = pacman_right_image
            elif direction["left"] and not (maze.maze[target_row][target_col] & 8):
                target_col -= 1
                animation = pacman_left_image
            elif direction["up"] and not (maze.maze[target_row][target_col] & 1):
                target_row -= 1
                animation = pacman_up_image
            elif direction["down"] and not (maze.maze[target_row][target_col] & 4):
                target_row += 1
                animation = pacman_down_image

        # --- 2. SMOOTHLY INTERPOLATE POSITION TOWARD TARGET ---
        if player_x < target_col:
            player_x = min(target_col, player_x + speed)
        elif player_x > target_col:
            player_x = max(target_col, player_x - speed)

        if player_y < target_row:
            player_y = min(target_row, player_y + speed)
        elif player_y > target_row:
            player_y = max(target_row, player_y - speed)

        # --- 3. ANIMATION TIMING ---
        current_time = pygame.time.get_ticks()
        if (current_time - last_anim_time) > anim_delay:
            animation.update_animation()
            red_image.update_animation()
            pacgum_image.update_animation()
            last_anim_time = current_time

        # --- 4. DRAWING AT FLOAT-DERIVED PIXEL POSITIONS ---
        px = x_offset + player_x * cell_size + (cell_size - 25) // 2
        py = y_offset + player_y * cell_size + (cell_size - 30) // 2

        animation.draw(screen, px, py)
        red_image.draw(screen, 1430, 780)
        pacgum_image.draw(screen, 1000, 780)

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
