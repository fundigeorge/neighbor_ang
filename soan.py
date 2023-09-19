from geodesic import Geodesic
from neighborhood import Neighborhood
from math import radians, degrees, pi
import pandas as pd

sites_loc = pd.read_csv("/home/fundi/capstone_project/csfb/test_data_sites.csv")
sites_loc = sites_loc.drop(columns=['Active', 'Antenna', 'DX (m)', 'DY (m)', 'Use Absolute Coordinates'], axis=1)
#sites_loc = sites_loc.head(100)
sites_loc.columns = sites_loc.columns.str.lower().str.replace(" ", "_").\
                    str.replace("(","").str.replace(")","")
sites_loc.rename(columns={'azimuth_°':'azimuth'}, inplace=True)
sites_loc = sites_loc.loc[:, ['site', 'transmitter', 'latitude', 'longitude', 'height_m', 'azimuth']]
sites_loc["radian_lat"] = sites_loc.loc[:, 'latitude'].apply(lambda x: radians(x))
sites_loc["radian_lon"] = sites_loc.loc[:, 'longitude'].apply(lambda x: radians(x))
sites_loc['radian_azim'] = sites_loc.loc[:, 'azimuth'].apply(lambda x: radians(x))
sites_loc.loc[:, 'coverage'] = "macro"
sites_loc.loc[15:30, 'coverage'] = "micro"
sites_loc["onedp_lat"] = sites_loc.loc[:, "latitude"].apply(lambda x: round(x, 1))
sites_loc["onedp_lon"] = sites_loc.loc[:, "longitude"].apply(lambda x: round(x, 1))
sites_loc["twodp_lat"] = sites_loc.loc[:, "latitude"].apply(lambda x: round(x, 2))
sites_loc["twodp_lon"] = sites_loc.loc[:, "longitude"].apply(lambda x: round(x, 2))


print(sites_loc.sample(20))
print(sites_loc.columns)



