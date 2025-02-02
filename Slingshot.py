import math
import pygame
import sys
import time

# User Inputs
inSelectPlanet = 'earth'
inOrbitalDistance = 10**4 # Km to planet
inScreenWidth = 4*10**7 # Screen width in km
inDataFeedInterval = 5 # datapoints/s
inExecuteSlingshot = True

# Initialize simulation
pygame.init()
font = pygame.font.SysFont("comicsans", 16)
FONT = pygame.font.SysFont('Courier New', 20, bold=True)

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
tan = '#A0825A'
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
whiteConsole = '\033[38;2;255;255;255m'
purpleConsole = '\033[38;2;189;22;255m'
redConsole = '\033[91m'
resetColor = '\033[0m'


# Make the planets
planets = {
    "sun": {"radius": 695700, "color": orange, "mass": 1.989 * 10 ** 30},
    "mercury": {"radius": 2440, "color": pink, "mass": 3.285 * 10 ** 23},
    "venus": {"radius": 6052, "color": limeGreen, "mass": 4.867 * 10 ** 24},
    "earth": {"radius": 6371, "color": cyan, "mass": 5.972 * 10 ** 24},
    "mars": {"radius": 3390, "color": red, "mass": 6.39 * 10 ** 23},
    "jupiter": {"radius": 69911, "color": tan, "mass": 1.898 * 10 ** 27},
    "saturn": {"radius": 58232, "color": yellow, "mass": 5.683 * 10 ** 26},
    "uranus": {"radius": 25362, "color": blue, "mass": 8.681 * 10 ** 25},
    "neptune": {"radius": 24622, "color": darkBlue, "mass": 1.024 * 10 ** 26}
}


def makeObject(planetName, posX, posY, scale):
    # Scale the coordinates from km to pixels
    orbitKm = posX
    posX = posX / scale # km / (km/pixel)
    posY = posY / scale

    # Define: Object parameters
    if planetName == 'spaceship':
        mass = 30000  # Mass in kg
        color = '#C3C3C3'
        radiusObjectKm = 2*inScreenWidth/10**2
        radiusObjectPixels = radiusObjectKm / scale
    else:
        try:
            data = planets[planetName]
            mass = data["mass"]
            color = data["color"]
            radiusObjectKm = data["radius"]
            radiusObjectPixels = radiusObjectKm / scale
        except KeyError:
            print(f'Planet name not found: {planetName}')
            sys.exit()

    # Print: Object parameters
    print(f'Simulate: {planetName}\n'
          f'     Mass: {mass:,.2e} kg\n'
          f'     Radius: {radiusObjectKm:,.0f} km\n'
          f'             {radiusObjectPixels:,.0f} pixels\n'
          f'     Position x: {posX}\n'
          f'     Position y: {posY}\n')

    if planetName == 'spaceship':
        print(f'     Orbital Distance: {orbitKm} km\n'
              f'     Orbital Distance: {posX} pixels\n')

    # Create the Planet
    object = SimulateObject(x=posX, y=posY, radius=radiusObjectPixels,
                       color=color, mass=mass)
    return object


class SimulateObject:
    # Simulation parameters
    gravity = 6.67428e-11 # m**3/(kg * s**2)
    timeStep = 10 # 3600  # 1 hr/s: 3600, 1 day/s: 3600 * 24
    simulationScale = inScreenWidth / width
    print(f'\nScreen width: {inScreenWidth:,.0f} km\n'
          f'       Scale: {simulationScale:,.2f} km/pixels\n')

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
        self.vel = 0

    def draw(self, Window):
        x = self.x + width / 2
        y = self.y + height / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x + width / 2
                y = y + height / 2
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

        self.velX += totalFx / self.mass * SimulateObject.timeStep
        self.velY += totalFy / self.mass * SimulateObject.timeStep
        self.vel = math.sqrt(self.velX**2 + self.velY**2)
        self.x += self.velX * SimulateObject.timeStep
        self.y += self.velY * SimulateObject.timeStep
        self.orbit.append((self.x, self.y))


def main(simulationTime, intervalCount=0):
    run = True
    clock = pygame.time.Clock()

    # Create: Planet
    planet = makeObject(planetName=inSelectPlanet,
                       posX=0, posY=0,
                       scale=SimulateObject.simulationScale)

    # Create: Spaceship
    spaceship = makeObject(planetName='spaceship',
                           posX=inScreenWidth / 2,
                           posY=inOrbitalDistance,
                           scale=SimulateObject.simulationScale)

    # Verify objects
    if planet is None or spaceship is None:
        print('ERROR: Object creation failed.\n'
              f'     Planet: {planet}\n'
              f'     Ship: {spaceship}')
        sys.exit()
    print(f"Planet Position: {planet.x}, {planet.y}")
    print(f"Spaceship Position: {spaceship.x}, {spaceship.y}")


    # Select: Simulated objects
    if inExecuteSlingshot:
        plotBoth = 1
        if plotBoth == 1:
            objectsList = [spaceship, planet] # planet,
        else:
            objectsList = [spaceship] # planet,
    else:
        objectsList = [planet]

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

        def getVelocity(objectLabel, interval):
            if objectLabel == 'spaceship':
                print(f'Simulation time: {whiteConsole}{interval:,} s{resetColor}\n'
                      f'     {objectLabel} velocity: '
                      f'{redConsole}{objectSimulate.vel:.2e} m/s{resetColor}')
            else:
                print(f'     {objectLabel} velocity: '
                      f'{purpleConsole}{objectSimulate.vel:.2e} m/s{resetColor}')

        # Update and track objects
        objs = ['spaceship', inSelectPlanet]
        printVel = False
        for index, objectSimulate in enumerate(objectsList):
            currentTime = time.time()
            if currentTime - simulationTime >= inDataFeedInterval:
                intervalCount += inDataFeedInterval
                simulationTime = time.time()
                getVelocity(objectLabel=objs[index], interval=intervalCount)
                printVel = True
            else:
                if printVel:
                    getVelocity(objectLabel=objs[index], interval=intervalCount)
                    printVel = False
            objectSimulate.update_position(objectsList)
            objectSimulate.draw(window)

        pygame.display.update()
    pygame.quit()
main(simulationTime=time.time())
