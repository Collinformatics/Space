import math
import pygame
import sys

AU = 1.496e+11  # Astronomical Unit in meters

inSelectPlanet = 'earth'
inSimulationScale = 30  # Large planets: 300, Small planets: 30
inOrbitalDistance = 50*10**1
print(f'Scale: {inSimulationScale:,}\n'
      f'Orbital Distance: {inOrbitalDistance:,} km\n')


pygame.init()

font = pygame.font.SysFont("comicsans", 16)

# Window parameters
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Solar System Simulation')

# Define colors
black = '#000000'
grey = '#989898'
white = '#FFFFFF'
red = '#DC0707'
orange = '#D06507'
yellow = '#FFD918'
limeGreen = '#0FEC05'
green = '#0F5B0F'
cyan = '#17ECEC'
blue = '#054FA4'
darkBlue = '#11387B'
purple = '#3D1075'
pink = '#ED0FF5'
magenta = '#EC0588'
textDistance = white
textOutline = '#930FC4'

FONT = pygame.font.SysFont('Courier New', 20, bold=True)


# Make the planets
planets = {
    "sun": {"radius": 695700, "color": "orange", "mass": 1.989 * 10 ** 30},
    "mercury": {"radius": 2440, "color": "pink", "mass": 3.285 * 10 ** 23},
    "venus": {"radius": 6052, "color": "limeGreen", "mass": 4.867 * 10 ** 24},
    "earth": {"radius": 6371, "color": "cyan", "mass": 5.972 * 10 ** 24},
    "mars": {"radius": 3390, "color": "red", "mass": 6.39 * 10 ** 23},
    "jupiter": {"radius": 69911, "color": "brown", "mass": 1.898 * 10 ** 27},
    "saturn": {"radius": 58232, "color": "gold", "mass": 5.683 * 10 ** 26},
    "uranus": {"radius": 25362, "color": "lightblue", "mass": 8.681 * 10 ** 25},
    "neptune": {"radius": 24622, "color": "darkblue", "mass": 1.024 * 10 ** 26}
}


class Planet:
    gravity = 6.67428e-11
    timeStep = 3600 * 24  # 1 day
    scale = inSimulationScale


    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.distance = 0

        self.velX = 0
        self.velY = 0


    def draw(self, Window):
        x = self.x * Planet.scale + width / 2
        y = self.y * Planet.scale + height / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * Planet.scale + width / 2
                y = y * Planet.scale + height / 2
                updated_points.append((x, y))

            pygame.draw.lines(Window, self.color, False, updated_points, 2)

        pygame.draw.circle(Window, self.color, (x, y), self.radius)


    def attraction(self, other):
        otherX, otherY = other.x, other.y
        distanceX = otherX - self.x
        distanceY = otherY - self.y
        self.distance = math.sqrt(distanceX ** 2 + distanceY ** 2)


        force = self.gravity * self.mass * other.mass / self.distance ** 2
        theta = math.atan2(distanceY, distanceX)
        Fx = math.cos(theta) * force
        Fy = math.sin(theta) * force
        return Fx, Fy


    def update_position(self, planets):
        totalFx = totalFy = 0
        for planet in planets:
            if self == planet:
                continue

            Fx, Fy = self.attraction(planet)
            totalFx += Fx
            totalFy += Fy

        self.velX += totalFx / self.mass * Planet.timeStep
        self.velY += totalFy / self.mass * Planet.timeStep

        self.x += self.velX * Planet.timeStep
        self.y += self.velY * Planet.timeStep
        self.orbit.append((self.x, self.y))



class Spaceship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mass = 30000 # Mass in kg
        self.radius = 30
        self.color = '#C3C3C3'

    def update_position(self, objects):
        # You can add orbital movement logic here, if needed.
        pass

    def draw(self, window):
        pygame.draw.circle(window, self.color,
                           (self.x + 400, self.y + 300),
                           self.radius)



def getPlanet(name):
    if name in planets:
        data = planets[name]
        planet = Planet(x=0, y=0, radius=100,
                        color=data["color"], mass=data["mass"])
        return planet
    else:
        print(f"Planet '{name}' not found.")
        sys.exit()



def main():
    run = True
    clock = pygame.time.Clock()

    # Create: Planet
    planet = getPlanet(inSelectPlanet)
    planet.velX = 0 * 1000
    planet.velY = 0 * 1000

    # Create: Spaceship
    spaceship = Spaceship(x=planet.x + inOrbitalDistance, y=planet.y + inOrbitalDistance)


    # Put the plants in a list
    objects = [planet, spaceship]

    while run:
        fps = 60  # Run simulation at specified fps
        clock.tick(fps)
        window.fill(black)

        # Close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False


        for objectSimulate in objects:
            objectSimulate.update_position(objects)
            objectSimulate.draw(window)

        pygame.display.update()
    pygame.quit()
main()
