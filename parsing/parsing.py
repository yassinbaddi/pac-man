from models.models import GameState, GameConfig
import sys
import json


class Config():

    def __init__(self, config_path):
        self.config_path = config_path

    def init_game(self) -> GameState:
        try:
            data = ""

            with open(self.config_path, "r") as f:
                in_command = False
                for line in f.readlines():
                    if in_command:
                        if line.strip().endswith("*/"):
                            in_command = False
                        continue
                    if line.strip().startswith("#") or line.strip().startswith("//"):
                        continue
                    elif line.strip().startswith("/*"):
                        in_command = True
                        continue
                    elif in_command:
                        continue
                    else:
                        data += line
            raw_data = json.loads(data)
        except Exception as e:
            sys.exit(1)

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

        return GameState(config)
