from geodesic import Geodesic
from neighborhood import Neighborhood
from math import radians, degrees, pi
import pandas as pd
import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from soan_db_conn import conn_db, cursor
import streamlit as st
from neo4j_connection import UmtsTransmitterGraph
import neighbors as neigh
from neighbors import Neighbors
from sqlalchemy import BigInteger as sqlint



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
    #instatiate an object of the Neighbors class with function for neighbor ranking, bi-direction, and get_cellname
    cell = Neighbors(source_sitename, source_transmitter)
    s_neighbor_ranked = cell.neighbor_ranking(s_neighborhood)
    print('passed ranking neighbors')
    st.text_area(label ="RANKED NEIGHBOR", value="filtered out the transmitter for the co site")
    st.dataframe(s_neighbor_ranked)
    s_bi_directional = cell.bi_directional(s_neighbor_ranked)
    print('passed getting bi directional neighbors')
    #get the transmitter details
    uintrafreq_neighbors = cell.get_cellname(s_bi_directional, conn_db)
    uintrafreq_neighbors = cell.generate_intrafreq_script(uintrafreq_neighbors)
    print(uintrafreq_neighbors)
    print('passed getting cell names')
    print(uintrafreq_neighbors.columns)
    print(uintrafreq_neighbors.isna().sum())
    uintrafreq_neighbors = uintrafreq_neighbors.dropna(how='any')
    uintrafreq_neighbors['source_cellname'] = uintrafreq_neighbors.iloc[0:10, 7].apply(lambda x: (str(x)+'-2'))
    #uintrafreq_neighbors.to_sql(name='uintrafreq', con =conn_db, if_exists='append', schema='dbo', index=False)
    #conn_db.commit()
    
    duplicates = 0
    
    for row in uintrafreq_neighbors.itertuples(index=False):
        try:
            query = "insert into uintrafreq values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            query_no_dups = """if not exists (select source_cellname, target_cellname from uintrafreq 
                                where source_cellname={0} and target_cellname={1}) 
                                insert into uintrafreq values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                                """.format(row.source_cellname, row.target_cellname)
            cursor.execute(query, row.source_site, row.source_transmitter,  row.target_site, row.target_transmitter, 
                            int(row.rank), row.source_bscname, int(row.source_rncid), row.source_cellname, 
                            int(row.source_cellid), row.target_bscname, int(row.target_rncid), row.target_cellname,
                            int(row.target_cellid), int(row.target_psc), int(row.target_lac), int(row.target_rac),  
                            row.uintrafreq_cmd 
                            )
            cursor.commit()
        except Exception as error:
            print(error)
            duplicates +=1
        finally:
            print(duplicates)
    cursor.close()

    # try:
    #     print('confirming written data \n',existing_uintrafreq)
    #     #try writing the same data again
    #     uintrafreq_neighbors.to_sql(name='uintrafreq', con =conn_db, if_exists='append', schema='dbo', index=False)
    #     existing_uintrafreq = pd.read_sql('select count(*) from uintrafreq', conn_db)
    #     #print('2nd writing',rows)
    #     print('confirming written data2 \n',existing_uintrafreq)
    #     print(pd.read_sql('select top 5 * from uintrafreq', conn_db))
    #     conn_db.commit()
    # except Exception:
    #     duplicates +=1
    # finally:
    #     print(f'there were {duplicates} records already existing')

    # #get the umts co_site data
    # safaricom_12015 = UmtsTransmitterGraph("Tom Hanks", "moviegraph")
    # tom_hanks_movie = safaricom_12015.get_movies()
    # print(tom_hanks_movie)
    
    

if __name__ == "__main__":
    main()
    #check
    df = pd.read_sql('select * from uintrafreq', conn_db)
    print(df)
