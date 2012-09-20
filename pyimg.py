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
current_step  = 0
current_point = 0
    
def get_image(lat1, lon1, lat2, lon2):
    fname = str(abs(lat1))+"_"+str(abs(lon1))+".bmp"
    if not os.path.exists('data/'+fname):
        bear = StreetView.bearing_between(lon1 =lon1, lat1 = lat1, lon2 = lon2, lat2 = lat2)
        url = StreetView.getimg(lat = lat1, lon = lon1, heading = bear)
        print url
        urllib.urlretrieve(url, 'data/'+fname)
    return os.path.join (data_dir, fname)

def get_step_point(point1, point2, cs):
    R = 6378.1 #Radius of the Earth
    lat1 = waypoints[point1]['LatitudeDegrees']
    lon1 = waypoints[point1]['LongitudeDegrees']
    lat2 = waypoints[point2]['LatitudeDegrees']
    lon2 = waypoints[point2]['LongitudeDegrees']
    
    d = cs*distance_step

    rval = {}
    if (waypoints[point1]['DistanceMeters'] + d*1000) > waypoints[point2]['DistanceMeters']:
        rval['next'] = True
    else:
        bear = StreetView.bearing_between(lon1 =lon1, lat1 = lat1, lon2 = lon2, lat2 = lat2)
        brng = math.radians(bear)
        print "dist: "+str(d)+" bearing: "+str(bear)
    
        lat1r = math.radians(lat1) #Current lat point converted to radians
        lon1r = math.radians(lon1) #Current long point converted to radians

        latN = math.asin( math.sin(lat1r)*math.cos(d/R) + math.cos(lat1r)*math.sin(d/R)*math.cos(brng))

        lonN = lon1r + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1r), math.cos(d/R)-math.sin(lat1r)*math.sin(latN))
        rval['lat'] = math.degrees(latN)
        rval['lon'] = math.degrees(lonN)
        rval['next'] = False
        
    return rval

def get_current_image(cp, cs):
    global current_step
    global current_point
    #sp = get_step_point(cp, cp+1, cs)
    lat1 = waypoints[cp]['LatitudeDegrees']
    lon1 = waypoints[cp]['LongitudeDegrees']
    lat2 = waypoints[cp+1]['LatitudeDegrees']
    lon2 = waypoints[cp+1]['LongitudeDegrees']
    #if not sp['next']:
    #    lat1 = sp['lat']
    #    lon1 = sp['lon']
    #else:
    #    lat1 = waypoints[cp+1]['LatitudeDegrees']
    #    lon1 = waypoints[cp+1]['LongitudeDegrees']
    #    lat2 = waypoints[cp+2]['LatitudeDegrees']
    #    lon2 = waypoints[cp+2]['LongitudeDegrees']
    #    current_step=0
    #    current_point+=1
    return pygame.image.load (get_image(lat1, lon1, lat2, lon2)).convert()
    
    
def main():
    global current_step
    global current_point
    mybike = bike()
    alpha = 100.0
    changed = False
    step = 20
   # doc = parse('brentmoor_6mi_loop.tcx')
    doc = parse('tail_of_dragon.tcx')
    trackpoints = doc.getElementsByTagName("Trackpoint")
    elements = ('AltitudeMeters', 'DistanceMeters', 'LatitudeDegrees', 'LongitudeDegrees')
    for tp in trackpoints:
        obj = {}
        for el in elements:
            obj[el] = float(tp.getElementsByTagName(el)[0].firstChild.data)
        waypoints.append(obj)
    
    pygame.init ()
    screen = pygame.display.set_mode ((640, 480), 0, 32)
    
    current_image = get_current_image(current_point, current_step)
    next_image    = get_current_image(current_point, (current_step+1))

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
                    current_image = get_current_image(current_point, current_step)
                    next_image    = get_current_image(current_point+1, current_step)
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
