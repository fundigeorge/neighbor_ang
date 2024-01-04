from geodesic import Geodesic
from neighborhood import Neighborhood
from math import radians, degrees, pi
import pandas as pd
import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from soan_db_conn import conn_db 
import streamlit as st
from neo4j_connection import UmtsTransmitterGraph
import neighbors as neigh

#user select the site
test_transmitter = "12001_NW_NI40010"
#filter the transmitter from the db
#record the transmitter lat and lon for filtering from the db the neighboring sites of the source site

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
    source_sitename = source_site.loc[:, 'site'].iloc[0]
    source_transmitter = source_site.loc[:, 'transmitter'].iloc[0]
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
    #param:neigh_size ensure atleast neigh_size neighboring site to the source site
    source_neighbors = neighbors.source_neighbors(32)
    print(source_neighbors.head(10), "size of the neighbor", source_neighbors.shape)
    #drop truncated lat and lon columns
    source_neighbors = source_neighbors.drop(columns=['onedp_lat', 'onedp_lon', 'twodp_lat', 'twodp_lon'])
    print('passed dropping columns')
    """calculate best neighbors for the source site"""
    #instantiate a source geodesic object with method to calculte distance btn source_target and best intersection
    source_geodesic = Geodesic(source_lat_rad, source_lon_rad, source_azim_rad, source_coverage)
    print('passed geodesic object instatiation')
    #calculate distance and intersection between source and neighbors
    s_neighborhood = source_geodesic.source_neighbors(source_neighbors)
    print('passed got neighbors to source')
    st.text_area(label='SOURCE NEIGHBORHOOD', value='The calculated intersection and dst12')
    st.dataframe(s_neighborhood)  
    #rank the neighbor and get top neighborhood transmitter
    s_neighbor_ranked = neigh.neighbor_ranking(s_neighborhood, source_sitename, source_transmitter)
    print('passed ranking neighbors')
    st.text_area(label ="RANKED NEIGHBOR", value="filtered out the transmitter for the co site")
    st.dataframe(s_neighbor_ranked)
    s_bi_directional = neigh.bi_directional(s_neighbor_ranked)
    print('passed getting bi directional neighbors')
    print(s_bi_directional)
    neigh.get_cellname(s_bi_directional, conn_db)
    print('passed getting cell names')

    #get the umts co_site data
    # safaricom_12015 = UmtsTransmitterGraph("Tom Hanks", "moviegraph")
    # tom_hanks_movie = safaricom_12015.get_movies()
    # print(tom_hanks_movie)
    
    

if __name__ == "__main__":
    main()