if __name__ == "__main__":
    n = 0    
    s_lat = sites_loc.loc[sites_loc['transmitter']=="12001_NW_NI40010", "radian_lat"].iloc[0]
    s_lon = sites_loc.loc[sites_loc['transmitter']=="12001_NW_NI40010", "radian_lon"].iloc[0]    
    s_lat_deg = sites_loc.loc[sites_loc['transmitter']=="12001_NW_NI40010", "latitude"].iloc[0]
    s_lon_deg = sites_loc.loc[sites_loc['transmitter']=="12001_NW_NI40010", "longitude"].iloc[0]
    s_azim =radians(0) #sites_loc.loc[sites_loc['transmitter']=="12001_NW_NI40010", "radian_azim"].astype(float)
    s_coverage ='macro' #sites_loc.loc[sites_loc['transmitter']=="12001_NW_NI40010", "coverage"]
    print(s_lat, s_lon, s_azim, s_coverage, type(s_coverage)) # -1.26123 36.798874 

    #get neighboring site to the source site
    print('................')
    source_neigh = Neighborhood(s_lat_deg, s_lon_deg, sites_loc)
    print("all sites", sites_loc.drop_duplicates(subset="site").shape)
    print("all transmitter", sites_loc.shape)
    neigh_sites = source_neigh.source_neighbors()
    neigh_sites.to_excel("/home/fundi/capstone_project/csfb/neigh_sites.xlsx", index=False)
    #testing getting neighbors to a source site
    
    #iterate through all the neighbor
    neigh_distance = []
    source_site = Geodesic(s_lat, s_lon, s_azim, s_coverage) # -1.26122956 36.79887354 36.79887354	
    teleposta_lat= radians(-1.25) #-1.285864 36.819414
    teleposta_lon = radians(36.82)
    tel_az = radians(0) #350.3
    upperhill_lat = radians(-1.27) # -1.294004  36.810818
    upperhill_lon = radians(36.78)
    upp_az = radians(0) #318
    kahawa_lat = radians(-1.184558) # -1.184558 36.925092
    kahawa_lon=radians(36.925092)
    kah_az = radians(247)
    kiambu_lat = radians(-1.167349) #-1.167349 36.824985
    kiambu_lon=radians(36.824985)
    kia_az = radians(274)
   
    # print('................')
    # print(source_site.lat, source_site.lon, source_site.azim, source_site.coverage)

    # print('TESTING DISTANCE BETWEEN SITES')
    # print('................')
    # print('teleposta distance', source_site.distance(teleposta_lat, s_lon))
    # print('upperhill distance', source_site.distance(upperhill_lat, upperhill_lon))
    # print('kahawa distance', source_site.distance(kahawa_lat, kahawa_lon))
    # print('kiambu distance', source_site.distance(kiambu_lat, kiambu_lon))
    # print('..................')

    # print('TESTING BEARING BETWEEN SITES')
    # print('................')
    #same point as source-target raise zeroDivisionError
    # #same s_lon and t_lon raise valueError "math domain error"
    # try:    
    #     print('teleposta bearing', source_site.bearing(teleposta_lat, s_lon))
    # except ZeroDivisionError as e:
    #     print("same point")
    # try:
    #     print('upperhill bearing', source_site.bearing(upperhill_lat, s_lon))
    # except ZeroDivisionError as e:
    #     print("same point")
    # try:
    #     print('kahawa bearing', source_site.bearing(kahawa_lat, kahawa_lon))
    # except ZeroDivisionError as e:
    #     print("same point")
    # try:
    #     print('kiambu bearing', source_site.bearing(kiambu_lat, kiambu_lon))
    # except ZeroDivisionError as e:
    #     print("same point")
    # print('..................')
    
    # print('TESTING INTERSECTION BETWEEN SITES')
    # print('................')
    # try:
    #     print('teleposta intersection', source_site.intersection(teleposta_lat, s_lon, s_azim, s_azim))
    # except ValueError as e:
    #     print('teleposta intersection', e)
    # except ZeroDivisionError as e:
    #     print(e, "same point")
    # try:
    #     print('teleposta intersection', source_site.intersection(teleposta_lat, s_lon, s_azim, tel_az))
    # except ValueError as e:
    #     print('teleposta intersection', e)
    # except ZeroDivisionError as e:
    #     print(e, "same point")
    # try:
    #     print('upperhill intersection', source_site.intersection(upperhill_lat, s_lon, s_azim, s_azim))
    # except ValueError as e:
    #     print('upperhill intersection', e)
    # except ZeroDivisionError as e:
    #     print(e, "same point")
    # try:
    #     print('upperhill intersection', source_site.intersection(upperhill_lat, s_lon, s_azim, upp_az))
    # except ValueError as e:
    #     print('upperhill intersection', e)
    # except ZeroDivisionError as e:
    #     print(e, "same point")
    # try:
    #     print('kahawa intersection', source_site.intersection(kahawa_lat, kahawa_lon, s_azim, kah_az))
    # except ValueError as e:
    #     print('kahawa intersection', e)
    # except ZeroDivisionError as e:
    #     print(e, "same point")
    # try:
    #     print('kiambu intersection', source_site.intersection(kiambu_lat, kiambu_lon, s_azim, kia_az))
    # except ValueError as e:
    #     print('kiambu intersection', e)
    # except ZeroDivisionError as e:
    #     print(e, "same point")
    # print('..................')

    # print('TESTING MACRO INTERSECTION BETWEEN SITES')
    # print('................') 
    # print('teleposta1:', source_site.macro_intersection(teleposta_lat, s_lon, radians(30))) 
    # print('teleposta2:', source_site.macro_intersection(teleposta_lat, s_lon, radians(150))) 
    # print('upperhill1:', source_site.macro_intersection(upperhill_lat, s_lon, radians(30))) 
    # print('upperhill2:', source_site.macro_intersection(upperhill_lat, s_lon, radians(150))) 
    # print('kahawa:', source_site.macro_intersection(kahawa_lat, kahawa_lon, kah_az)) 
    # print('kiambu:', source_site.macro_intersection(kiambu_lat, kiambu_lon, kia_az)) 


    # print('TESTING MACRO-MICR0 INTERSECTION BETWEEN SITES')
    # print('................') 
    # print('teleposta1:', source_site.micro_intersection(teleposta_lat, s_lon, radians(0+15))) 
    # print('...') 
    # print('teleposta2:', source_site.micro_intersection(teleposta_lat, s_lon, radians(180+15))) 
    # print('...') 
    # print('upperhill1:', source_site.micro_intersection(upperhill_lat, s_lon, radians(0+15))) 
    # print('...') 
    # print('upperhill2:', source_site.micro_intersection(upperhill_lat, s_lon, radians(180+15)))
    # print('...')  
    # print('kahawa:', source_site.micro_intersection(kahawa_lat, kahawa_lon, kah_az)) 
    # print('kiambu:', source_site.micro_intersection(kiambu_lat, kiambu_lon, kia_az)) 

    # print('TESTING MICRO-MACRO INTERSECTION BETWEEN SITES')
    # print('................') 
    # print('teleposta1:', source_site.micro_intersection(teleposta_lat, s_lon, radians(0+15), 'micro'))
    # print('...')  
    # print('teleposta1:', source_site.micro_intersection(teleposta_lat, s_lon, radians(180+15), 'micro'))
    # print('...')  
    # print('upperhill1:', source_site.micro_intersection(upperhill_lat, s_lon, radians(0+15),'micro'))
    # print('...')  
    # print('upperhill2:', source_site.micro_intersection(upperhill_lat, s_lon, radians(180+15), 'micro'))
    # print('...')  
    # print('kahawa:', source_site.micro_intersection(kahawa_lat, kahawa_lon, kah_az, 'micro')) 
    # print('kiambu:', source_site.micro_intersection(kiambu_lat, kiambu_lon, kia_az, 'micro')) 

    # print('TESTING BEST NEIGHBOR FUNCTION')
    # print('................') 
    # neighbors = source_site.source_neighbors(sites_loc)
    # #excel_writer = pd.ExcelWriter(engine='openpyxl')
    # neighbors.to_excel('/home/fundi/capstone_project/csfb/neighbors.xlsx', index=False)

