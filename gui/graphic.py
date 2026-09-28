import pygame
import random
import sys
from models.models import Obj_animation
from mazegenerator import MazeGenerator

pacman_right_frames = [
    pygame.transform.scale(
        pygame.image.load("images/pacman/pacman.png"),
        (35, 35)
    ),
    pygame.transform.scale(
        pygame.image.load("images/pacman/right_1.png"),
        (35, 35)
    ),
    pygame.transform.scale(
        pygame.image.load("images/pacman/right_2.png"),
        (35, 35)
    )
]

pacman_left_frames = [
    pygame.transform.scale(
        pygame.image.load("images/pacman/pacman.png"),
        (35, 35)
    ),
    pygame.transform.scale(
        pygame.image.load("images/pacman/left_1.png"),
        (35, 35)
    ),
    pygame.transform.scale(
        pygame.image.load("images/pacman/left_2.png"),
        (35, 35)
    )
]

pacman_up_frames = [
    pygame.transform.scale(
        pygame.image.load("images/pacman/pacman.png"),
        (35, 35)
    ),
    pygame.transform.scale(
        pygame.image.load("images/pacman/up_1.png"),
        (35, 35)
    ),
    pygame.transform.scale(
        pygame.image.load("images/pacman/up_2.png"),
        (35, 35)
    )
]

pacman_down_frames = [
    pygame.transform.scale(
        pygame.image.load("images/pacman/pacman.png"),
        (35, 35)
    ),
    pygame.transform.scale(
        pygame.image.load("images/pacman/down_1.png"),
        (35, 35)
    ),
    pygame.transform.scale(
        pygame.image.load("images/pacman/down_2.png"),
        (35, 35)
    )
]

ghost_size = (35, 35)

GHOST_FOLDERS = [
    "images/ghosts/light_blue_ghost",
    "images/ghosts/pink_ghost",
    "images/ghosts/red_ghost",
    "images/ghosts/yellow_ghost",
]

ghost_animations = []
for ghost_folder in GHOST_FOLDERS:
    ghost_frames = [
        pygame.transform.scale(
            pygame.image.load(f"{ghost_folder}/{frame_name}"),
            ghost_size
        )
        for frame_name in [
            "up_1.png", "up_2.png",
            "down_1.png", "down_2.png",
            "left_1.png", "left_2.png",
            "right_1.png", "right_2.png"
        ]
    ]
    ghost_animations.append(Obj_animation(ghost_frames))

pellet_frames = [
    pygame.image.load("images/gum/pill.png"),
    pygame.image.load("images/gum/power_pill.png"),
    pygame.image.load("images/gum/pill.png")
]

cell_size = 50
wall_width = 10
tile_size = 2

pacman_right_animation = Obj_animation(pacman_right_frames)
pacman_left_animation = Obj_animation(pacman_left_frames)
pacman_up_animation = Obj_animation(pacman_up_frames)
pacman_down_animation = Obj_animation(pacman_down_frames)

pellet_animation = Obj_animation(pellet_frames)


