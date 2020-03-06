# Apartment-Info Scraping & Visualization

## Basic concept: 
When making a decision regarding relocation, it is necessary to consider various factors including transitional convenience, price, room type and nearby recreation facility. Furthermore, a high crime rate would make residents feel vulnerable. As crime goes up, home values tend to drop. Existing websites lack the above combination and fail to customize apartment features according to users’ preferences.
## Overall objective: 
Our project aims to combine apartment information with crime information together into one place.​ We scraped the apartment information in Pittsburgh from ​apartments.com​, one of the most popular apartment websites in American, and we downloaded the crime_info csv from ​Data.gov​, which is hosted by the U.S. General Services Administration. To make the information more intuitive and understandable, ​Google
Maps API ​was used to locate nearby facilities, calculate distances, visualize the crime distribution, apartment features, and compare them based on the user’s priorities.
## Use cases: 
Assume you are an incoming CMU Heinz student and planning to rent an apartment in Fall 2020. You have many considerations in your head, ​like price, safety, room type, convenience, ​and you have different priorities toward these factors. In this case, our application can help you determine which neighborhood most fits your preferences.
## Sources of data:
Web Scraping: apartments.com (​https://www.apartments.com/​)

API: Google Map API - Geocoding API / Places API
(​https://developers.google.com/maps/documentation/geocoding/intro​)
(​https://developers.google.com/places/web-service/search?hl=zh-tw​)

CSV: Pittsburgh Police Arrest Data.csv - downloaded from Data.gov
(​https://catalog.data.gov/dataset/pittsburgh-police-arrest-data​)
