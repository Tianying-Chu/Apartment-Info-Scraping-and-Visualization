# -*- coding: utf-8 -*-
"""
@author: Joyqiao
Uses： detect corresponding Council_ID for each apartment
        add Council_ID on apt_data
"""


import geopandas as gpd
from shapely.geometry import Point
   
# CHECK IF THE POINT OF ADDRESS IS WITHIN BOUDARY POLYGON
#RETURN COUNCIL_ID
def check(lon,lat,boundary):
    point = Point(lon, lat) #BUILD SHAPELY POINT FROM LONGITUDE AND LATITUDE
    council_belong = -1
    #LOOP THROUGH ALL COUNCIL BOUDARY TO ASSIGN THE RIGHT COUNCIL ID FOR THIS APARTMENT
    for i in range(len(boundary)):        
        if point.within(boundary['geometry'][i]):
            council_belong = boundary['council'][i]
        if council_belong != -1:
            return council_belong

def main(data):
    boundary = gpd.read_file('PGH_CityCouncil.geojson') #READ GEOJSON AS GEODF
    council_list = []
    for i in range(len(data['lat'])): #LOOP THROUGH ALL APT 
        council_belong  = check(data['lng'][i],data['lat'][i],boundary)
        council_list.append(council_belong) 
    data['Council'] = council_list #ADD COUNCIL_ID TO APT_DATA
    return data
    
if __name__ == '__main__':
    main()

