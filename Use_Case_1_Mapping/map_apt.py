# Author: Guoyu Wu
# Description: This program uses the folium package to visualize data.
# It defines functions to display a choropleth map of crime data
# and add apartment data as markers


import pandas as pd
import folium # a useful library for visualization


# This function initiates a blank map
# parameter: [latitude, longitude] of the center point
# return the blank map
def initiate_map(center_location):
    pit_map = folium.Map(location = center_location, zoom_start = 12)
    return pit_map


# This function draws the boundary lines of councils
# parameter1: boundary_data should be a GeoJson formatted file
# parameter2: pit_map is the map object you want to draw on;
def draw_boundary(boundary_data, pit_map):
#    import json
#    import requests
    folium.GeoJson(
            data = boundary_data,
            # specify the boundary styles
            style_function=lambda feature: {
                           'fillColor': '#ffff00', #fill with yellow
                           'color': 'black', #line color
                           'weight': 2, #line weight
                           'dashArray': '5, 5' #line style
                           }
            ).add_to(pit_map)
    return pit_map
    

# This function counts the number of crimes in each council area
# parameter: the raw crime data CSV file
# return a crime_stats dataframe
def crime_stat(crime_data):
    crime_df = pd.read_csv(crime_data)
    crime_df = crime_df.dropna() # remove rows containing NA
    crime_df = crime_df.iloc[-365:,:] # select the data for the past 365 days
    
    crime_stats = pd.DataFrame(crime_df['COUNCIL_DISTRICT'].value_counts())
    crime_stats.reset_index(inplace=True)
    crime_stats.rename(columns={'index':'Council_ID','COUNCIL_DISTRICT':'Count'},inplace=True)
    return crime_stats


# This function draws a choropleth map of crime data
# parameter1: boundary_data should be a GeoJson formatted file;
# parameter2: crime_stats is a dataframe indicating how dark the color of an area should be
# parameter3: pit_map is the map object you want to draw on
def map_crime(boundary_data, crime_stats, pit_map):

    folium.Choropleth(
            geo_data = boundary_data, 
            data = crime_stats,
            columns=['Council_ID','Count'],
            key_on='feature.properties.council', #variable in the GeoJson file to bind the data to
            
            fill_color='YlOrRd', # "red"
            fill_opacity=0.5,
            line_opacity=0.2,
            highlight=True,
            legend_name='Crime Counts in Pittsburgh (for the past 365 days)'
            
            ).add_to(pit_map)

    # mark the location of Hamburgh Hall
    # Hamburg Hall coordinates are obtained by find_lat_lng(address) function in find_apt.py
    hbh_location = [40.4443494, -79.9455454]
    folium.CircleMarker(hbh_location, radius=15, popup='HBH 1006', 
                        color='green', fill=True, 
                        fill_color='green',fill_opacity=1).add_to(pit_map)
    return pit_map


# This function processes the raw apartment data to lists
# parameter: the raw apartment data CSV file
# return three lists
def apt_process(apt_data):
    apt_lat = list(apt_data['lat'])
    apt_lng = list(apt_data['lng'])
    
    # create pop-up info dataframe
    labels = list()
    for i in range(len(apt_data['lat'])):
        title = apt_data['Title'].iloc[i]
        unit = apt_data['Unit'].iloc[i]
        rent = apt_data['Rent'].iloc[i]
        phone = apt_data['Phone'].iloc[i]
        df = pd.DataFrame(data=[[title,unit,rent,phone]], 
                          columns=['Title','Room Types','Rent Range','Tel'])
        labels.append(df)
        
    return apt_lat, apt_lng, labels


# This function adds apartment markers and their associated pop-up info
# parameter1,2: latitude and longitude lists of the apartment;
# parameter3: a list of dataframes;
# parameter4: pit_map is the map object you want to draw on
# return the new map object
def add_apt_marker(apt_lat, apt_lng, labels, pit_map):

    for lat, lng, df in zip(apt_lat, apt_lng, labels):
        # add pop-up info dataframe to each apartment marker
        html = df.to_html(classes='table table-striped table-hover table-condensed table-responsive')
        popup = folium.Popup(html)
        # create markers
        folium.Marker([lat, lng], popup=popup, 
                               icon = folium.Icon(color='blue',icon='ok-sign')
                               ).add_to(pit_map)
        
    return pit_map



# The main function 
# parameter1: the raw apartment data CSV file;
# parameter2: a list of dataframes;
# return the new map object
def main(apt_data, html_savefile):
    # initiate a blank map with HBH in the center
    hbh_location = [40.4443494, -79.9455454]
    pit_map = initiate_map(hbh_location)
    
    # draw the boundary lines of the nine councils in Pittsburgh
    pit_boundary = 'PGH_CityCouncil.geojson'
    pit_map = draw_boundary(pit_boundary,pit_map)

    # process the raw data
    crime_data = 'Pittsburgh Police Arrest Data.csv'
    crime_stats = crime_stat(crime_data)
    apt_lat,apt_lng,labels = apt_process(apt_data)
    
    # add crime data and apartment information to the blank map
    pit_map = map_crime(pit_boundary, crime_stats, pit_map)
    pit_map = add_apt_marker(apt_lat, apt_lng, labels, pit_map)

    # save map to html format
    pit_map.save(html_savefile)
    
    # display the map (for later use in Use Case 2)
    from IPython.display import display
    display(pit_map)




if __name__ == '__main__':
    apt = 'apt_data.csv'# output file from find_apt.py
    apt_data = pd.read_csv(apt)
    main(apt_data,'pit_map.html')


