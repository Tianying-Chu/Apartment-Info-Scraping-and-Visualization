# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 10:30:16 2020

@author: Yanyi Qian
"""

'''
Scraping_Subpage.py scrapes the apartment details(eg. AverageRating, WalkScore, 
TransitScore, Rent_by_room...) on the subpages, saves the details to a Dataframe, 
merge the information on the listpages and subpages, and write the merged 
Dataframe into a csv file.
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import bs4

'''
getSubpage function gets the content on the subpages which stores the details of each apartment
input: url for each subpage from 'Apt_Info.csv'
return: a list of content on the subpages (each subpage is a 'bs4.element.Tag')
'''
def getSubpage(urls):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36', 
            'Cookie': 'ab=%7b%22e%22%3atrue%2c%22r%22%3a%5b%5d%7d; _ga=GA1.2.1961149352.1581467936; _gcl_au=1.1.2000694365.1581467937; _fbp=fb.1.1581467938702.1037277821; kppid_managed=M_dN1jMF; hpe=%7b%22id%22%3a%22%22%2c%22v%22%3a-1%2c%22et%22%3a13%2c%22cdi%22%3a17%2c%22dispatch%22%3atrue%2c%22isRead%22%3atrue%2c%22irm%22%3atrue%7d; _gid=GA1.2.515334799.1582925803; s=; akaalb_www_apartments_com_main=~op=www_apartments_com:www_apartments_com_RESTON|~rv=23~m=www_apartments_com_RESTON:0|~os=0847b47fe1c72dfaedb786f1e8b4b630~id=cc330a8cb9376e416a91f4b55f8c8922; _gac_UA-1746553-2=1.1582991128.Cj0KCQiAtOjyBRC0ARIsAIpJyGNNiHZyYpt_LQHz0UAgL8w2hXliVJ96ntIUGdq9ulkElEPYbanWHcYaAse_EALw_wcB; _gcl_aw=GCL.1582991128.Cj0KCQiAtOjyBRC0ARIsAIpJyGNNiHZyYpt_LQHz0UAgL8w2hXliVJ96ntIUGdq9ulkElEPYbanWHcYaAse_EALw_wcB; _gcl_dc=GCL.1582991128.Cj0KCQiAtOjyBRC0ARIsAIpJyGNNiHZyYpt_LQHz0UAgL8w2hXliVJ96ntIUGdq9ulkElEPYbanWHcYaAse_EALw_wcB; dlf=%7B%22FirstName%22%3A%22%22%2C%22LastName%22%3A%22%22%2C%22PhoneNumber%22%3A%22%22%2C%22Email%22%3A%22%22%2C%22MoveInDate%22%3A%2203%2F01%2F2020%22%2C%22EmailListings%22%3Atrue%2C%22MaxRent%22%3Anull%2C%22ContactVia%22%3Anull%2C%22Beds%22%3Anull%2C%22Bath%22%3Anull%2C%22ReasonForMoving%22%3Anull%2C%22IsSubmitted%22%3Afalse%7D; lg=%7B%22ID%22%3A%22ykb96rv%22%2C%22PlaceId%22%3Anull%2C%22Display%22%3A%22Friendship%20-%20Pittsburgh%2C%20PA%22%2C%22GeographyType%22%3A4%2C%22Address%22%3A%7B%22City%22%3A%22Pittsburgh%22%2C%22County%22%3Anull%2C%22PostalCode%22%3Anull%2C%22State%22%3A%22PA%22%2C%22StreetName%22%3Anull%2C%22StreetNumber%22%3Anull%2C%22Title%22%3A%22Friendship%22%2C%22Abbreviation%22%3Anull%2C%22BuildingName%22%3Anull%2C%22CollegeCampusName%22%3Anull%2C%22MarketName%22%3A%22Pittsburgh%22%2C%22DMA%22%3A%22Pittsburgh%2C%20PA-WV-MD%22%7D%2C%22Location%22%3A%7B%22Latitude%22%3A40.461%2C%22Longitude%22%3A-79.934%7D%2C%22BoundingBox%22%3A%7B%22LowerRight%22%3A%7B%22Latitude%22%3A40.45657%2C%22Longitude%22%3A-79.93087%7D%2C%22UpperLeft%22%3A%7B%22Latitude%22%3A40.46457%2C%22Longitude%22%3A-79.93697%7D%7D%2C%22O%22%3Anull%2C%22Radius%22%3Anull%2C%22v%22%3A11253%7D; uat=%7B%22VisitorId%22%3A%2227a51920-c9bd-4ca8-9db8-77a87fb37767%22%2C%22VisitId%22%3A%22884135e6-eb6b-4a74-ad57-494273709338%22%2C%22LastActivityDate%22%3A%222020-02-29T10%3A45%3A27.9961756-05%3A00%22%2C%22LastFrontDoor%22%3A%22google%22%2C%22LastSearchId%22%3A%229BD59CF2-A375-47F9-B51E-1FDD0137DCAC%22%7D; lsc=%7B%22Map%22%3A%7B%22BoundingBox%22%3A%7B%22LowerRight%22%3A%7B%22Latitude%22%3A40.45657%2C%22Longitude%22%3A-79.93087%7D%2C%22UpperLeft%22%3A%7B%22Latitude%22%3A40.46457%2C%22Longitude%22%3A-79.93697%7D%7D%7D%2C%22Geography%22%3A%7B%22ID%22%3A%22ykb96rv%22%2C%22Display%22%3A%22Friendship%20-%20Pittsburgh%2C%20PA%22%2C%22GeographyType%22%3A4%2C%22Address%22%3A%7B%22City%22%3A%22Pittsburgh%22%2C%22State%22%3A%22PA%22%2C%22Title%22%3A%22Friendship%22%2C%22MarketName%22%3A%22Pittsburgh%22%2C%22DMA%22%3A%22Pittsburgh%2C%20PA-WV-MD%22%7D%2C%22Location%22%3A%7B%22Latitude%22%3A40.461%2C%22Longitude%22%3A-79.934%7D%2C%22BoundingBox%22%3A%7B%22LowerRight%22%3A%7B%22Latitude%22%3A40.45657%2C%22Longitude%22%3A-79.93087%7D%2C%22UpperLeft%22%3A%7B%22Latitude%22%3A40.46457%2C%22Longitude%22%3A-79.93697%7D%7D%2C%22v%22%3A11253%7D%2C%22Listing%22%3A%7B%7D%2C%22Paging%22%3A%7B%7D%2C%22ResultSeed%22%3A844257%2C%22Options%22%3A1%7D; _dpm_id.c51a=67932295-7f29-43fb-8b39-5f82193a17f2.1581467938.9.1582997944.1582995443.69c8c8bc-4c1f-47b6-8887-8f9f7363f722; gip=%7b%22Display%22%3a%22Pittsburgh%2c+PA%22%2c%22GeographyType%22%3a2%2c%22Address%22%3a%7b%22City%22%3a%22Pittsburgh%22%2c%22State%22%3a%22PA%22%7d%2c%22Location%22%3a%7b%22Latitude%22%3a40.4289%2c%22Longitude%22%3a-79.9232%7d%7d; bm_mi=A0B1B98FB29F2E42FAA24762E550170A~L0leodavSluaELWnDf9bNuUtpC/h1wibMwM7bfENn1oW+jl0Et1ZlAMyc4jt+K116xlLX89jgY+xrn5fYh/TnYTMlZbawQYOFdFf/SILjo7AlnczD5AZlE920W68pMa3gPwkN9kAwa2pDMNoh4f7IG0/r/uEtnHxgjl7uOA2tJ+LMrx0fEdKFunSx9UezRqWy1udRIe4l5QVtF2UjKfshUPvPVEV2+OnlNEPErtTK9ZRJVKIa1wLrm8qmIuzGW3g2108hNN1feQM8/jLtHdJojvRiqGXXeqYu8J+43MIJc4ft5PbSKuC6AC+dj9Gd3N2QDz0END7fCHgP0tmwUgC1g==; sr=%7B%22Width%22%3A1504%2C%22Height%22%3A860%2C%22PixelRatio%22%3A1.5%7D; bm_sv=271C6E9363B91BB626C86C6505D7FAD2~lXroequU7cgSi97MTbPp3xD8VZBi3DbZM/CpHWw6AgVTXg4Cb+2flGLeY0+CxQ0LOLJJhXxhcim1qbYnM+gtYtNtraUY25QqEg24wOH630n/gpu0k9f/uwTIF6h379cTF+oqWvHpj6l2oDi6bene6Jrx9vOulk1qQRatjGj4Bds=; uat=%7b%22VisitorId%22%3a%2227a51920-c9bd-4ca8-9db8-77a87fb37767%22%2c%22VisitId%22%3a%223f3b4f52-b1dc-49c0-aa67-38976abda193%22%2c%22LastActivityDate%22%3a%222020-02-29T14%3a03%3a42.8231417-05%3a00%22%2c%22LastFrontDoor%22%3a%22APTS%22%7d; ak_bmsc=26229E446C86498280CFC51A4F10582F172BA5DC484100002CAB5A5E3B9FDC7F~plMRGiMHj3BQ+T6AsIQNiVGgIBI2IRJS7pL3VwehAn0LNyQTr4Hj1TDQQE0IXCE7l4SQGdmX5uhA2pn0GSO75mOcKUHMkbWemAqosC8r8hK2beCP5WwZAxvfPMgSD1g85t8k7WLPIWhC9ExNxF2twN+5JQZMg57Dah1c0e+90tCtPaajDRH0iMUZmEaxsK7NuRehRefmLbZTckMzugTTc1PGCfSKFIQSHrq3i82LkxR6O2Gs5WM4T/neIt9/r0AHg1'
            }
    Subpage_list = list()
    
    # loop for urls of each apartment
    for url in urls:
        response = requests.get(url, headers = headers)
        
        if response.status_code == 200:
            # get all the content on the page
            soup = BeautifulSoup(response.content, 'html.parser') 
            
            # Subpage of each apt
            appContainer = soup.find(name='div',attrs={"class":"mainWrapper"}) 
            Subpage_list.append(appContainer)
        
        time.sleep(0.2)
    return Subpage_list
            
'''
getDetail function extracts detailed data from the subpages into the Dataframe
input: the list of subpages from getSubpage function
return: a Dataframe of apartment detailed information on the subpages
'''       
def getDetail(Subpage_list):
    Subpage_info = pd.DataFrame(columns =['AverageRating','# of Reviwer',
                                          'WalkScore','WalkScore_desc',
                                          'TransitScore', 'TransitScore_desc', 'Rent_by_room'])
    for Subpage in Subpage_list:        
        # get rent roll up of apartments
        # different rent for different types of room, stored the rents in a dictionary         
        try:
            rent_dict = {}
            rent_info = Subpage.find_all('span', {'class': 'rentRollup'})
            for item in rent_info:
                key = item.find('span', {'class': 'shortText'}).text.strip()
                string = "".join([t for t in item.contents if type(t) == bs4.element.NavigableString])
                value = string.strip()
                rent_dict[key] = value
        except:
            rent_dict = {} 
        
        # get average rating
        try:
            averageRating = Subpage.find('div', {'class': 'averageRating'}).text.strip()
        except:
            averageRating = ''
        
        # get number of revirewer
        try:
            num_reviewer = Subpage.find('p', {'class': 'renterReviewsLabel'}).text.strip()
        except:
            num_reviewer = ''
            
        # get walk score and the corresponding description
        try:
            walkScore = Subpage.find('div', {'class': 'ratingCol walkScore'}).find('span', {'class': 'score'}).text.strip()
            walkScore_desc = Subpage.find('div', {'class': 'ratingCol walkScore'}).find('span', {'class': 'scoreDescription'}).text.strip()
        except:
            walkScore = ''  
            walkScore_desc = ''
        
        # get transit score and the corresponding description
        try:
            transitScore = Subpage.find('div', {'class': 'ratingCol transitScore'}).find('span', {'class': 'score'}).text.strip()
            transitScore_desc = Subpage.find('div', {'class': 'ratingCol transitScore'}).find('span', {'class': 'scoreDescription'}).text.strip()
        except:
            transitScore = ''
            transitScore_desc = ''
                    
        # append each apartment's details to Subpage_info
        Subpage_data = {'AverageRating': averageRating, 
                    '# of Reviwer': num_reviewer, 'WalkScore': walkScore, 
                    'WalkScore_desc': walkScore_desc, 'TransitScore': transitScore, 
                    'TransitScore_desc': transitScore_desc, 'Rent_by_room': rent_dict}  
        Subpage_info = Subpage_info.append(Subpage_data, ignore_index = True)
        
    return Subpage_info

'''
main function reads in the 'Apt_Info.csv', calls getSubpage funtion and getDetail
function, merges readin data and subpage information, and writes into a csv file.
'''
def main():
    # read in urls
    apt_info = pd.read_csv('Apt_Info.csv', index_col = 0)
    urls = apt_info['Url'].tolist()
    
    # fetch information on the subpages
    Subpage_list = getSubpage(urls)
    Subpage_info = getDetail(Subpage_list)

    # merge readin information and subpage information
    merged_data = pd.concat([apt_info, Subpage_info], axis = 1)
    
    # write data into csv
    merged_data.to_csv('Merged_Data.csv')

if __name__ == '__main__':    
    main()