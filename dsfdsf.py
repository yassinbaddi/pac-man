import pygame
import sys

# 1. Always initialize Pygame first!
pygame.init()

# 2. Load the frames (make sure to convert that .gif to a .png!)
pacman_frames = [
    pygame.image.load("images/pac-man/pacman_open.png"),
    pygame.image.load("images/pac-man/pacman_half_open.png"),
    pygame.image.load("images/pac-man/pacman_closed.png")  # Changed to .png
    # pygame.image.load("images/pac-man/pacman_half_open.png"),
    # pygame.image.load("images/pac-man/pacman_closed.png")

]


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


# Setup screen and clock
screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
clock = pygame.time.Clock()

# 3. Create the player OUTSIDE the loop!
player = Obj_animation(pacman_frames)

while True:
    # 4. Handle events (prevents window from freezing)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 5. Clear the screen (Black background)
    screen.fill((0, 0, 0))

    # 6. Update animation and draw
    player.update_animation()
    player.draw(screen, 100, 100)

    # 7. Push the drawing to the actual monitor
    pygame.display.flip()

    # 8. Cap the game at 60 Frames Per Second so it doesn't melt your CPU
    clock.tick(60)
