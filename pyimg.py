import os
import pygame
import StreetView
from pygame.locals import *
import hud
import StreetView
from bike import bike
import urllib
import os.path
import unicodedata
import math
from xml.dom.minidom import parse

#http://www.bikehike.co.uk/mapview.php

def usage():
    print ("TODO...")

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')
waypoints = []
distance_step = .05 #2 Meters
current_point = 0

    
def main():
    global current_step
    global current_point
    mybike = bike()
    alpha = 100.0
    changed = False
    step = 20
    doc = parse('breckenridge_5k.tcx')
    trackpoints = doc.getElementsByTagName("Trackpoint")
    elements = ('AltitudeMeters', 'DistanceMeters', 'LatitudeDegrees', 'LongitudeDegrees')
    for tp in trackpoints:
        obj = {}
        for el in elements:
            obj[el] = float(tp.getElementsByTagName(el)[0].firstChild.data)
        waypoints.append(obj)
    
    pygame.init ()
    screen = pygame.display.set_mode ((640, 480), 0, 32)
    
    all_route_points = {}
    all_route_points = StreetView.load_route_points(data_dir, waypoints)
    
    current_image = pygame.image.load (all_route_points[current_point]['FileName']).convert()
    next_image    = pygame.image.load (all_route_points[current_point+1]['FileName']).convert()

    pygame.display.flip ()
    pygame.key.set_repeat (500, 30)
    usage()

    going = True
    while going:
        for event in pygame.event.get ():
            if event.type == QUIT:
                going = False

            if event.type == KEYDOWN and event.key == K_q:
                alpha -= step
                if alpha <= 0.0:
                    alpha = 100
                    current_point+=1
                    current_image = pygame.image.load (all_route_points[current_point]['FileName']).convert()
                    next_image    = pygame.image.load (all_route_points[current_point+1]['FileName']).convert()
                changed = True
            elif event.type == KEYDOWN and event.key == K_w:
                alpha += step
                changed = True
                if alpha >= 100:
                    alpha = 100

        current_image.set_alpha(alpha)
        next_image.set_alpha(100-alpha)
        screen.blit (current_image, (0, 0))
        screen.blit (next_image, (0, 0))
        screen.blit (hud.get_hud(mybike), (0,0))
        pygame.display.flip ()
        changed = False

    pygame.quit()


if __name__ == '__main__': 
    main()
