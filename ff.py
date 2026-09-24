import time
from PIL import Image, ImageSequence
# Assuming you are using an MLX python wrapper (e.g., standard ctypes wrapper)
from mlx import Mlx


class MlxGifPlayer:
    def __init__(self, mlx_instance, filename):
        self.mlx = mlx_instance
        self.frames = []
        self.frame_durations = []
        self.current_frame = 0
        self.last_update = time.time()

        # Load the GIF using Pillow
        pil_image = Image.open(filename)

        for frame in ImageSequence.Iterator(pil_image):
            # 1. Convert frame to RGBA
            frame_rgba = frame.convert("RGBA")
            width, height = frame_rgba.size

            # 2. Create an empty MLX image buffer
            mlx_img = self.mlx.new_image(width, height)

            # 3. Get the raw image data address
            # (Syntax varies slightly depending on which Python MLX wrapper you use)
            img_data = self.mlx.get_data_addr(mlx_img)

            # 4. Write pixels from Pillow into MLX memory layout
            # (Note: MLX often uses BGRA/ARGB format, adjustments may be needed)
            raw_bytes = frame_rgba.tobytes()
            img_data[:len(raw_bytes)] = raw_bytes

            self.frames.append(mlx_img)
            # Get frame duration in seconds (defaults to 100ms if not specified)
            duration = frame.info.get('duration', 100) / 1000.0
            self.frame_durations.append(duration)

    def update_and_draw(self, win, x, y):
        now = time.time()
        # Check if it's time to transition to the next frame
        if now - self.last_update >= self.frame_durations[self.current_frame]:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update = now

        # Draw the active frame onto the window
        self.mlx.put_image_to_window(
            win, self.frames[self.current_frame], x, y)


# --- Game Setup ---
mlx = Mlx()
win = mlx.new_window(500, 500, "MLX GIF Player")

# Instantiate our custom GIF handler
gif_player = MlxGifPlayer(mlx, "bacman.gif")

# The loop hook runs on every frame iteration


def render_loop():
    mlx.clear_window(win)
    gif_player.update_and_draw(win, 100, 100)
    return 0


mlx.loop_hook(render_loop)
mlx.loop()
