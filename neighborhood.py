import pandas as pd

class Neighborhood:
        
    """ a class for find the neighboring sites to source site. given source lat, lon and
    taking the tenth(11km), lat,lon to 1dp given a square grid around the source site of
    11km. 2dp gives a grid of 1km by 1km, 3dp gives a grid of 100m by 100
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
    def __init__(self, lat, lon, sites:pd.DataFrame, dp, offset = 0.1):
        self.lat = lat
        self.lon = lon
        self.sites = sites
        self.dp = dp
        self.offset = offset
        self.site_size = 30

    def expanded_region(self):
        lat = round(self.lat, self.dp)   
        lon =round(self.lon, self.dp)
        lat_d = round(self.lat-self.offset, self.dp)
        lat_u = round(self.lat+self.offset, self.dp)
        lon_d = round(self.lon-self.offset, self.dp)
        lon_u = round(self.lon+self.offset, self.dp)    
        grids= [[lat_d, lon_d], [lat_d, lon], [lat_d, lon_u],
            [lat, lon_d], [lat, lon], [lat, lon_u],
            [lat_u, lon_d], [lat_u, lon], [lat_u, lon_u],
            ]
        return grids

    def source_neighbors(self,):
        #determine the 11km square around the site
        lat = round(self.lat, self.dp)
        lon = round(self.lon, self.dp)
        region_sites = self.sites.loc[(self.sites["tenth_lat"]==lat) & (self.sites["tenth_lon"]==lon), :]
        unique_sites = region_sites.drop_duplicates(subset ="site").shape    
       
        if unique_sites[0] > self.site_size: 
            print(unique_sites)  
            return region_sites
        #if no of sites in area is less expand area
        else:
            grids = self.expanded_region()
            region_sites = self.sites.loc[((self.sites['tenth_lat']==grids[0][0])&(self.sites['tenth_lon']==grids[0][1])) | 
                                          ((self.sites['tenth_lat']==grids[1][0])&(self.sites['tenth_lon']==grids[1][1])) |  
                                          ((self.sites['tenth_lat']==grids[2][0])&(self.sites['tenth_lon']==grids[2][1])) | 
                                          ((self.sites['tenth_lat']==grids[3][0])&(self.sites['tenth_lon']==grids[3][1])) | 
                                          ((self.sites['tenth_lat']==grids[4][0])&(self.sites['tenth_lon']==grids[4][1])) |
                                          ((self.sites['tenth_lat']==grids[5][0])&(self.sites['tenth_lon']==grids[5][1])) |
                                          ((self.sites['tenth_lat']==grids[6][0])&(self.sites['tenth_lon']==grids[6][1])) |  
                                          ((self.sites['tenth_lat']==grids[7][0])&(self.sites['tenth_lon']==grids[7][1])) | 
                                          ((self.sites['tenth_lat']==grids[8][0])&(self.sites['tenth_lon']==grids[8][1])), : 
             
            print(region_sites.drop_duplicates(subset="site").shape)                             ]
            return region_sites
        

        #filter the transmitter
        #check if the number of transmitter > transmitter_size if not recurse


        