class Gui:
    def __init__(self):
        self.screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.maze_generator = MazeGenerator((25, 15))
        self.maze_generator.generate()
        self.maze = self.maze_generator.maze
        self.start_game()

    def init(self):
        pygame.init()
        pygame.display.set_caption("Pac-Man")
        self.menu_background = pygame.image.load("start_image.png").convert()
        self.menu_background = pygame.transform.scale(
            self.menu_background,
            (1920, 1080)
        )

    def start_game(self):
        print("Game started!")

        running = True
        cell_size = 40
        wall_width = 4

        maze_width = len(self.maze[0]) * cell_size
        maze_height = len(self.maze) * cell_size

        x_offset = (self.screen.get_width() - maze_width) // 2
        y_offset = (self.screen.get_height() - maze_height) // 2

        player_column = 0
        player_row = 0

        ghost_cells = [
            (
                random.randrange(len(self.maze)),
                random.randrange(len(self.maze[0]))
            )
            for _ in ghost_animations
        ]

        last_move_time = 0
        move_delay = 150

        current_animation = pacman_right_animation

        direction = {
            "up": False,
            "right": True,
            "down": False,
            "left": False
        }

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    if event.key == pygame.K_1:
                        self.maze_generator.generate()
                        self.maze = self.maze_generator.maze
                        player_column = 0
                        player_row = 0

                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        if not (self.maze[player_row][player_column] & 1):
                            current_animation = pacman_up_animation
                            direction = {
                                "up": True,
                                "right": False,
                                "down": False,
                                "left": False
                            }

                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        if not (self.maze[player_row][player_column] & 2):
                            current_animation = pacman_right_animation
                            direction = {
                                "up": False,
                                "right": True,
                                "down": False,
                                "left": False
                            }

                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        if not (self.maze[player_row][player_column] & 4):
                            current_animation = pacman_down_animation
                            direction = {
                                "up": False,
                                "right": False,
                                "down": True,
                                "left": False
                            }

                    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        if not (self.maze[player_row][player_column] & 8):
                            current_animation = pacman_left_animation
                            direction = {
                                "up": False,
                                "right": False,
                                "down": False,
                                "left": True
                            }

            self.screen.fill((0, 0, 0))

            for row_index, maze_row in enumerate(self.maze):
                for column_index, cell in enumerate(maze_row):

                    cell_x = x_offset + column_index * cell_size
                    cell_y = y_offset + row_index * cell_size

                    if cell & 1:
                        pygame.draw.line(
                            self.screen,
                            (0, 0, 255),
                            (cell_x, cell_y),
                            (cell_x + cell_size, cell_y),
                            wall_width
                        )

                    if cell & 2:
                        pygame.draw.line(
                            self.screen,
                            (0, 0, 255),
                            (cell_x + cell_size, cell_y),
                            (cell_x + cell_size, cell_y + cell_size),
                            wall_width
                        )

                    if cell & 4:
                        pygame.draw.line(
                            self.screen,
                            (0, 0, 255),
                            (cell_x, cell_y + cell_size),
                            (cell_x + cell_size, cell_y + cell_size),
                            wall_width
                        )

                    if cell & 8:
                        pygame.draw.line(
                            self.screen,
                            (0, 0, 255),
                            (cell_x, cell_y),
                            (cell_x, cell_y + cell_size),
                            wall_width
                        )

            current_time = pygame.time.get_ticks()

            if current_time - last_move_time > move_delay:
                has_moved = False

                if direction["right"]:
                    if not (self.maze[player_row][player_column] & 2):
                        player_column += 1
                        has_moved = True

                elif direction["up"]:
                    if not (self.maze[player_row][player_column] & 1):
                        player_row -= 1
                        has_moved = True

                elif direction["left"]:
                    if not (self.maze[player_row][player_column] & 8):
                        player_column -= 1
                        has_moved = True

                elif direction["down"]:
                    if not (self.maze[player_row][player_column] & 4):
                        player_row += 1
                        has_moved = True

                if has_moved:
                    last_move_time = current_time

            pacman_x = x_offset + player_column * \
                cell_size + (cell_size - 25) // 2
            pacman_y = y_offset + player_row * \
                cell_size + (cell_size - 30) // 2

            current_animation.update_animation()
            current_animation.draw(self.screen, pacman_x, pacman_y)

            for ghost_animation, (ghost_row, ghost_column) in zip(
                    ghost_animations, ghost_cells):
                ghost_animation.update_animation()
                ghost_x = x_offset + ghost_column * cell_size + \
                    (cell_size - ghost_size[0]) // 2
                ghost_y = y_offset + ghost_row * cell_size + \
                    (cell_size - ghost_size[1]) // 2
                ghost_animation.draw(self.screen, ghost_x, ghost_y)

            pellet_animation.update_animation()
            pellet_animation.draw(self.screen, 1000, 780)

            pygame.display.flip()
            self.clock.tick(60)

    def high_scores(self):
        print("High scores")
        self.screen.fill((0, 0, 0))
        pygame.display.flip()

    def instructions(self):
        print("Instructions")
        self.screen.fill((0, 0, 0))
        pygame.display.flip()

    def any_fun(self):
        running = True

        while running:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_1:
                        self.start_game()

                    elif event.key == pygame.K_2:
                        self.high_scores()

                    elif event.key == pygame.K_3:
                        self.instructions()

                    elif event.key == pygame.K_4:
                        pygame.quit()
                        sys.exit()

            pygame.display.flip()
            self.clock.tick(60)
