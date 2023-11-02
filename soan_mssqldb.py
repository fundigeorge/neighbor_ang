from geodesic import Geodesic
from neighborhood import Neighborhood
from math import radians, degrees, pi
import pandas as pd
import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from soan_db_conn import conn_db 
import streamlit as st

#user select the site
test_transmitter = "12001_NW_NI40010"
#filter the transmitter from the db
#record the transmitter lat an lon for filtering from the db the neighboring sites of the source site

def main():
    """select a transmitter from the db as the source site"""
    #get all the transmitter from the db
    all_transmitter = pd.read_sql("select transmitter from umts_transmitter", conn_db)
    #avail all the transmitter on selection button
    umts_transmitter = st.selectbox(label ="select umts transmitter", options=all_transmitter)
    print(umts_transmitter)
    #get the selected transmitter from the db
    source_site = pd.read_sql(f"select * from umts_transmitter where transmitter = '{umts_transmitter}' ", conn_db)
    print('\ngot transmitter\n', source_site)
    #get the transmitter lat and lon and azimuth
    source_lat = source_site.loc[:, 'latitude'].iloc[0]
    source_lon = source_site.loc[:, 'longitude'].iloc[0]
    source_azim = source_site.loc[:, 'azimuth'].iloc[0]
    source_coverage = source_site.loc[:, 'coverage'].iloc[0]
    source_lat_rad = source_site.loc[:, 'radian_lat'].iloc[0]
    source_lon_rad = source_site.loc[:, 'radian_lon'].iloc[0]
    source_azim_rad = source_site.loc[:, 'radian_azim'].iloc[0]

    print(source_lat, source_lon, source_azim, '\n')
   
    """with source lat lon get the neighbor sites...4"""
    neighbors = Neighborhood(source_lat, source_lon)
    source_neighbors = neighbors.source_neighbors(32)
    print(source_neighbors.head(10), "size of the neighbor", source_neighbors.shape)

    """calculate best neighbors for the source site"""
    #instantiate a source geodesic object with method to calculte distance btn source_target and best intersection
    source_geodesic = Geodesic(source_lat_rad, source_lon_rad, source_azim_rad, source_coverage)
    #calculate distance and intersection between source and neighbors
    source_neighborhood = source_geodesic.source_neighbors(source_neighbors)
    print("calculate neighborhood", source_neighborhood.head())
    
    

if __name__ == "__main__":
    main()
