# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 18:51:40 2020

@author: Tianying Chu
"""

'''
Data_Cleaning.py splits the 'Rent_by_room' column into 5 new columns ('Studio', 
'1 Bed', '2 Beds', '3 Beds', '4 Beds'), calculate the average for each new column,
and removes apartment records without detailed location or with abnormal values.
'''

import pandas as pd
import numpy as np

'''
Rent_info function deals with the dictionary for 'Rent_by_room' column 
input: the 'Rent_by_room' column that needs to be split (a list of dictionary)
return: a Dataframe of the 5 new columns (representing the average price)
'''
def Rent_info(rent_dict):
    # define the room types we need
    room_types = ['Studio', '1 Bed', '2 Beds', '3 Beds', '4 Beds']
    
    rent_info = pd.DataFrame(columns = room_types)
    
    # loop for each apartment
    for row_dict in rent_dict:
        # calculate average prices for each room type
        Studio_mean = getMeanPrice(row_dict, room_types[0])
        One_bed_mean = getMeanPrice(row_dict, room_types[1])
        Two_beds_mean = getMeanPrice(row_dict, room_types[2])
        Three_beds_mean = getMeanPrice(row_dict, room_types[3])
        Four_beds_mean = getMeanPrice(row_dict, room_types[4])
        
        # append each apartment's rent to rent_info
        rent_data = {
                'Studio': Studio_mean, '1 Bed': One_bed_mean, 
                '2 Beds': Two_beds_mean, '3 Beds': Three_beds_mean, 
                '4 Beds': Four_beds_mean
                }
        rent_info = rent_info.append(rent_data, ignore_index = True)

    return rent_info

'''
getMeanPrice function calculates average price for a specific room type in an apartment
input: 'Rent_by_room' of an apartment (a dictionary), a specific room type
return: the average price for a specific room type in that apartment
'''
def getMeanPrice(row_dict, room_type):
    try:
        # price_list collects the prices of a specific room type in one apartment
        price_list = list()
        # get the lower bound and upper bound of the price
        for price in eval(row_dict)[room_type].split('–'):
            price_list.append(getDigit(price))
    except:
        price_list = ['']
    
    # calculate the average price if the price exists
    if price_list != ['']:
        mean = np.mean(price_list)
    else:
        mean = None
    return mean

'''
getDigit function get price value from complex string (the original string contains special characters like $, ,, ...)
input: a complex string containing the price value
return: the price value in the string (int)
'''
def getDigit(string):
    digit = ''
    
    # loop for each character in the string, keep the character if it is a digit
    for i in string:
        if i.isdigit():
            digit += i
        else:
            pass
    digit = int(digit)
    return digit

'''
main function reads in the 'Merged_Data.csv', calls Rent_info function, 
concatenates the original data with new rent information, remove unvalid records,
and writes the cleaned data into a csv file.
'''
def main():
    
    # import data and show its structure
    data = pd.read_csv('Merged_Data.csv', index_col = 0)
    print(data.info())

    # split 'Rent_by_room' column into seperate columns
    rent_info = Rent_info(data['Rent_by_room'])
    
    # add rent information into table
    data_with_rent = pd.concat([data, rent_info], axis = 1)

    # remove apartment records without detailed location
    no_location = data_with_rent['Location'].str.split(',').str[0].str.contains('Pittsburgh')
    data_with_location = data_with_rent[~ no_location]

    # remove abnormal value in TransitScore
    abnormal_TransitScore = data_with_location['TransitScore'].str.contains('-')
    cleaned_data = data_with_location[~ abnormal_TransitScore]

    # write data into csv and display its structure
    cleaned_data.to_csv('Cleaned_Data.csv')
    print(cleaned_data.info())

if __name__ == '__main__':
    main()