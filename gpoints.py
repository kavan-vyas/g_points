import pygame
import random
import math

"""
gpoints.py(gravity point simulation)
A gravity simulation where particles are attracted to gravity points.
Click to add gravity points that attract particles.
Particles are initialized with random positions and velocities.
Gravity points can be arranged in various patterns.
"""

# Init and config
pygame.init()
WIDTH, HEIGHT = 1920, 1080  
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
pygame.display.set_caption("Gravity Points")

# Particle class
class Particle:
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 2)
        self.vel = pygame.math.Vector2(math.cos(angle), math.sin(angle)) * speed

    def draw(self):
        # draw the particle itself
        pygame.draw.rect(screen, (0, 255, 100), (int(self.pos.x), int(self.pos.y), 2, 2))

    def update(self, gravity_points):
        for gp in gravity_points:
            direction = gp - self.pos
            dist = max(direction.length(), 10)
            force = direction.normalize() * (600 / dist**3)
            self.vel += force
        self.vel *= 1
        self.pos += self.vel



def sine_wave_pattern(count, amp=100, freq=0.01):
    return [pygame.math.Vector2(x, HEIGHT//2 + math.sin(x * freq) * amp) for x in range(0, WIDTH, WIDTH // count)]


def spiral_pattern(center, rings, points_per_ring, spacing=30):
    return [pygame.math.Vector2(center.x + math.cos(i/points_per_ring * 2*math.pi) * spacing * r, 
                               center.y + math.sin(i/points_per_ring * 2*math.pi) * spacing * r) 
            for r in range(1, rings + 1) for i in range(points_per_ring)]



def line_pattern(start, end, count):
    return [start.lerp(end, i / (count - 1)) for i in range(count)]

# Initialise
particles = [Particle(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(1500)]
gravity_points = []

# Choose a pattern here:
gravity_points += sine_wave_pattern(50)

gravity_points += spiral_pattern(pygame.Vector2(WIDTH//2, HEIGHT//2), 10, 20)

gravity_points += line_pattern(pygame.Vector2(500, 200), pygame.Vector2(2000, 200), 30)


# Main loop
running = True
while running:
    screen.fill((0, 0, 0))

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.MOUSEBUTTONDOWN:
            gravity_points.append(pygame.Vector2(e.pos))

    for p in particles:
    
        p.update(gravity_points)
        p.draw()

    for gp in gravity_points:
        pygame.draw.rect(screen, (255, 255, 255), (int(gp.x), int(gp.y), 4, 4))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()