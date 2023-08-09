from geodesic import Geodesic
from math import radians
import pandas as pd

def source_neighbors(neighbors:pd.DataFrame):
    pass

sites_loc = pd.read_csv("/home/fundi/capstone_project/csfb/test_data_sites.csv")
sites_loc = sites_loc.drop(columns=['Active', 'Antenna', 'DX (m)', 'DY (m)', 'Use Absolute Coordinates'], axis=1)
sites_loc = sites_loc.head(100)
if __name__ == "__main__":
    source_site = Geodesic(radians(1.2), radians(36))
    print(sites_loc.head())
    print(sites_loc.columns)
    n = 0
    s_lat = sites_loc.loc[sites_loc['Transmitter']=="12001_NW_NI40010", "Latitude"]
    s_lon = sites_loc.loc[sites_loc['Transmitter']=="12001_NW_NI40010", "Longitude"]
    print(s_lat, s_lon)
    # neigh_distance = []
    # for i, row in sites_loc.iterrows():
    #     source_site = Geodesic(s_lat, s_lon)
    #     dst12  = source_site.distance(row["Latitude"], row['Longitude'])
    #     neigh_distance.append(dst12)
    # sites_loc["neigh_distance"] = neigh_distance
    neigh_distance_2 = []
    source_site = Geodesic(s_lat, s_lon)
    for row in sites_loc.itertuples(index=False):
        dst12  = source_site.distance(row.Latitude, row.Longitude)
        neigh_distance_2.append(dst12)
    sites_loc["neigh_distance_2"] = neigh_distance_2       

    print(sites_loc.tail())

