import math
import pygame
import sys
import time

# User Input 1:
inSelectPlanet = 'earth'
inSpaceshipVel = 3*10**5 # km/s
inSpaceshipTrajectory = 9.8 # Theta

# User Input 2:
inSimulationSpeed = 4*10**-3 # 1 s/s = 1, 1 hr/s = 3600, 1 day/s = 3600 * 24
inScreenWidth = 2*10**5 # Screen width in km
inOrbitalDistanceX = inScreenWidth / 3 # Km to planet
inOrbitalDistanceY = inScreenWidth / 10
print(inOrbitalDistanceY)
inScaleObjects = 10**0
inDataFeedInterval = 2 # datapoints/s

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
greenLime = '#0FEC05'
green = '#0F5B0F'
cyan = '#17ECEC'
blue = '#054FA4'
darkBlue = '#11387B'
purple = '#3D1075'
pink = '#ED0FF5'
magenta = '#EC0588'
textColorSimulation = greenLime
textOutline = '#930FC4'
whiteConsole = '\033[38;2;255;255;255m'
purpleConsole = '\033[38;2;189;22;255m'
redConsole = '\033[91m'
resetColor = '\033[0m'


# Make the planets
planets = {
    "sun": {"radius": 695700, "color": orange, "mass": 1.989 * 10 ** 30},
    "mercury": {"radius": 2440, "color": pink, "mass": 3.285 * 10 ** 23},
    "venus": {"radius": 6052, "color": greenLime, "mass": 4.867 * 10 ** 24},
    "earth": {"radius": 6371, "color": cyan, "mass": 5.972 * 10 ** 24},
    "mars": {"radius": 3390, "color": red, "mass": 6.39 * 10 ** 23},
    "jupiter": {"radius": 69911, "color": tan, "mass": 1.898 * 10 ** 27},
    "saturn": {"radius": 58232, "color": yellow, "mass": 5.683 * 10 ** 26},
    "uranus": {"radius": 25362, "color": blue, "mass": 8.681 * 10 ** 25},
    "neptune": {"radius": 24622, "color": darkBlue, "mass": 1.024 * 10 ** 26}
}


def makeObject(planetName, scale, posX, posY):
    # Define: Object parameters
    if planetName == 'spaceship':
        mass = 10000  # Mass in kg
        color = '#C3C3C3'
        radiusObjectKm = 4000
        posX += radiusObjectKm
        if abs(posX) > posX:
            posX += radiusObjectKm
        else:
            posX -= radiusObjectKm
    else:
        try:
            data = planets[planetName]
            mass = data["mass"]
            color = data["color"]
            radiusObjectKm = data["radius"]
        except KeyError:
            print(f'Planet name not found: {planetName}')
            sys.exit()
    radiusObject = radiusObjectKm / scale

    # Define: Object parameters
    orbitKm = posX
    posX = posX / scale  # km / (km/pixel)
    posY = posY / scale

    # Print: Object parameters
    print(f'Simulate: {planetName}\n'
          f'     Mass: {mass:,.2e} kg\n'
          f'     Radius: {radiusObjectKm:,.0f} km\n'
          f'     Radius: { radiusObject:,.0f} pixels\n')

    # Create the Planet
    object = SimulateObject(label=planetName, x=posX, y=posY,
                            radius=radiusObject, color=color, mass=mass)
    return object


