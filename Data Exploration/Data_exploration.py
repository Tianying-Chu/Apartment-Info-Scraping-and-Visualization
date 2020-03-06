# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 17:21:51 2020

@author: Yanyi Qian
"""
'''exploratory data analysis (EDA): give us a better understanding about the 
apartment and crime data by analyzing and visualizing the distribution of them'''

import pandas as pd
import seaborn as sns

# Apartment data exploration
# for apartment data, we will focus on the distribution of AvarageRateing, WalkScore and TransitScore
aparts = pd.read_csv('Cleaned_Data.csv', dtype = {'WalkScore' : int, 'TransitScore' : int}) #import cleaned apartment data

# Calculate the number of missing value in each column
num_missing = aparts.isnull().sum(axis=0)
print(num_missing)

# Analysing the distribution of the three columns
aparts_stats = aparts.describe().loc[:, ['AverageRating', 'WalkScore', 'TransitScore']]
print(aparts_stats)

'''the range of AverageRating is 0 to 5, and the range of WalkScore & TransitScore are 0-100,
thus we create two separate boxplots'''
aparts.loc[:,['AverageRating']].boxplot()
aparts.loc[:,['WalkScore', 'TransitScore']].boxplot()


# Crime data exploration
# for crime data, we only care about 'ARRESTTIME' and 'COUNCIL_DISTRICT'
crime = pd.read_csv('Pittsburgh Police Arrest Data.csv')

# Calculate the number of missing value in each column
num_missing = crime.isnull().sum(axis=0)
print(num_missing)

# extract crime year and month from column 'ARRESTTIME'
split_time = crime['ARRESTTIME'].str.split('-').to_list()
crime['CRIME_YEAR'] = [i[0] for i in split_time]
crime['CRIME_MONTH'] = [i[1] for i in split_time]

# Calculate the number of crimes in each council and in each year
crime_stats = crime.groupby(['CRIME_YEAR','COUNCIL_DISTRICT'], as_index=False)['PK'].count()
crime_stats.rename(columns={"PK": "# of Crimes"}, inplace = True)

print(crime_stats)

crime_4years = crime_stats[(crime_stats['CRIME_YEAR'].apply(int)>2015) & (crime_stats['CRIME_YEAR'].apply(int)<2020)]

crime_distribution = sns.factorplot(x='COUNCIL_DISTRICT', y='# of Crimes', col='CRIME_YEAR',\
                                    col_wrap=2, kind='bar', data=crime_4years)        