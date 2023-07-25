from math import radians
import pandas as pd
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
    lat2=radians(-1.280823) #0.709186 -1.280823 36.822151
    lon2=radians(36.822151) #1.287762
    crs13 = 20
    crs23 = 270

    source = Geodesic(lat1, lon1)
    closest_intersect = source.best_intersection(lat2, lon2, crs13, crs23)
    print(closest_intersect)
    crs13 = radians(50)
    crs23 = radians(300)
    print("manual calc", crs13, crs23)
    print("distance to point 2", source.distance(lat2, lon2))
    try:
        print(source.bearing(lat2, lon2))
        print(source.intersection(lat2, lon2, crs13, crs23))
    except ZeroDivisionError as error:
        print("same location")

    
