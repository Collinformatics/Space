import pygame
import math


pygame.init()

font = pygame.font.SysFont("comicsans", 16)

# Window parameters
width, height = 1500, 1100
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


class Planet:
    AU = 149.6e6 * 1000
    gravity = 6.67428e-11
    scale = 150 / AU  # 250/AU: 1AU=100 pixels
    timeStep = 3600 * 24  # 1 day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.star = False
        self.distanceToSun = 0

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

        if not self.star:
            # Show distance to the sun
            distance = self.distanceToSun / 1000 # Distance in km
            distanceText = FONT.render(f'{distance:.2e} km', True, white)
            textOutline = FONT.render(f'{distance:.2e} km', 1, limeGreen)
            textOutlineRectangle = textOutline.get_rect(center=(x, y))

            # Add a colored outline
            Window.blit(textOutline, (x - distanceText.get_width() / 2,
                                      y - distanceText.get_height() / 2))
            Window.blit(distanceText, textOutlineRectangle)


    def attraction(self, other):
        otherX, otherY = other.x, other.y
        distanceX = otherX - self.x
        distanceY = otherY - self.y
        distance = math.sqrt(distanceX ** 2 + distanceY ** 2)
        if distance < self.radius + other.radius:
            distance = self.radius + other.radius # Assign proximity limit

        if other.star:
            self.distanceToSun = distance

        force = self.gravity * self.mass * other.mass / distance ** 2
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


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, color=orange, mass=2.98892 * 10 ** 30)
    sun.velX = 0 * 1000
    sun.velY = 0 * 1000
    sun.sun = True

    mercury = Planet(x=-0.532 * Planet.AU, y=0, radius=12,
                     color=pink, mass=2.10 * 10 ** 25)
    mercury.velY = 28.4 * 1000

    venus = Planet(x=0.82 * Planet.AU, y=0, radius=14,
                   color=limeGreen, mass=7.8685 * 10 ** 24)
    venus.velY = -31.02 * 1000

    earth = Planet(x=-1 * Planet.AU, y=0, radius=18,
                   color=cyan, mass=5.9742 * 10 ** 27)
    earth.velY = 43.783 * 1000

    mars = Planet(x=1.524 * Planet.AU, y=0, radius=12,
                   color=red, mass=8.39 * 10 ** 24)
    mars.velY = -24.077 * 1000

    planet7 = Planet(x=-2.11 * Planet.AU, y=0, radius=19,
                   color=white, mass=10.9647 * 10 ** 25)
    planet7.velY = 19.07 * 1000

    planet8 = Planet(x=2.39 * Planet.AU, y=0, radius=16,
                   color=yellow, mass=12.6781 * 10 ** 24)
    planet8.velY = -19.98 * 1000

    planet9 = Planet(x=-3.4 * Planet.AU, y=0, radius=28,
                   color=darkBlue, mass=17.4994 * 10 ** 27)
    planet9.velY = 19.01 * 1000

    planet10 = Planet(x=3.7 * Planet.AU, y=0, radius=38,
                   color=purple, mass=28.5125 * 10 ** 28)
    planet10.velY = -19.01 * 1000

    moon = Planet(x=4.7 * Planet.AU, y=0, radius=10,
                   color=magenta, mass=16.1235 * 10 ** 27)
    moon.velY = -9.83 * 1000

    # Put the plants in a list
    planets = [sun, earth, mars, mercury, venus,
               planet7, planet8, planet9, planet10, moon]

    while run:
        fps = 60  # Run simulation at specified fps
        clock.tick(fps)
        window.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(window)

        pygame.display.update()

    pygame.quit()
main()
