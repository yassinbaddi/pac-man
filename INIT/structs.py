import sys
import json
from dataclasses import dataclass, field


@dataclass
class GameConfig:
    highscore_filename: str = "highscores.json"
    lives: int = 3
    pacgum: int = 10
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    seed: int = 42
    level_max_time: int = 90
    # Python 3.10+ allows standard collections for type hints
    levels: list[dict[str, int]] = field(default_factory=list)


@dataclass
class Position:
    x: int
    y: int


class Player:
    def __init__(self, start_pos: Position, config: GameConfig) -> None:
        self.pos: Position = start_pos
        self.lives: int = config.lives
        self.score: int = 0
        self.is_invincible: bool = False
        self.direction: str = "STOP"  # UP, DOWN, LEFT, RIGHT


class Ghost:
    def __init__(self, start_pos: Position, ghost_type: str) -> None:
        self.spawn_pos: Position = start_pos
        self.pos: Position = start_pos
        self.type: str = ghost_type  # Blinky, Pinky, etc.
        self.is_edible: bool = False
        self.direction: str = "STOP"


class GameState:
    def __init__(self, config: GameConfig) -> None:
        self.config: GameConfig = config
        self.current_level: int = 1
        self.time_remaining: int = config.level_max_time
        self.is_paused: bool = False
        self.is_game_over: bool = False

        # These get populated when the maze generator is called
        self.maze_grid: list[list[int]] = []
        self.pacgums_left: int = 0

        # Entities
        self.player: Player | None = None
        self.ghosts: list[Ghost] = []


class Obj_animation:
    def __init__(self, pacman_frames):
        self.frames = pacman_frames
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 10  # This will now trigger every 10 frames

    def update_animation(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self, screen, x, y):
        screen.blit(self.frames[self.current_frame], (x, y))


def init_game(config_path: str) -> GameState:
    try:
        with open(config_path, 'r') as f:
            # Add custom logic here to strip '#' comments
            raw_data = json.load(f)
    except Exception as e:
        # The subject strictly forbids Python tracebacks on error
        print(f"Error loading config: {e}")
        sys.exit(1)

    # Map raw_data to GameConfig, handling missing keys with safe defaults
    config = GameConfig()
    config.highscore_filename = raw_data["highscore_filename"]
    config.lives = raw_data["lives"]
    config.pacgum = raw_data["pacgum"]
    config.points_per_pacgum = raw_data["points_per_pacgum"]
    config.points_per_super_pacgum = raw_data["points_per_super_pacgum"]
    config.points_per_ghost = raw_data["points_per_ghost"]
    config.seed = raw_data["seed"]
    config.level_max_time = raw_data["level_max_time"]
    config.levels = raw_data["level"]
    print(f"Loaded config: {config}")

    return GameState(config)


#init_game("test.json")
