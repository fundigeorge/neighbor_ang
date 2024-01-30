import pandas as pd
import sqlalchemy
from soan_db_conn import conn_db

class Neighborhood:
        
    """ a class for find the neighboring sites to source site. given source lat, lon and
    taking the ones(1.1km), lat,lon to 2dp given a square grid around the source site of
    1.1km. 1dp gives a grid of 11km by 11km, 3dp gives a grid of 100m by 100
    ...

    Attributes
    ----------
    lat : float
        The latitude for source site
    lon : float
        the longitude for the source site

    Methods
    -------
    expanded_region(): determine the lat lon making the grid around the source site
    """
    def __init__(self, lat, lon, freq:str):
        self.lat = lat
        self.lon = lon
        self.dp = 2
        self.offset = 0.01
        self.site_size = 32
        self.freq = freq

    def expanded_region(self, dp, offset):
        lat = round(self.lat, dp)   
        lon =round(self.lon, dp)
        lat_d = round((self.lat-offset), dp)
        lat_u = round((self.lat+offset), dp)
        lon_d = round((self.lon-offset), dp)
        lon_u = round((self.lon+offset), dp)    
        grids= [[lat_d, lon_d], [lat_d, lon], [lat_d, lon_u],
            [lat, lon_d], [lat, lon], [lat, lon_u],
            [lat_u, lon_d], [lat_u, lon], [lat_u, lon_u],
            ]
        return grids

    def source_neighbors(self, neigh_size):
        #define the number of neighbors site for the source site
        self.site_size = neigh_size
        #determine the 1km square around the site
        lat = round(self.lat, self.dp)
        lon = round(self.lon, self.dp)
        #filter from the db  any transmitter with twodp_lat and twodp equal to the source site
        #todo, pick only the site, transmitter, lat, lon, azimuth fields
        #todo what is impact of neigh_sites as a local variable and a object variable
        #added checking the transmitter frequency i.e 10587, 10562, 2949
        query =  f"""select tx.*, cell.uarfc_downlink 
                    from umts_transmitter tx
                    left join umts_cells cell 
                    on tx.transmitter = cell.atoll_transmitter
                    where (onedp_lat = {lat} and onedp_lon = {lon}) and cell.uarfc_downlink = {self.freq}
                    """
        neigh_sites = pd.read_sql(query, conn_db)
        unique_sites = neigh_sites.drop_duplicates(subset ="site").shape 
        # print("sites:transmitter", pd.read_sql('select count(*) from umts_transmitter', conn_db))
        # print("sites:sites", pd.read_sql('select COUNT(DISTINCT site) from umts_transmitter', conn_db))
        # print("region:transmitter", neigh_sites.shape)
        # print("region:sites", neigh_sites.drop_duplicates(subset="site").shape) 
          
        #check if no of site is > neigh_size, if not expand the search area
        if unique_sites[0] >= self.site_size:
            return neigh_sites       
        
        #if no of sites in area is less expand area to 3.3km sqaurearound the site       
        grids = self.expanded_region(self.dp, self.offset)
        # print(grids)
        query = f""" select tx.*, cell.uarfc_downlink
                     from umts_transmitter tx
                     left join umts_cells cell
                     on tx.transmitter = cell.atoll_transmitter
                     where ( 
                                (twodp_lat={grids[0][0]} and twodp_lon={grids[0][1]}) or
                                (twodp_lat={grids[1][0]} and twodp_lon={grids[1][1]}) or
                                (twodp_lat={grids[2][0]} and twodp_lon={grids[2][1]}) or
                                (twodp_lat={grids[3][0]} and twodp_lon={grids[3][1]}) or
                                (twodp_lat={grids[4][0]} and twodp_lon={grids[4][1]}) or
                                (twodp_lat={grids[5][0]} and twodp_lon={grids[5][1]}) or
                                (twodp_lat={grids[6][0]} and twodp_lon={grids[6][1]}) or
                                (twodp_lat={grids[7][0]} and twodp_lon={grids[7][1]}) or
                                (twodp_lat={grids[8][0]} and twodp_lon={grids[8][1]}) 
                            ) AND cell.uarfc_downlink = {self.freq}
                    """
        neigh_sites = pd.read_sql(query, conn_db)
        #check if number of site >= 30
        unique_sites = neigh_sites.drop_duplicates(subset="site").shape
        # print("3.3km square", neigh_sites.shape)
        # print("3.3km square", unique_sites)
        if unique_sites[0] >= self.site_size:
            # print("expanded unique 3.3km", neigh_sites.drop_duplicates(subset="site").shape)
            return neigh_sites
        
        #if no of site is less expand the area to 11km square around source
        lat = round(self.lat, 1)
        lon = round(self.lon, 1)
        #filter transmitter on this lat lon combination
        query = f"""select tx.*, cell.uarfc_downlink 
                    from umts_transmitter tx
                    left join umts_cells cell 
                    on tx.transmitter = cell.atoll_transmitter
                    where (onedp_lat = {lat} and onedp_lon = {lon}) and cell.uarfc_downlink = {self.freq}
                    """
        neigh_sites = pd.read_sql(query, conn_db)
        unique_sites = neigh_sites.drop_duplicates(subset="site").shape
        # print("11km square", neigh_sites.shape)
        # print("11km square", unique_sites)
        if unique_sites[0] >= self.site_size:
            # print("returning from 11km")
            return neigh_sites
        
        #if no site is less expand the area to 33km square around the surce
        grids = self.expanded_region(1, 0.1)
        # print(grids)
        query = f""" select tx.*, cell.uarfc_downlink 
                    from umts_transmitter tx
                    left join umts_cells cell 
                    on tx.transmitter = cell.atoll_transmitter
                    where ( 
                                (onedp_lat={grids[0][0]} and onedp_lon={grids[0][1]}) or
                                (onedp_lat={grids[1][0]} and onedp_lon={grids[1][1]}) or
                                (onedp_lat={grids[2][0]} and onedp_lon={grids[2][1]}) or
                                (onedp_lat={grids[3][0]} and onedp_lon={grids[3][1]}) or
                                (onedp_lat={grids[4][0]} and onedp_lon={grids[4][1]}) or
                                (onedp_lat={grids[5][0]} and onedp_lon={grids[5][1]}) or
                                (onedp_lat={grids[6][0]} and onedp_lon={grids[6][1]}) or
                                (onedp_lat={grids[7][0]} and onedp_lon={grids[7][1]}) or
                                (onedp_lat={grids[8][0]} and onedp_lon={grids[8][1]}) 
                            ) AND cell.uarfc_downlink = {self.freq}                                      
                    """            
        neigh_sites =pd.read_sql(query, conn_db)
        unique_sites = neigh_sites.drop_duplicates(subset="site").shape
        # print(unique_sites)
        # print("33km square", neigh_sites.shape)
        # print("33km square", unique_sites)
        #33km square around the site is largest area to be considered
        return neigh_sites

        
            
        

        