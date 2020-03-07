# Apartment-Info Scraping & Visualization
## Group Members: Tianying Chu, Yanyi Qian, Zhaoyu Qiao, Guoyu Wu

## Basic concept: 
When making a decision regarding relocation, it is necessary to consider various factors including price, room type, transitional convenience, and nearby recreational facilities. Furthermore, a high crime rate would make residents feel vulnerable. As crime goes up, home values tend to drop. Existing websites lack the above combination and fail to customize apartment features according to users’ preferences.
## Overall objective: 
Our project aims to combine apartment information with factors that influence residential experience into one place.
We scraped the apartment information in Pittsburgh from apartments.com, one of the most popular apartment websites in America, and we downloaded the crime information CSV from Data.gov, which is hosted by the U.S. General Services Administration. To make the information more intuitive and understandable, Google Maps API was used to locate nearby facilities, calculate distances, and visualize the crime distribution.
## Use cases: 
Assume you are an incoming CMU Heinz student and planning to rent an apartment in Fall 2020. You have many considerations in your head, like price, safety, room type, convenience, and you have different priorities toward these factors. In this case, our application can help you determine which neighborhood most fits your preferences.
## Sources of data:
Web Scraping: apartments.com

API: Google Maps API  - Geocoding API / Places API 

CSV file: Pittsburgh Police Arrest Data.csv - downloaded from Data.gov

Others: Pittsburgh City Council Boundary Geojson data - download from Pittsburgh open data

