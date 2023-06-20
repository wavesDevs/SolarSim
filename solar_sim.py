import numpy as np
from skyfield.api import load, utc
from datetime import datetime, timedelta
import pygame

#load planetary data
planets = load('de421.bsp')  #ephemeris data from 1900 to 2050
ts = load.timescale()

#initialize pygame
pygame.init()
screen_width, screen_height = 1600, 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Solar System Simulation")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 20)

#create color codes for easy reference
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
CYAN = (0, 255, 255)

#create dictionary with planet info
bodies = {
    "sun": {"obj": planets["sun"], "radius": 10, "color": YELLOW, "trail": []},                
    "mercury": {"obj": planets["mercury"], "radius": 2, "color": ORANGE, "trail": []},         
    "venus": {"obj": planets["venus"], "radius": 3, "color": WHITE, "trail": []},              
    "earth": {"obj": planets["earth"], "radius": 3, "color": BLUE, "trail": []},               
    "mars": {"obj": planets["mars"], "radius": 2, "color": RED, "trail": []},                  
    "jupiter": {"obj": planets["jupiter_barycenter"], "radius": 7, "color": ORANGE, "trail": []},
    "saturn": {"obj": planets["saturn_barycenter"], "radius": 6, "color": GREEN, "trail": []},   
    "uranus": {"obj": planets["uranus_barycenter"], "radius": 5, "color": RED, "trail": []},    
    "neptune": {"obj": planets["neptune_barycenter"], "radius": 5, "color": CYAN, "trail": []}  
}

#print(planets["sun"], planets["mercury"], planets["venus"], planets["earth"], planets["mars"], planets["jupiter_barycenter"], planets["saturn_barycenter"], planets["uranus_barycenter"], planets["neptune_barycenter"])

#current date and time information
current_time = datetime.utcnow().replace(tzinfo=utc)
time_step = timedelta(days=1)

#scaling factor to be used in sim
scaling_factor = 30

#sim loop
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((0, 0, 0))

    for name, data in bodies.items():
        #set t to current time in utc for skyfield
        t = ts.utc(current_time)

        #positional data, if-else necessary to not break the sim (still not entirely sure why this works but it does)
        if name in ["jupiter", "saturn", "uranus", "neptune"]:
            pos = data["obj"].at(t).position.au
        else:
            pos = data["obj"].at(t).observe(planets["sun"]).apparent().position.au

        #use position data as x and y coordinates
        x = int(pos[0] * (scaling_factor) + screen.get_width() / 2)
        y = int(-pos[1] * scaling_factor + screen.get_height() / 2)

        #import radius information
        radius = data["radius"]

        #create the planets in pygame
        pygame.draw.circle(screen, data["color"], (x, y), radius)

        #add labels to the planets
        label = font.render(name, True, WHITE)
        label_rect = label.get_rect(center=(x, y - radius - 10))  #position calculation for the label placement
        screen.blit(label, label_rect)

        #create the trails
        data["trail"].append((x, y))
        for i in range(len(data["trail"]) - 1):
            pygame.draw.line(screen, data["color"], data["trail"][i], data["trail"][i + 1])

        # #limit to trail length
        # if len(data["trail"]) > 100:
        #     data["trail"] = data["trail"][1:]

    pygame.display.flip()
    clock.tick(60)
    current_time += time_step #update time step

pygame.quit()