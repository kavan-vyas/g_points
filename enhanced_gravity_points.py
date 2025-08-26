import pygame
import random
import math
import colorsys

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 2560, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Premium Gravity Simulation")
clock = pygame.time.Clock()

# Fonts
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 32)
font_small = pygame.font.Font(None, 24)

# Colors
BACKGROUND = (8, 12, 20)
PARTICLE_COLORS = [
    (100, 200, 255),  # Light blue
    (255, 150, 100),  # Orange
    (150, 255, 150),  # Light green
    (255, 200, 150),  # Peach
    (200, 150, 255),  # Purple
]
GRAVITY_POINT_COLOR = (255, 100, 100)
UI_BACKGROUND = (20, 25, 35)
UI_BORDER = (60, 70, 85)
UI_TEXT = (200, 210, 220)
SLIDER_ACTIVE = (100, 150, 255)
BUTTON_HOVER = (80, 90, 110)

class Particle:
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        # Random initial velocity
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(0.5, 2.0)
        self.vel = pygame.math.Vector2(math.cos(angle), math.sin(angle)) * speed
        
        # Visual properties
        self.color = random.choice(PARTICLE_COLORS)
        self.size = random.uniform(1.5, 3.0)
        self.trail = []
        self.max_trail_length = 15
        self.life = 1.0
        
    def update(self, gravity_points):
        # Apply gravity from all gravity points
        for gp in gravity_points:
            direction = gp - self.pos
            dist = max(direction.length(), 15)  # Minimum distance to prevent extreme forces
            
            # Gravitational force calculation
            force_magnitude = 800 / (dist ** 1.5)  # Adjusted for smoother motion
            if direction.length() > 0:
                force = direction.normalize() * force_magnitude
                self.vel += force * 0.016  # Frame-rate independent
        
        # Apply velocity damping for smoother motion
        self.vel *= 0.985
        
        # Update position
        self.pos += self.vel
        
        # Add to trail
        self.trail.append(self.pos.copy())
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
        
        # Wrap around screen edges
        if self.pos.x < 0:
            self.pos.x = WIDTH
        elif self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT
        elif self.pos.y > HEIGHT:
            self.pos.y = 0
    
    def draw(self, screen):
        # Draw trail
        for i, trail_pos in enumerate(self.trail):
            alpha = (i / len(self.trail)) * 0.3
            trail_size = self.size * (i / len(self.trail)) * 0.5
            if trail_size > 0.5:
                color_with_alpha = (*self.color, int(255 * alpha))
                trail_surface = pygame.Surface((trail_size * 2, trail_size * 2), pygame.SRCALPHA)
                pygame.draw.circle(trail_surface, color_with_alpha, 
                                 (trail_size, trail_size), trail_size)
                screen.blit(trail_surface, (trail_pos.x - trail_size, trail_pos.y - trail_size))
        
        # Draw main particle with glow effect
        glow_size = self.size * 3
        glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
        glow_color = (*self.color, 30)
        pygame.draw.circle(glow_surface, glow_color, (glow_size, glow_size), glow_size)
        screen.blit(glow_surface, (self.pos.x - glow_size, self.pos.y - glow_size))
        
        # Main particle
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), int(self.size))

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, label):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val
        self.label = label
        self.dragging = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            rel_x = event.pos[0] - self.rect.x
            self.val = self.min_val + (rel_x / self.rect.width) * (self.max_val - self.min_val)
            self.val = max(self.min_val, min(self.max_val, self.val))
    
    def draw(self, screen):
        # Slider background
        pygame.draw.rect(screen, UI_BORDER, self.rect, border_radius=5)
        pygame.draw.rect(screen, UI_BACKGROUND, self.rect.inflate(-4, -4), border_radius=3)
        
        # Slider handle
        handle_x = self.rect.x + (self.val - self.min_val) / (self.max_val - self.min_val) * self.rect.width
        handle_rect = pygame.Rect(handle_x - 8, self.rect.y - 5, 16, self.rect.height + 10)
        pygame.draw.rect(screen, SLIDER_ACTIVE, handle_rect, border_radius=8)
        
        # Label and value
        label_text = font_small.render(f"{self.label}: {int(self.val)}", True, UI_TEXT)
        screen.blit(label_text, (self.rect.x, self.rect.y - 25))

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()
    
    def draw(self, screen):
        color = BUTTON_HOVER if self.hovered else UI_BACKGROUND
        pygame.draw.rect(screen, UI_BORDER, self.rect, border_radius=8)
        pygame.draw.rect(screen, color, self.rect.inflate(-4, -4), border_radius=6)
        
        text_surface = font_medium.render(self.text, True, UI_TEXT)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class GravitySimulation:
    def __init__(self):
        self.particles = []
        self.gravity_points = []
        self.target_particle_count = 500
        
        # UI Elements
        self.particle_slider = Slider(50, 50, 200, 20, 0, 2000, 500, "Particles")
        self.reset_button = Button(270, 40, 120, 40, "Reset", self.reset_gravity_points)
        self.clear_button = Button(400, 40, 120, 40, "Clear All", self.clear_all)
        
        # Background stars
        self.stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT), 
                      random.uniform(0.5, 2.0)) for _ in range(200)]
        
    def reset_gravity_points(self):
        self.gravity_points.clear()
        
    def clear_all(self):
        self.gravity_points.clear()
        self.particles.clear()
        
    def update_particle_count(self):
        current_count = len(self.particles)
        target_count = int(self.particle_slider.val)
        
        if current_count < target_count:
            # Add particles
            for _ in range(target_count - current_count):
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                self.particles.append(Particle(x, y))
        elif current_count > target_count:
            # Remove particles
            self.particles = self.particles[:target_count]
    
    def draw_background(self, screen):
        # Simple gradient background using rects for better performance
        screen.fill(BACKGROUND)
        
        # Draw stars
        for star_x, star_y, star_size in self.stars:
            alpha = 100 + int(55 * math.sin(pygame.time.get_ticks() * 0.001 + star_x * 0.01))
            alpha = max(50, min(255, alpha))  # Clamp alpha to valid range
            star_color = (alpha, alpha, alpha)
            if star_size >= 1:  # Only draw stars with valid size
                pygame.draw.circle(screen, star_color, (int(star_x), int(star_y)), max(1, int(star_size)))
    
    def draw_gravity_points(self, screen):
        for i, gp in enumerate(self.gravity_points):
            # Pulsing effect
            pulse = 1 + 0.3 * math.sin(pygame.time.get_ticks() * 0.005 + i)
            size = int(8 * pulse)
            
            # Outer glow
            glow_size = size * 3
            glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            glow_color = (*GRAVITY_POINT_COLOR, 50)
            pygame.draw.circle(glow_surface, glow_color, (glow_size, glow_size), glow_size)
            screen.blit(glow_surface, (gp.x - glow_size, gp.y - glow_size))
            
            # Main gravity point
            pygame.draw.circle(screen, GRAVITY_POINT_COLOR, (int(gp.x), int(gp.y)), size)
            pygame.draw.circle(screen, (255, 255, 255), (int(gp.x), int(gp.y)), size, 2)
    
    def draw_ui(self, screen):
        # Semi-transparent UI background
        ui_surface = pygame.Surface((WIDTH, 100), pygame.SRCALPHA)
        ui_surface.fill((*UI_BACKGROUND, 180))
        screen.blit(ui_surface, (0, 0))
        
        # Draw UI elements
        self.particle_slider.draw(screen)
        self.reset_button.draw(screen)
        self.clear_button.draw(screen)
        
        # Instructions
        instructions = [
            "Click to add gravity points",
            f"Gravity Points: {len(self.gravity_points)}",
            f"Active Particles: {len(self.particles)}"
        ]
        
        for i, instruction in enumerate(instructions):
            text = font_small.render(instruction, True, UI_TEXT)
            screen.blit(text, (WIDTH - 300, 20 + i * 25))
    
    def run(self):
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if click is on UI elements first
                    if event.pos[1] > 100:  # Below UI area
                        self.gravity_points.append(pygame.math.Vector2(event.pos))
                
                # Handle UI events
                self.particle_slider.handle_event(event)
                self.reset_button.handle_event(event)
                self.clear_button.handle_event(event)
            
            # Update particle count based on slider
            self.update_particle_count()
            
            # Update particles
            for particle in self.particles:
                particle.update(self.gravity_points)
            
            # Draw everything
            self.draw_background(screen)
            
            # Draw particles
            for particle in self.particles:
                particle.draw(screen)
            
            # Draw gravity points
            self.draw_gravity_points(screen)
            
            # Draw UI
            self.draw_ui(screen)
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    simulation = GravitySimulation()
    simulation.run()