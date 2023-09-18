import pandas as pd

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
    def __init__(self, lat, lon, sites:pd.DataFrame,):
        self.lat = lat
        self.lon = lon
        self.sites = sites
        self.dp = 2
        self.offset = 0.01
        self.site_size = 2351

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

    def source_neighbors(self,):
        #determine the 1km square around the site
        lat = round(self.lat, self.dp)
        lon = round(self.lon, self.dp)
        neigh_sites = self.sites.loc[(self.sites["twodp_lat"]==lat) & (self.sites["twodp_lon"]==lon), :]
        unique_sites = neigh_sites.drop_duplicates(subset ="site").shape 

        print("sites:transmitter", self.sites.shape)
        print("sites:sites", self.sites.drop_duplicates(subset="site").shape)
        print("region:transmitter", neigh_sites.shape)
        print("region:sites", neigh_sites.drop_duplicates(subset="site").shape) 
          
        #check if no of site is >= 30, if not expand the search area
        if unique_sites[0] >= self.site_size:
            return neigh_sites        
        #if no of sites in area is less expand area to 3.3km sqaurearound the site       
        grids = self.expanded_region(self.dp, self.offset)
        print(grids)
        neigh_sites = self.sites.loc[((self.sites['twodp_lat']==grids[0][0])&(self.sites['twodp_lon']==grids[0][1])) | 
                                          ((self.sites['twodp_lat']==grids[1][0])&(self.sites['twodp_lon']==grids[1][1])) |  
                                          ((self.sites['twodp_lat']==grids[2][0])&(self.sites['twodp_lon']==grids[2][1])) | 
                                          ((self.sites['twodp_lat']==grids[3][0])&(self.sites['twodp_lon']==grids[3][1])) | 
                                          ((self.sites['twodp_lat']==grids[4][0])&(self.sites['twodp_lon']==grids[4][1])) |
                                          ((self.sites['twodp_lat']==grids[5][0])&(self.sites['twodp_lon']==grids[5][1])) |
                                          ((self.sites['twodp_lat']==grids[6][0])&(self.sites['twodp_lon']==grids[6][1])) |  
                                          ((self.sites['twodp_lat']==grids[7][0])&(self.sites['twodp_lon']==grids[7][1])) | 
                                          ((self.sites['twodp_lat']==grids[8][0])&(self.sites['twodp_lon']==grids[8][1])), : 
                                         ]
        #check if number of site >= 30
        unique_sites = neigh_sites.drop_duplicates(subset="site").shape
        print("3.3km square", neigh_sites.shape)
        print("3.3km square", unique_sites)
        if unique_sites[0] >= self.site_size:
            print("expanded unique", neigh_sites.drop_duplicates(subset="site").shape)
            return neigh_sites
        
        #if no of site is less expand the area to 11km square around source
        lat = round(self.lat, 1)
        lon = round(self.lon, 1)
        #filter transmitter on this lat lon combination
        neigh_sites = self.sites.loc[(self.sites["onedp_lat"]==lat) & (self.sites["onedp_lon"]==lon), :]
        unique_sites = neigh_sites.drop_duplicates(subset="site").shape
        if unique_sites[0] >= self.site_size:
            print("returning from 11km")
            print(neigh_sites.shape)
            print(unique_sites)
            return neigh_sites
        
        #if no site is less expand the area to 33km square around the surce
        grids = self.expanded_region(1, 0.1)
        print(grids)
        neigh_sites = self.sites.loc[((self.sites['onedp_lat']==grids[0][0])&(self.sites['onedp_lon']==grids[0][1])) | 
                                          ((self.sites['onedp_lat']==grids[1][0])&(self.sites['onedp_lon']==grids[1][1])) |  
                                          ((self.sites['onedp_lat']==grids[2][0])&(self.sites['onedp_lon']==grids[2][1])) | 
                                          ((self.sites['onedp_lat']==grids[3][0])&(self.sites['onedp_lon']==grids[3][1])) | 
                                          ((self.sites['onedp_lat']==grids[4][0])&(self.sites['onedp_lon']==grids[4][1])) |
                                          ((self.sites['onedp_lat']==grids[5][0])&(self.sites['onedp_lon']==grids[5][1])) |
                                          ((self.sites['onedp_lat']==grids[6][0])&(self.sites['onedp_lon']==grids[6][1])) |  
                                          ((self.sites['onedp_lat']==grids[7][0])&(self.sites['onedp_lon']==grids[7][1])) | 
                                          ((self.sites['onedp_lat']==grids[8][0])&(self.sites['onedp_lon']==grids[8][1])), : 
                                         ]     
         
        unique_sites = neigh_sites.drop_duplicates(subset="site").shape
        print(unique_sites)
        #33km square around the site is largest area to be considered
        return neigh_sites

        
            
        

        