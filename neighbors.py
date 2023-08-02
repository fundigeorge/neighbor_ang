from math import radians, degrees
import pandas as pd
import numpy as np
from geodesic import Geodesic




if __name__ == "__main__":
    """ETL

    Extract:
    extract data from mssql db to pandas dataframe or spark dataframe

    Transform:
    calculate distance, bearing, intersection to each neighbor

    Load:
    store the processed neighbor to db
    """
    #select the site of interest by site id or coordinate
    #use the coordinate to filter a given number of neighboring sites
    lat1=radians(-1.2814722) #0.592539 -1.2814722 36.8209444
    lon1=radians(36.8209444) #2.066470
    #lat lon in radians
    lat2=radians(-1.280823) #0.709186 -1.280823 36.822151, 179, 239, 209(all ambigous)
    lon2=radians(36.822151) #1.287762
    lat3=radians(-1.277733) # -1.277733  36.827901
    lon3=radians(36.827901)
    crs13 = 20
    crs23 = 212

    source = Geodesic(lat1, lon1)
    bearing = source.bearing(lat2, lon2)
    print(bearing)
    print("distance to point 2", source.distance(lat2, lon2))
    crs13 = radians(bearing+10)
    crs23 = radians(bearing+10)
    fdelta = 5
    closest_intersect = source.macro_best_intersection(lat2, lon2, crs13, crs23)
    print('closest_intersect:fdelta=5', closest_intersect)
    print("manual calc", degrees(crs13), degrees(crs23))
    fdelta = 10 
    closest_intersect = source.macro_best_intersection(lat2, lon2, crs13, crs23)  
    print('closest_intersect:fdelta=10', closest_intersect) 
    try:
        
        print(source.intersection(lat2, lon2, crs13, crs23))
    except ZeroDivisionError as error:
        print("same location")
    except ValueError as e:
        print("ambigouos intersection")

#test for micro ibs
    source_micro = Geodesic(lat1, lon1)
    source_azim = radians(source_micro.bearing(lat2, lon2)-10)
    crs12 = radians(source_micro.bearing(lat2, lon2))
    print('testing macro to micro function\n...............')
    ibs_directness = source_micro.micro_best_intersection(lat2, lon2, source_azim, "macro")   
    print('directness', ibs_directness)

#test for IBS to macro target
    source_ibs = Geodesic(lat1, lon1)
    print('\ntesting ibs to macro directness..............')
    print("bearing ibs to macro", source_ibs.bearing(lat2, lon2))
    target_azimuth = (source_ibs.bearing(lat2, lon2) + 180) %360
    print("bearing from macro to ibs", target_azimuth)
    target_azimuth = radians(target_azimuth-360)
    site_type = "micro"
    directness = source_ibs.micro_best_intersection(lat2, lon2, target_azimuth, site_type)
    print('directness', directness)

# test_azimuth = np.arange(11, 360, 30)  
# ambigous_cases = 0
# crs13 = radians(20)
# for a in test_azimuth:    
#     print(f'for azimuth {a}')
#     print(f'-----------------------')
#     a = radians(a)
#     try:
#         neigh = source.best_intersection(lat2, lon2, crs13, a)
#         print('best intersection', neigh)
#     except ValueError as e:
#          print("message from function:", str(e))
#          ambigous_cases +=1
     
# print(f'total number = {len(test_azimuth)}, ambiguous case:{ambigous_cases}, ')
     