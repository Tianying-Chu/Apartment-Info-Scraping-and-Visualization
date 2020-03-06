# Author: Guoyu Wu
# Description: This program uses the folium package 
# to display a choropleth map of crime data
# and add apartment data as markers


import pandas as pd
import folium # a useful library for visualization


# read the crime and apartment data to dataframes respectively
crime = 'Pittsburgh Police Arrest Data.csv'
apt = 'apt_data.csv' # output file from find_apt.py
crime_data = pd.read_csv(crime)
apt_data = pd.read_csv(apt)


# Hamburg Hall coordinates returned by find_lat_lng(address) function in find_apt.py
hbh_lat = 40.4443494
hbh_lng = -79.9455454

# initiate a blank Pittsburgh map (let HBH be the center)
pit_map = folium.Map(location=[hbh_lat, hbh_lng], zoom_start=12)



# use folium.GeoJson to draw the boundary lines of Pittsburgh city
import json
import requests

folium.GeoJson(
        # pass the Pittsburgh boundary data file (GeoJson formatted)
        data = 'PGH_CityCouncil.geojson',
        # specify the boundary styles
        style_function=lambda feature: {
                       'fillColor': '#ffff00', #fill with yellow
                       'color': 'black', #line color
                       'weight': 2, #line weight
                       'dashArray': '5, 5' #line style
                       }
        ).add_to(pit_map)



# create coordinates lists from apt_data dataframe
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


# add apartment markers and associated pop-up info
for lat, lng, df in zip(apt_lat, apt_lng, labels):
    # add pop-up info dataframe to each apartment marker
    html = df.to_html(classes='table table-striped table-hover table-condensed table-responsive')
    popup = folium.Popup(html)
    # create markers with the apt data with pop-up info
    marker = folium.Marker([lat, lng], popup=popup, 
                           icon = folium.Icon(color='blue',icon='ok-sign')
                           ).add_to(pit_map)



crime_data = crime_data.dropna() # remove rows containing NA
crime_data = crime_data.iloc[-365:,:] # select the data for the past 365 days

# count crime numbers in each council
concil_stats = pd.DataFrame(crime_data['COUNCIL_DISTRICT'].value_counts())
concil_stats.reset_index(inplace=True)
concil_stats.rename(columns={'index':'Council_ID','COUNCIL_DISTRICT':'Count'},inplace=True)
print(concil_stats)

# draw a choropleth map of crime data
folium.Choropleth(
        # pass the Pittsburgh boundary data file (GeoJson formatted)
        geo_data = 'PGH_CityCouncil.geojson', 
        # pass the count data
        data = concil_stats,
        columns=['Council_ID','Count'],
        # variable in the GeoJson file to bind the data to
        key_on='feature.properties.council',
        
        # define map styles
        fill_color='YlOrRd', # "red"
        fill_opacity=0.5,
        line_opacity=0.2,
        highlight=True,
        legend_name='Crime Counts in Pittsburgh (for the past 365 days)'
        
        ).add_to(pit_map)


# mark the location of Hamburgh Hall
folium.CircleMarker([hbh_lat, hbh_lng], radius=15, popup='HBH 1006', 
                    color='green', fill=True, 
                    fill_color='green',fill_opacity=1).add_to(pit_map)


# Save map to html format
pit_map.save('pit_map.html')

