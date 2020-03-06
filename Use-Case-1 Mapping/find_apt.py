import pandas as pd
import requests, json


# define a function to transform the address column into latitude and longitude columns 
# input formatted address of the location (string type)
# output latitude and longtitude of the input address
def find_lat_lng(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    parameter = address
    r = requests.get(url + 'address=' + parameter + '&key=' + KEY)
    geocode_result = r.json() 
#    
    #obtain latitude and longtitude
    location = geocode_result['results'][0]['geometry']['location']
    lat,lng = location['lat'],location['lng']
    return lat,lng


# apply your API KEY at https://code.google.com/apis/console
KEY = input('Enter your GoogleMaps API key:')


# read the apartment data file (cleaned) to a dataframe
data = 'Cleaned_Data.csv'
apt_data = pd.read_csv(data)


# create two lists
lat_list = []
lng_list = []

# populate the lists with the lat and lng data returned by the find_lat_lng(address) function
for i in range(len(apt_data['Location'])):
    address = apt_data['Location'][i]
    latitude,longitude = find_lat_lng(address)
    lat_list.append(latitude)
    lng_list.append(longitude)
    
# append the two new lists to the dataframe
apt_data['lat'] = lat_list
apt_data['lng'] = lng_list


# write the new dataframe (two new columns appended) to a new csv
apt_data.to_csv('apt_data.csv')