class SimulateObject:
    # Simulation parameters
    gravity = 6.67428e-11 # m**3/(kg * s**2)
    timeStep = inSimulationSpeed
    simulationScale = inScreenWidth / width
    print(f'\nScreen width: {inScreenWidth:,.0f} km\n'
          f'       Scale: {simulationScale:,.2f} km/pixels\n')

    def __init__(self, label, x, y, radius, color, mass):
        self.name = label
        self.x = x
        self.xKm = x * inScreenWidth / width
        self.y = y
        self.yKm = y * inScreenWidth / width
        self.radius = radius * inScaleObjects
        self.color = color
        self.mass = mass
        self.orbit = []
        self.distance = 0
        self.distanceMin = 10**99
        self.gravity = 0
        self.gravityMax = 0
        self.thetaRadians = math.radians(inSpaceshipTrajectory)
        if self.name == 'spaceship':
            self.velX = inSpaceshipVel * math.cos(self.thetaRadians) * 1000
            self.velY = -inSpaceshipVel * math.sin(self.thetaRadians) * 1000
            self.vel = math.sqrt(self.velX**2 + self.velY**2)
            print(f'Initial Trajectory:\n'
                  f'          Theta: {inSpaceshipTrajectory} degrees\n'
                  f'       Velocity: {self.vel:,.2e} m/s\n'
                  f'     Velocity x: {self.velX:,.2e} m/s\n'
                  f'     Velocity y: {-self.velY:,.2e} m/s\n')
        else:
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
        otherX, otherY = other.xKm, other.yKm
        distanceX = otherX - self.xKm
        distanceY = otherY - self.yKm
        self.distance = math.sqrt(distanceX ** 2 + distanceY ** 2)
        if self.distance < self.distanceMin:
            self.distanceMin = self.distance
        if self.name == 'spaceship':
            self.displayData(window)

        force = self.gravity * self.mass * other.mass / ((self.distance * 1000) ** 2)
        self.gravity = force
        if force > self.gravityMax:
            self.gravityMax = force
        theta = math.atan2(distanceY, distanceX)
        Fx = math.cos(theta) * force
        Fy = math.sin(theta) * force
        return Fx, Fy


    def updatePosition(self, planets):
        totalFx = totalFy = 0
        for planet in planets:
            if self == planet:
                continue

            # Calculate: Gravitational forces
            Fx, Fy = self.attraction(planet)
            totalFx += Fx
            totalFy += Fy

            self.velX += totalFx / self.mass * SimulateObject.timeStep
            self.velY += totalFy / self.mass * SimulateObject.timeStep
            self.vel = math.sqrt(self.velX**2 + self.velY**2)
            self.x += ((self.velX * SimulateObject.timeStep) /
                       (1000 * self.simulationScale))
            self.y += ((self.velY * SimulateObject.timeStep) /
                       (1000 * self.simulationScale))
            self.xKm = self.x * self.simulationScale
            self.yKm = self.y * self.simulationScale
            self.orbit.append((self.x, self.y))


    def displayData(self, Window):
        # Display parameters
        fontSize = 40
        font = pygame.font.Font(None, fontSize)
        line1 = 20
        line2 = 50
        center = width // 2
        offsetSmall = width // 4
        offsetMid = 250
        
        textDistance = font.render(
            f'Distance: {self.distance:,.0f} km',
            True, textColorSimulation)
        textDistanceRect = textDistance.get_rect(
            center=(offsetSmall, line1))
        Window.blit(textDistance, textDistanceRect)
        
        textDistanceMin = font.render(
            f'Minimum Distance: {self.distanceMin:,.0f} km',
            True, textColorSimulation)
        textDistanceMinRect = textDistanceMin.get_rect(
            center=(center, line1))
        Window.blit(textDistanceMin, textDistanceMinRect)
        
        textVel = font.render(
            f'Velocity: {self.vel/1000:,.2e} km/s',
            True, textColorSimulation)
        textVelRect = textVel.get_rect(
            center=(center + offsetSmall, line1))
        Window.blit(textVel, textVelRect)

        textGravity = font.render(
            f'Gravity: {self.gravity} N',
            True, textColorSimulation)
        textGravityRect = textVel.get_rect(
            center=(center - offsetMid, line2))
        Window.blit(textGravity, textGravityRect)

        textGravityMax = font.render(
            f'Maximum Gravity: {self.gravity} N',
            True, textColorSimulation)
        textGravityMaxRect = textVel.get_rect(
            center=(center + offsetMid, line2))
        Window.blit(textGravityMax, textGravityMaxRect)


def main(simulationTime, intervalCount=0):
    run = True
    clock = pygame.time.Clock()

    # Create: Planet
    planet = makeObject(planetName=inSelectPlanet, scale=SimulateObject.simulationScale,
                       posX=0, posY=0)

    # Create: Spaceship
    spaceship = makeObject(planetName='spaceship', scale=SimulateObject.simulationScale,
                           posX=-inOrbitalDistanceX, posY=inOrbitalDistanceY)

    # Verify objects
    if planet is None or spaceship is None:
        print('ERROR: Object creation failed.\n'
              f'     Planet: {planet}\n'
              f'     Ship: {spaceship}')
        sys.exit()

    # Select: Simulated objects
    objectsList = [spaceship, planet]

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

        def getData(interval):
            if objectSimulate.name == 'spaceship':
                print(f'Simulation time: {whiteConsole}{interval:,} s{resetColor}\n'
                      f'     {objectSimulate.name} velocity: '
                      f'{redConsole}{objectSimulate.vel:.2e} m/s{resetColor}')
            else:
                print(f'     {objectSimulate.name} velocity: '
                      f'{purpleConsole}{objectSimulate.vel:.2e} m/s{resetColor}')
                print(f'     Gravity: {objectSimulate.gravity:.2e} Newtons')

        # Update and track objects
        printVel = False
        for index, objectSimulate in enumerate(objectsList):
            currentTime = time.time()
            if currentTime - simulationTime >= inDataFeedInterval:
                intervalCount += inDataFeedInterval
                simulationTime = time.time()
                getData(interval=intervalCount)
                printVel = True
            else:
                if printVel:
                    getData(interval=intervalCount)
                    printVel = False
                    # print('End Simulation: Get the projections right')
                    # sys.exit()
            objectSimulate.updatePosition(objectsList)
            objectSimulate.draw(window)

        pygame.display.update()
    pygame.quit()
main(simulationTime=time.time())
