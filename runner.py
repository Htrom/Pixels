import pygame
from world import World

COLORS = [(200, 0, 0), (0, 200, 0), (0, 200, 200)]


def render_pixels(screen, pixels):
    for pixel in pixels:
        pygame.draw.circle(screen, COLORS[pixel.color], (pixel.pos_x, pixel.pos_y), 1)


pygame.init()

world = World()
screen = pygame.display.set_mode([500, 500])

running = True
FPS = 60
clock = pygame.time.Clock()
while running:
    dt = clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((50, 50, 50))

    world.update_world(dt)
    render_pixels(screen, world.pixels)

    pygame.display.flip()

pygame.quit()
