# -*- coding: utf-8 -*-
"""
@author: Joyqiao
Function： Use Google API to obtain distance and nearby restaurant info
          Concact crime data to represent safety index of apartment 
          Return comprehensive apartment data      
"""
import pandas as pd
import requests 
import apt_to_council



#INPUT ORIGIN ADDRESS AND DESTINATION ADDRESS
#OUTPUT DISTANCE BETWEEN
def calculate_distance_api(origin,destination,KEY):
    
    url = 'https://maps.googleapis.com/maps/api/directions/json?'
    r = requests.get(url + 'origin=' + origin + '&destination=' + destination + '&key=' + KEY) 
    geocode_result = r.json() 
    distance = geocode_result['routes'][0]['legs'][0]['distance']['text'] #EXTRACT DISTANCE AS '0.6 mile'
    distance = distance.split(' ')[0] #get the first item after split which is the numeric number
    return distance



# INPUT LATITUDE LONGITUDE OF THE APT ADDRESS AND EXPECTED RADIUS (RADIUS TYPE IS NUMERIC)
# SEARCHTYPE(restaurant, bank,police,park extra) IN THIS CASE WE USE RESTAURANT
# OUTPUT RESTAURANT NUMBER AND RESTUARANT LIST AS [{NAME1:PRICLEVEL1},{NAME2:PRICELEVEL2}] 
def search_nearby_api(lat,lng,radius,searchtype,KEY): 

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"        
    parameter = 'location={},{}&radius={}&type={}'.format(lat,lng,radius,searchtype)
    r = requests.get(url  + parameter +'&key=' + KEY) 
    nearby_result = r.json() 
    restaurant_number = len(nearby_result['results'])
    restaurant_list = []
    
    #ADD FOR LOOP FOR ALL THE RESTAURANT RETURNED TO DOUBLE CHECK IF THEIR NAME AND PRICELEVEL ARE NOT NONE
    for i in range(restaurant_number):
        if 'name' in nearby_result['results'][i]:
            name = nearby_result['results'][i]['name']
        else:
            continue
        if 'price_level' in nearby_result['results'][i]:
            price_level = nearby_result['results'][i]['price_level']
        else:
            price_level = None
        restaurant_list.append({'name':name,'price_level':price_level})
    
    return restaurant_number,restaurant_list


#CALL DISTANCE AND NEARBY FUNCTIONS
#INPUT APARTMENT DATA DATAFRMAE
#OUTPUT DISTANCE AND NEARBY ITEM ADDED DATAFRAME    
def add_distance_nearby_data(apt_data,destination,radius,searchtype,KEY):

    distance_list = []   
    Res_N_list = []
    Res_name_list=[]
    
    #CALL THE DISTANCE AND NEARBY FUNCTION AND SAVE DATA INTO LISTS
    for i in range(len(apt_data['Location'])):
        address = apt_data['Location'][i]
        latitude,longitude = apt_data['lat'][i],apt_data['lng'][i]

        distance = calculate_distance_api(address,destination,KEY)
        restaurant_n, restaurant_name = search_nearby_api(latitude,longitude,radius,searchtype,KEY)
        
        distance_list.append(distance)
        Res_N_list.append(restaurant_n)
        Res_name_list.append(restaurant_name)

    #ADD LISTS TO DATAFRAME 
    apt_data.loc[:,'distance'] = distance_list  
    apt_data.loc[:,'restaurant_n'] = Res_N_list
    apt_data.loc[:,'restarant_name'] = Res_name_list        
    return apt_data



#JOIN CORRESPOINDING CRIME CASE PERCETANGE ON COUNCIL_ID AND ADD INTO APT_DATA
#INPUT APTARTMENT DATAFRAME
#OUTPUT UPDATED APARTMENT DATAFRAME
def add_crime(apt_data):
    data = 'Pittsburgh Police Arrest Data.csv'
    crime_data = pd.read_csv(data)
    crime_data = crime_data.dropna() 
    council_data = pd.DataFrame(crime_data['COUNCIL_DISTRICT'].value_counts())
    council_data.reset_index(inplace=True)
    council_data.rename(columns={'index':'Council_ID','COUNCIL_DISTRICT':'Count'},inplace=True)
    council_data['Count'] = council_data['Count']/sum(council_data['Count'])
    apt_data = pd.merge(apt_data, council_data, how='left', left_on=['Council'],right_on = ['Council_ID']).drop(['Council_ID'],axis = 1)
    apt_data.rename(columns={'Count':'crime_count_pct'},inplace = True)
    return apt_data



#OUTPUT COMPREHENSIVE APARTMENT CSV FILE
def main():
    KEY = input('Please enter your Google key:') # APPLY YOUR API KEY AT https://code.google.com/apis/console
    apt_data = pd.read_csv('apt_data.csv',index_col = 0) #READ IN DATA
    apt_data = apt_to_council.main(apt_data) #ADD COUNCIL_ID
    apt_data = apt_data[apt_data['Council'].notna()] #DROP APARTMENTS OUTSIDE PITTSBURGH BOUNDARY
    apt_data = apt_data.reset_index(drop=True) #REINDEX    
    apt_data = add_distance_nearby_data(apt_data,destination = 'Hamburg Hall, Forbes Ave, Pittsburgh, PA 15213',radius = 400,searchtype = 'restaurant',KEY = KEY)
    apt_data = add_crime(apt_data)
    apt_data.to_csv('apt_combined_data.csv')
    
if __name__ == '__main__':
    main()
    
