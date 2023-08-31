import pygame
import time
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

# Define Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 140, 255)
RED = (180, 38, 50)
DARK_GRAY = (80, 78, 80)

# Define Constants
AU = 149.6e6 * 1000
G = 6.67428e-11
SCALE = 250 / AU
TIMESTEP = 3600 * 24

class Planet:
    def __init__(self, x, y, radius, color, mass, initial_velocity=0):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.sun = False
        self.distance_to_sun = 0
        self.x_vel = 0
        self.y_vel = initial_velocity
        self.orbit = []

    def draw(self, win):
        # Calculate the display position
        x = self.x * SCALE + WIDTH / 2
        y = self.y * SCALE + HEIGHT / 2
        
        # Draw the orbit if there are enough points
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * SCALE + WIDTH / 2
                y = y * SCALE + HEIGHT / 2
                updated_points.append((x, y))
            pygame.draw.lines(win, self.color, False, points=updated_points)
        
        # Draw the planet as a circle
        pygame.draw.circle(win, self.color, (int(x), int(y)), self.radius)

    def gravity(self, other):
        # Calculate the gravitational force between two planets
        distance_x = other.x - self.x
        distance_y = other.y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        # Update the position of the planet based on gravitational forces
        total_x = total_y = 0
        for planet in planets:
            if self != planet:
                fx, fy = self.gravity(planet)
                total_x += fx
                total_y += fy
        self.x_vel += total_x / self.mass * TIMESTEP
        self.y_vel += total_y / self.mass * TIMESTEP
        self.x += self.x_vel * TIMESTEP
        self.y += self.y_vel * TIMESTEP
        self.orbit.append((self.x, self.y))

def main():
    clock = pygame.time.Clock()

    # Create planet objects
    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10 ** 30)
    sun.sun = True

    earth = Planet(-1 * AU, 0, 16, BLUE, 5.9742 * 10 ** 24, 29.783 * 1000)
    mars = Planet(-1.524 * AU, 0, 12, RED, 6.39 * 10 ** 23, 24.077 * 1000)
    mercury = Planet(0.387 * AU, 0, 8, DARK_GRAY, 3.30 * 10 ** 23, -47.4 * 1000)
    venus = Planet(0.723 * AU, 0, 14, WHITE, 4.8685 * 10 ** 24, -35.02 * 1000)

    planets = [sun, earth, mars, mercury, venus]

    run = True
    while run:
        WIN.fill((0, 0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        # Update and draw planets
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)
        
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
