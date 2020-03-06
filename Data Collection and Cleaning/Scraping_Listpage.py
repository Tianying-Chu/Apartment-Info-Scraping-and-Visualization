# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 21:22:02 2020

@author: Tianying Chu
"""

'''
Scraping_Listpage.py scrapes the apartment information(eg. url, location, ...)
on the listpages, saves the information to a Dataframe, and write the Dataframe 
into a csv file.
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

'''
getAptCards function gets the cards on the listpage which stores the basic information of each apartment 
no input parameters
return: a list of cards(each card is a 'bs4.element.Tag')
'''
def getAptCards():
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763',
            'Cookie': 'ab=%7b%22e%22%3atrue%2c%22r%22%3a%5b%5d%7d; hpe=%7b%22id%22%3a%22%22%2c%22v%22%3a-1%2c%22et%22%3a13%2c%22cdi%22%3a17%2c%22dispatch%22%3atrue%2c%22isRead%22%3afalse%2c%22irm%22%3afalse%7d; lg=%7B%22ID%22%3A%22g7kmpjy%22%2C%22PlaceId%22%3Anull%2C%22Display%22%3A%22Pittsburgh%2C%20PA%22%2C%22GeographyType%22%3A2%2C%22Address%22%3A%7B%22City%22%3A%22Pittsburgh%22%2C%22County%22%3Anull%2C%22PostalCode%22%3Anull%2C%22State%22%3A%22PA%22%2C%22StreetName%22%3Anull%2C%22StreetNumber%22%3Anull%2C%22Title%22%3Anull%2C%22Abbreviation%22%3Anull%2C%22BuildingName%22%3Anull%2C%22CollegeCampusName%22%3Anull%2C%22MarketName%22%3A%22Pittsburgh%22%2C%22DMA%22%3A%22Pittsburgh%2C%20PA-WV-MD%22%7D%2C%22Location%22%3A%7B%22Latitude%22%3A40.431%2C%22Longitude%22%3A-79.981%7D%2C%22BoundingBox%22%3A%7B%22LowerRight%22%3A%7B%22Latitude%22%3A40.36157%2C%22Longitude%22%3A-79.86579%7D%2C%22UpperLeft%22%3A%7B%22Latitude%22%3A40.50104%2C%22Longitude%22%3A-80.09551%7D%7D%2C%22O%22%3Anull%2C%22Radius%22%3Anull%2C%22v%22%3A37323%7D; _ga=GA1.2.101764883.1581720802; uat=%7b%22VisitorId%22%3a%22b74dd047-ba3d-444a-8a95-6ca6a5e44bc1%22%2c%22VisitId%22%3a%220d16e21e-1941-4de0-8747-cad6cfd1b138%22%2c%22LastActivityDate%22%3a%222020-02-28T15%3a58%3a17.1188335-05%3a00%22%2c%22LastFrontDoor%22%3a%22APTS%22%7d; _gcl_au=1.1.1607667592.1581720803; _dpm_id.c51a=758ad3fe-ad24-4abe-a817-ad5f0fb21041.1581720804.2.1582923486.1581720804.2a1a11dc-f25d-4082-a8b3-cc533107fd68; _fbp=fb.1.1581720807562.1825746062; cto_bundle=C_sD9l8zaXZZNUxYbXBpRzU1SWl5dTViZ0JnZSUyRnNhWiUyRlN5M0hKY3h1bVVTdXlJUDM3dHJKUlRoR3VLN3NiVUVLY21yOGRUNkE2U25MMyUyQkx2OTNUeTdqU1YlMkJEQ25ESVpLbTFQRUpyZDNVRk1DU1ZucFhLdjA3ZE1oc0l0RDJYeWZaaTJHVkpKdWY5V2hzMkIzZ2Vab3dtbGxQYnh0RSUyRmRlNlc3NE1xZEJvT0Q0WnBjJTNE; s=; gip=%7b%22Display%22%3a%22Pittsburgh%2c+PA%22%2c%22GeographyType%22%3a2%2c%22Address%22%3a%7b%22City%22%3a%22Pittsburgh%22%2c%22State%22%3a%22PA%22%7d%2c%22Location%22%3a%7b%22Latitude%22%3a40.445%2c%22Longitude%22%3a-79.9527%7d%7d; ak_bmsc=6F7E18063A023AAB276E4413F78AAD4C172B3AEDAD580000A07D595ED4095707~plTgK1VpA0zMxmcwsUslEbE/yqLkTba6Bp0QIqvfidzS+pe9VtOBUx5gknZVO8Azx2mJ7hWf5aawWnbzKV1nXgOu65uuXj8T99KjsRtFvf7V5Ek0csGzybT6uf6Hz9hmJPENLo/0IPKN4DNJavwbJdqge5M4a0si0iizIFmgiQQJRffijpuUh5yTwtLWg9SS0OCP+JbguZCiCzKKdVpNRntko5lQszdGKLb8csNDQQNrRbwVYcSfmpPAHb0xmABqHd; akaalb_www_apartments_com_main=~op=www_apartments_com:www_apartments_com_RESTON|~rv=15~m=www_apartments_com_RESTON:0|~os=0847b47fe1c72dfaedb786f1e8b4b630~id=a171c82dad505731946c28fd04ef52e6; sr=%7B%22Width%22%3A725%2C%22Height%22%3A624%2C%22PixelRatio%22%3A3%7D; _gid=GA1.2.799266776.1582923157; _dpm_ses.c51a=*; bm_sv=6A4888F93CFC640CE003F2C2D28486B8~Z7B7IJmhR6sJw7ERwQfrNsO0xYRoRpqvcb+mlf7n3yhXv2LakfajOYonqve5AEn7usgVow5pCcMOKFU2/4KSlFtuCS+rGXDXhY/TzE/q4lYrOfejaz1RpFSVWFYYcSjPQPkjQrJg5FR72HmGpK0pkpdUZLG7IObso5/3qq4B1oM=; lnc=%7b%22Geography%22%3a%7b%22ID%22%3a%22g7kmpjy%22%2c%22Display%22%3a%22Pittsburgh%2c+PA%22%2c%22GeographyType%22%3a2%2c%22Address%22%3a%7b%22City%22%3a%22Pittsburgh%22%2c%22State%22%3a%22PA%22%2c%22MarketName%22%3a%22Pittsburgh%22%2c%22DMA%22%3a%22Pittsburgh%2c+PA-WV-MD%22%7d%2c%22Location%22%3a%7b%22Latitude%22%3a40.431%2c%22Longitude%22%3a-79.981%7d%2c%22BoundingBox%22%3a%7b%22LowerRight%22%3a%7b%22Latitude%22%3a40.36157%2c%22Longitude%22%3a-79.86579%7d%2c%22UpperLeft%22%3a%7b%22Latitude%22%3a40.50104%2c%22Longitude%22%3a-80.09551%7d%7d%2c%22v%22%3a37323%7d%2c%22BoundingBox%22%3a%7b%22LowerRight%22%3a%7b%22Latitude%22%3a40.36157%2c%22Longitude%22%3a-79.86579%7d%2c%22UpperLeft%22%3a%7b%22Latitude%22%3a40.50104%2c%22Longitude%22%3a-80.09551%7d%7d%7d; uat=%7B%22VisitorId%22%3A%22b74dd047-ba3d-444a-8a95-6ca6a5e44bc1%22%2C%22VisitId%22%3A%220d16e21e-1941-4de0-8747-cad6cfd1b138%22%2C%22LastActivityDate%22%3A%222020-02-28T15%3A57%3A12.4935597-05%3A00%22%2C%22LastFrontDoor%22%3A%22APTS%22%2C%22LastSearchId%22%3A%228AFB3E25-B9F4-470E-8F9C-0A4C05791DE9%22%7D; lsc=%7B%22Map%22%3A%7B%22BoundingBox%22%3A%7B%22LowerRight%22%3A%7B%22Latitude%22%3A40.36157%2C%22Longitude%22%3A-79.86579%7D%2C%22UpperLeft%22%3A%7B%22Latitude%22%3A40.50104%2C%22Longitude%22%3A-80.09551%7D%7D%7D%2C%22Geography%22%3A%7B%22ID%22%3A%22g7kmpjy%22%2C%22Display%22%3A%22Pittsburgh%2C%20PA%22%2C%22GeographyType%22%3A2%2C%22Address%22%3A%7B%22City%22%3A%22Pittsburgh%22%2C%22State%22%3A%22PA%22%2C%22MarketName%22%3A%22Pittsburgh%22%2C%22DMA%22%3A%22Pittsburgh%2C%20PA-WV-MD%22%7D%2C%22Location%22%3A%7B%22Latitude%22%3A40.431%2C%22Longitude%22%3A-79.981%7D%2C%22BoundingBox%22%3A%7B%22LowerRight%22%3A%7B%22Latitude%22%3A40.36157%2C%22Longitude%22%3A-79.86579%7D%2C%22UpperLeft%22%3A%7B%22Latitude%22%3A40.50104%2C%22Longitude%22%3A-80.09551%7D%7D%2C%22v%22%3A37323%7D%2C%22Listing%22%3A%7B%7D%2C%22Paging%22%3A%7B%7D%2C%22ResultSeed%22%3A361024%2C%22Options%22%3A1%7D; _gat=1',
            'Host': 'www.apartments.com'
            }
    card_list = list()
    
    # loop for each listpage
    for i in range(28):
        url = 'https://www.apartments.com/pittsburgh-pa/' + str(i) + '/'
        response = requests.get(url, headers = headers)
        
        if response.status_code == 200:
            # get all the content on the page
            soup = BeautifulSoup(response.content, 'html.parser') 
            
            # cardContainer includes content of all the apt. cards 
            card_Container = soup.find(name = 'div', attrs = {'id': 'placardContainer'}) 
            
            # cards include cards for each apt.
            cards = card_Container.find_all(name = 'article') 
            for card in cards:
                card_list.append(card)
        
        time.sleep(0.2)
    return card_list

'''
getAptInfo function extracts data from the cards into the Dataframe
input: the list of cards from getAptCards function
return: a Dataframe of apartment information on the listpages
'''
def getAptInfo(card_list):
    apt_info = pd.DataFrame(columns = ['Url', 'Title', 'Company', 'Location', 
                                       'Last_Updated', 'Rent', 'Unit', 
                                       'Availability', 'Phone'])
    for card in card_list:
        # get apt_class to identify different types of card structures
        apt_class = card.attrs['class'][0]
        
        # fetch apartment information in each cards except for 'reinforcement' class(containing the advertisement)
        if apt_class != 'reinforcement':
            
            # get the url for each apartment
            try:
                url = card.attrs['data-url']
            except:
                url = ''
            
            # get the apartment title
            try:
                title = card.find(name = 'a', attrs = {'class': 'placardTitle js-placardTitle'}).text.strip()
            except:
                title = ''
            
            # get the property management company of the apartment
            try:
                company = card.find(name = 'img', attrs = {'class': 'propertyLogo'}).attrs['alt']
            except:
                company = ''
            
            # get the location of the apartment
            try:
                location = card.find(name = 'div', attrs = {'class': 'location'}).text
            except:
                location = ''
            
            # get the time for the last update
            try:
                last_updated = card.find(attrs = {'class': 'listingFreshness'}).text.strip()
            except:
                last_updated = ''
            
            # get the rent range of the apartment
            try:
                rent = card.find(attrs = {'class': 'altRentDisplay'}).text
            except:
                rent = ''
            
            # get the room types of the apartment
            try:
                unit = card.find(attrs = {'class': 'unitLabel'}).text
            except:
                unit = ''
            
            # get the availability of the apartment
            try:
                availability = card.find(attrs = {'class': 'availabilityDisplay noBedSelected'}).text
            except:
                availability = ''
            
            # get the phone number of the apartment owner
            try:
                phone = card.find(attrs = {'class': 'phone'}).text.strip()
            except:
                phone = ''
        
        # append each apartment's information to apt_info     
        apt_record = {'Title': title, 'Url': url, 'Company': company, 
                      'Location': location, 'Last_Updated': last_updated, 
                      'Rent': rent, 'Unit': unit, 'Availability': availability, 
                      'Phone': phone}
        apt_info = apt_info.append(apt_record, ignore_index=True)
    
    return apt_info

'''
writeCSV function writes the apartment information in the listpage into a csv file
input: apartment information Dataframe from getAptInfo function, file name
no return
'''
def writeCSV(apt_info, file):
    apt_info.to_csv(file)
        
'''
main function calls all the functions before.
'''
def main():
    # The information of each apartment is stored in the cards of listpage
    card_list = getAptCards()
    
    # extract data from the cards into the Dataframe
    apt_info = getAptInfo(card_list)
    
    # write the apartment information in the listpage into a csv file
    writeCSV(apt_info, 'Apt_Info.csv')
    
        
if __name__ == '__main__':
    
    main()
    
