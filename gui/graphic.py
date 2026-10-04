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

super_pellet_frames = [
    pygame.transform.scale(
        pygame.image.load("images/gum/pill_new.png"), (24, 24)
    ),
    pygame.transform.scale(
        pygame.image.load("images/gum/2013.png"), (24, 24)
    ),
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

pellet_frames = pygame.transform.scale(
    pygame.image.load("images/gum/pill_new.png"),
    (10, 10)
),

def get_neighbors(x, y, maze):
                neighbors = set()

                # Up
                if not (maze[y][x] & 1):
                    neighbors.add((x, y - 1))

                # Right
                if not (maze[y][x] & 2):
                    neighbors.add((x + 1, y))

                # Down
                if not (maze[y][x] & 4):
                    neighbors.add((x, y + 1))

                # Left
                if not (maze[y][x] & 8):
                    neighbors.add((x - 1, y))

                return neighbors


def bfs(end, x, y, maze):
                from collections import deque

                start = (x, y)
                dp = deque([start])

                visited = {start}
                came_from = {start: None}

                while dp:
                    cur = dp.popleft()

                    if cur == end:
                        break

                    for neighbor in get_neighbors(*cur, maze):
                        if neighbor not in visited:
                            visited.add(neighbor)
                            dp.append(neighbor)
                            came_from[neighbor] = cur

                if end not in came_from:
                    return []

                path = []
                cur = end

                while cur is not None:
                    path.append(cur)
                    cur = came_from[cur]

                path.reverse()
                return path

first_x = 0
first_y = 0
cell_size = 50
wall_width = 10
tile_size = 2
all_past = set()

pacman_right_animation = Obj_animation(pacman_right_frames)
pacman_left_animation = Obj_animation(pacman_left_frames)
pacman_up_animation = Obj_animation(pacman_up_frames)
pacman_down_animation = Obj_animation(pacman_down_frames)

pellet_animation = Obj_animation(pellet_frames)
super_pellet_animation = Obj_animation(super_pellet_frames)


class Gui:
    def __init__(self, config):
        self.screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.maze_generator = MazeGenerator((25, 20), entry_cell=(5, 5), seed=12)
        self.maze_generator.generate()
        self.maze = self.maze_generator.maze
        self.config = config.config
        self.pacman_pos_x = 0
        self.pacman_pos_y = 0
        self.ghost_x = 0
        self.ghost_y = 0
        self.init()
        self.start_game()

    def init(self):
        pygame.init()
        pygame.display.set_caption("Pac-Man")
        # self.menu_background = pygame.image.load("start_image.png").convert()
        # self.menu_background = pygame.transform.scale(
        #     self.menu_background,
        #     (1920, 1080)
        # )
        self.pacman_font = pygame.font.Font("PressStart2P-Regular.ttf", 24)

    def start_game(self):
        running = True
        cell_size = 40
        wall_width = 4

        maze_width = len(self.maze[0]) * cell_size
        maze_height = len(self.maze) * cell_size

        x_offset = (self.screen.get_width() - maze_width) // 2
        y_offset = (self.screen.get_height() - maze_height) // 2

        player_column, player_row = self.maze_generator.maze_entry

        last_move_time = 0
        move_delay = 150
        visited_cells = set()

        current_animation = pacman_right_animation

        direction = {
            "up": False,
            "right": True,
            "down": False,
            "left": False
        }



        ghost_path_index = 0
        ghost_last_move_time = 0
        ghost_move_delay = 300

        while running:
            ghost_path = bfs((self.pacman_pos_x, self.pacman_pos_y), self.ghost_x, self.ghost_y, self.maze)
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
                        player_column = self.maze_generator.entry_cell[0]
                        player_row = self.maze_generator.entry_cell[1]

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
            max_row = len(self.maze[0]) - 1
            max_column = len(self.maze) - 1
            i = 0

            for row_index, maze_row in enumerate(self.maze):
                for column_index, cell in enumerate(maze_row):
                    cell_x = x_offset + column_index * cell_size
                    cell_y = y_offset + row_index * cell_size

                    if i == 0:
                        first_x = cell_x
                        first_y = cell_y
                        i = 1

                    _x = x_offset + max_row * cell_size
                    _y = y_offset + max_column * cell_size

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

                    if not (cell & 1 and cell & 2 and cell & 4 and cell & 8):
                        if not (player_column == column_index and player_row == row_index):
                            visited_cells.add((player_column, player_row))
                            if not (column_index, row_index) in visited_cells:
                                pellet_animation.update_animation()
                                pellet_animation.draw(
                                    self.screen, cell_x + 17, cell_y + 16
                                )
                    super_pellet_animation.update_animation(4000)

                    if column_index == 0 and row_index == 0:
                        super_pellet_animation.draw(
                            self.screen, cell_x + 11, cell_y + 11
                        )

                    # if column_index == 0 and row_index == 0:
                    #     super_pellet_animation.draw(
                    #         self.screen, _x + 7, _y + 7
                    #     )

                    # if column_index == 0 and row_index == 0:
                    #     super_pellet_animation.draw(
                    #         self.screen, cell_x + 11, cell_y + 11
                    #     )

                    # if column_index == _y and row_index == _x:
                    #     super_pellet_animation.draw(
                    #         self.screen, cell_x + 11, cell_y + 11
                    #     )
            text_surface = self.pacman_font.render(f"HIGH SCORE: {(len(visited_cells) - 3 ) * self.config.points_per_pacgum}", False, (255, 255, 255))
            self.screen.blit(text_surface, (10, 10))

            super_pellet_animation.draw(
                self.screen, first_x + 11, cell_y + 11
            )

            super_pellet_animation.draw(
                self.screen, cell_x + 11, first_y + 11
            )
            super_pellet_animation.draw(
                self.screen, cell_x + 11, cell_y + 11
            )
            visited_cells.add((first_x, cell_y))
            visited_cells.add((cell_x, first_y))
            visited_cells.add((cell_x, cell_y))

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
            self.pacman_pos_x, self.pacman_pos_y = player_column, player_row
            pacman_x = x_offset + player_column * \
                cell_size + (cell_size - 25) // 2
            pacman_y = y_offset + player_row * \
                cell_size + (cell_size - 30) // 2

            current_animation.update_animation()
            current_animation.draw(self.screen, pacman_x, pacman_y)



            # ij = 0
            # past = (-1, -1)
            # if ij == 0:
            #     path = bfs((4, 4), 0, 0)
            #     ij += 1
            # for x, y in path:
            #     if (x, y) != past:
            #         all_past.add(past)
            #     if (x, y) not in all_past:
            #         for ghost_animation in ghost_animations:
            #             ghost_animation.update_animation()
            #             ghost_x = x_offset + x * cell_size + \
            #                 (cell_size - ghost_size[0]) // 2
            #             ghost_y = y_offset + y * cell_size + \
            #                 (cell_size - ghost_size[1]) // 2
            #             ghost_animation.draw(self.screen, ghost_x, ghost_y)
            #             pygame.display.flip()
            #         past = (x, y)current_time = pygame.time.get_ticks()

            if (ghost_path and current_time - ghost_last_move_time >= ghost_move_delay):
                if ghost_path_index < len(ghost_path) - 1:
                    ghost_path_index += 1
                ghost_last_move_time = current_time
            ghost_x_cell, ghost_y_cell = ghost_path[ghost_path_index]
            self.ghost_x = ghost_x_cell
            self.ghost_y = ghost_y_cell
            ghost_x = ( x_offset + ghost_x_cell * cell_size + (cell_size - ghost_size[0]) // 2)
            ghost_y = ( y_offset + ghost_y_cell * cell_size + (cell_size - ghost_size[1]) // 2)


            for ghost_animation in ghost_animations:
                ghost_animation.update_animation()
                ghost_animation.draw(
                    self.screen,
                    ghost_x,
                    ghost_y
                )



            # pellet_animation.update_animation()
            # pellet_animation.draw(self.screen, 1000, 780)
            # print((len(visited_cells) - 3) * self.config.points_per_pacgum)

            pygame.display.flip()
            self.clock.tick(60)

    def high_scores(self):
        self.screen.fill((0, 0, 0))
        pygame.display.flip()

    def instructions(self):
        self.screen.fill((0, 0, 0))
        pygame.display.flip()

    def any_fun(self):

        while True:
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
