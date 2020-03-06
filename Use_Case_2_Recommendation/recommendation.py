# -*- coding: utf-8 -*-
"""
@author: Joyqiao
Uses： Apartment recommendation program to custom your preference and
      visualize the result on map
"""

import pandas as pd

#INPUT ATTRIBUTE COLUMN
#OUTPUT MINMAX SCALED COLUMN
def minmax_scale(column):
    float_array = column.values.astype(float)
    minx = min(float_array)
    maxx = max(float_array)
    scaled_array = (float_array - minx)/(maxx - minx)
    return scaled_array


#INPUT COMBINED APARTMENT DATA, USER ENTER THEIR PREFERRED ROOM TYPE
#RETURN DATAFRAME CONTAINS ALL APARTMENTS WITH THE SELECTED ROOM TYPE
def preferred_roomtype(data):
    print('please enter your targeted room type:')
    print('Enter 1 to denote Studio\nEnter 2 to denote 1 bedroom\nEnter 3 to denote 2 bedrooms\nEnter 4 to denote 3 bedrooms\nEnter 5 to denote 4 bedrooms')
    room = int(input('your choice:'))
    #SELECT VALID ROWS AFTER ROO TYPE SELECTION AND SAVE INTO NEW DF
    if room == 1:
        df = data[data['Studio'].notna()]
        df.loc[:,'price'] = df['Studio']
    elif room == 2:
        df = data[data['1 Bed'].notna()]
        df.loc[:,'price'] = df['1 Bed']
    elif room == 3:
        df = data[data['2 Beds'].notna()]
        df.loc[:,'price'] = df['2 Beds']
    elif room == 4:
        df = data[data['3 Beds'].notna()]
        df.loc[:,'price'] = df['3 Beds']
    elif room == 5:
        df = data[data['3 Beds'].notna()]
        df.loc[:,'price'] = df['4 Beds']
    else:
        print('error')
    
    return df
        
#INPUT PREVIOUS DF
#USER INPUT THEIR SCORE PREFERENCE FROM 1-5 SEPARATIVELY TO PRICE,SAFETY,DISTANCE,RESTARANT NUMBER AND TRANSIT SCORE      
#OUTPUT 10 RECOMMENDED APARTMENT INFO DF
def recommendation_calculator(df):
    
    #SCALE ALL THE METRICS
    price = minmax_scale(df['price'])
    safety = minmax_scale(df['crime_count_pct']) * (-1)
    distance = minmax_scale(df['distance'])
    res_n = minmax_scale(df['restaurant_n'])
    transit = minmax_scale(df['TransitScore']) 
    
    #USER ENTER POINTS
    #HELP TO CALCULATE AND CONFIRM THEIR FINAL CHOICE
    a = 0
    while a == 0:     
        print("Please Allocate total points of 100 across 5 metrics: \nPrice, safety, distance to heinz, nearby restaurant and transit convenience according to your perceived value as it relates to apartment preference.\nIt’s ok to score 0 or 100 to one metric.")
        price_w = float(input('price points:'))
        print('Your remaining score is {}'.format(100 - price_w))
        safety_w = float(input('safety points:'))
        print('Your remaining score is {}'.format(100 - price_w - safety_w))
        distance_w = float(input('distance points:'))
        print('Your remaining score is {}'.format(100 - price_w - safety_w - distance_w))
        resta_w = float(input('restaurant number points:'))
        print('Your remaining score is {}'.format(100 - price_w - safety_w - distance_w - resta_w))
        transit_w = float(input('Transit convenience points:'))
        
        if price_w + safety_w + distance_w + resta_w +transit_w == float(100):
            a = float(input('Do you want to proceed or re-set your points? proceed enter 1, re-set enter 0: '))
        else:
            print('Error. Sum of points is not 10. Please re-set your points\n')
    
    #CALCULATE FINAL SCORE
    final_score = price_w * price + safety_w * safety + distance_w * distance + resta_w * res_n + transit_w * transit
    df.loc[:,'final_score'] = final_score
    df = df.sort_values(by ='final_score',ascending = False) #SORT BY FINAL SCORE
    
    #MAKE SURE WE ARE ABLE TO SELECT TOP 10 OR WHATEVER WE HAVE IF ROW NUMBER LESS THAN 10
    if len(df) >= 10:
        recommended_apt_df = df[:10] 
    else:
        recommended_apt_df = df
    print('Done')
    
    return recommended_apt_df


def main():
    raw_data = pd.read_csv('apt_combined_data.csv') #READ IN CSV GENERATED FROM APT_COMBINE_DATA.PY
    df = preferred_roomtype(raw_data) #USER ENTER ROOMTYPE
    target_data = recommendation_calculator(df) #CALCULATE
    
    import map_apt #IMPORT MAP_APT TO VISUALIZE THE TOP 10 ON MAP
    map_apt.main(target_data,'recommended_map.html')
    target_data.to_csv('recommended_data.csv')
    

if __name__ == '__main__':
    main()


