import pygame
import math
from math import sin, cos, acos, atan2, pi, degrees, radians

import urllib
import os.path

def bearing_between(lon1, lat1, lon2, lat2):
    """
    tc1=mod(atan2(sin(lon2-lon1)*cos(lat2),
                  cos(lat1)*sin(lat2)-sin(lat1)*cos(lat2)*cos(lon2-lon1)),
            2*pi)
    """


    lon1 = radians(lon1)
    lon2 = radians(lon2)

    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = atan2(
               sin(lon2-lon1)*cos(lat2),
               cos(lat1)*sin(lat2)-sin(lat1)*cos(lat2)*cos(lon2-lon1)
        ) % (2*pi)

    return degrees(a)

def getimg(lat, lon, heading):
    url = "http://maps.googleapis.com/maps/api/streetview?size=640x640&location={lat},%20{lon}&fov=120&heading={heading}&pitch=0&sensor=false".format(lat = lat, lon = lon, heading = heading)
    return url
    
def get_bearing_radians(lat1, lon1, lat2, lon2):
    lat1r = radians(lat1)
    lon1r = radians(lon1)
    lat2r = radians(lat2)
    lon2r = radians(lon2)
    a = atan2(
        cos(lat1r)*sin(lat2r)-sin(lat1r)*cos(lat2r)*cos(lon2r-lon1r),
        sin(lon2r-lon1r)*cos(lat2r)
    )
    return a
    
def get_lat_lon_dist_km(lat1, lon1, lat2, lon2):
    a = acos(cos(radians(90-lat1))*cos(radians(90-lat2))+sin(radians(90-lat1)) *sin(radians(90-lat2)) *cos(radians(lon1-lon2))) *6371
    return a
    
def get_lat_lon_steps(lat1, lon1, lat2, lon2):
    step_dist = 0.05 #km
    dist = get_lat_lon_dist_km(lat1, lon1, lat2, lon2)
    s = math.floor(get_lat_lon_dist_km(lat1, lon1, lat2, lon2)/step_dist)
    s = int(s)
    if(s <= 1):
        return 0
    else:
        return s-1 

def get_step_point(lat1, lon1, lat2, lon2, tsteps, step):
    rval = {}
    rval['lat'] =((lat2-lat1)/tsteps)*step + lat1
    rval['lon'] =((lon2-lon1)/tsteps)*step + lon1
    return rval
    
def download_streetview_image(data_dir, lat1, lon1, bear):
    fname = str(abs(lat1))+"_"+str(abs(lon1))+"_"+str(bear)+".bmp"
    if not os.path.exists('data/'+fname):
        url = getimg(lat = lat1, lon = lon1, heading = bear)
        urllib.urlretrieve(url, 'data/'+fname)
        print "   Downloading...."
    return os.path.join (data_dir, fname)

def load_route_points(data_dir, waypoints):
    total_wp = len(waypoints)
    current_wp = 0
    rpoint_count = 0
    rpoints = {}
    for wp in waypoints:
        if ((current_wp + 1) < total_wp):
            lat1 = waypoints[current_wp]['LatitudeDegrees']
            lon1 = waypoints[current_wp]['LongitudeDegrees']
            lat2 = waypoints[current_wp+1]['LatitudeDegrees']
            lon2 = waypoints[current_wp+1]['LongitudeDegrees']
            steps = get_lat_lon_steps(lat1, lon1, lat2, lon2)
            if steps == 0:
                print "Processing Waypoint ("+str(current_wp)+" of  "+str(total_wp)+")..."       
                rpoints[rpoint_count] = {}
                rpoints[rpoint_count]['LatitudeDegrees']  = lat1
                rpoints[rpoint_count]['LongitudeDegrees'] = lon1
                rpoints[rpoint_count]['AltitudeMeters'] = waypoints[current_wp]['AltitudeMeters']
                rpoints[rpoint_count]['DistanceMeters'] = get_lat_lon_dist_km(lat1, lon1, lat2, lon2)*1000
                bear = degrees(get_bearing_radians(lat1, lon1, lat2, lon2))
                rpoints[rpoint_count]['BearingD'] = bear
                rpoints[rpoint_count]['FileName'] = download_streetview_image(data_dir, lat1, lon1, bear)
                rpoint_count += 1
            else:
            	for i in range(int(steps)):
            	    print "Processing Waypoint ("+str(current_wp)+" of  "+str(total_wp)+") Step("+str(i)+" of "+str(steps)+")..."
                    point1 = get_step_point(lat1, lon1, lat2, lon2, steps, i)
                    point2 = get_step_point(lat1, lon1, lat2, lon2, steps, i+1)
                    rpoints[rpoint_count] = {}
                    rpoints[rpoint_count]['LatitudeDegrees'] = point1['lat']
                    rpoints[rpoint_count]['LongitudeDegrees'] = point1['lon']
                    rpoints[rpoint_count]['AltitudeMeters'] = waypoints[current_wp]['AltitudeMeters']
                    rpoints[rpoint_count]['DistanceMeters'] = get_lat_lon_dist_km(point1['lat'], point1['lon'], point2['lat'], point2['lon'])*1000
                    bear = degrees(get_bearing_radians(point1['lat'], point1['lon'], point2['lat'], point2['lon']))
                    rpoints[rpoint_count]['BearingD'] = bear
                    rpoints[rpoint_count]['FileName'] = download_streetview_image(data_dir, point1['lat'], point1['lon'], bear)
                    rpoint_count +=1
            current_wp += 1
    return rpoints