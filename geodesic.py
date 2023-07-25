# Python 3 program to calculate Distance Between Two Points on Earth
from math import radians, cos, sin, asin, acos, sqrt, atan2, atan, pi
import numpy as np
import pandas as pd
class Geodesic:
    """ a class for calculating geodesic measurements, distance between two points on the earth 
    surface, bearing between points, intersection between two lines from two points

    ...

    Attributes
    ----------
    lat : float
        The latitude for source site
    lon : float
        the longitude for the source site

    Methods
    -------
    distance(lat1, lon1, lat2, lon2): calculate distance between two point
    bearing(lat1, lon1, lat2, lon2): calculate bearing between two point
    intersection(lat1, lon1, lat2, lon2, crs13, crs23): calculate intersection point of two lines
    """
   
    def __init__(self, lat, lon) -> None:
        self.lat = lat
        self.lon = lon 
        self.half_bw = 30 
        self.earth_circum = 40035      
        
    def distance(self,lat, lon):        
        """calculate the distance between point 1(lat1, lon1) and point 2(lat2, lon2)
        
        args:

        returns:
            float:distance between point 1 and point 2
        """
        # Haversine formula
        dlon = lon - self.lon
        dlat = lat - self.lat
        #c is the angular distance in radians, and a is the square of half the chord length between the points
        a = sin(dlat / 2)**2 + cos(self.lat) * cos(lat) * sin(dlon / 2)**2
        angular_distance = 2 * asin(sqrt(a)) 
        #distance in kms by multiplying with earth radius
        unit_distance = angular_distance * 6371     

        return unit_distance

    def bearing(self, lat, lon):
        """We obtain the initial course, tc1, (at point 1) from point 1 to point 2 by the 
        following. The formula fails if the initial point is a pole. We can special case this 
        with:
            if (cos(lat1) < EPS)   // EPS a small number ~ machine precision
                if (lat1 > 0)
                    tc1= pi        //  starting from N pole
                else
                    tc1= 2*pi         //  starting from S pole

        input: Point A coord(lat1, lon1) and point B(lat2, lon2)
        output: bearing degrees
        """

        #calculate distance between point 1 and point 2
        d=2*asin(sqrt((sin((self.lat-lat)/2))**2 +  cos(self.lat)*cos(lat)*(sin((self.lon-lon)/2))**2))

        #calculate the bearing based on position
        if sin(lon-self.lon)>0:      
            tc1=acos((sin(lat)-sin(self.lat)*cos(d))/(sin(d)*cos(self.lat)))    
        else:
            tc1=2*pi-acos((sin(lat)-sin(self.lat)*cos(d))/(sin(d)*cos(self.lat)))    

        #convert the radian angle to degree
        tc1 = tc1*180/pi
        return tc1

    def intersection(self, lat, lon, crs13, crs23):
        '''computing the intersection(point 3) of a line at azimuth 1 from point 1 and a line at 
        azimuth 2 from point 2

        Args:
            lat1(float): latitude of point 1
            lon1(float): longitude of point 1
            lat2(float): latitude of point 2
            lon2(float): longitude of point 2
            crs13(float): bearing from 1 to point 3
            crs213float): bearing from 2 to point 3

        Returns:
            float: intersection distance from point 1 to point 3    
        '''
        #distance between point 1 and point 2
        dst12 = 2*asin(sqrt((sin((self.lat-lat)/2))**2 + cos(self.lat)*cos(lat)*sin((self.lon-lon)/2)**2))
        #calculating bearing from point 1 to 2 csr12 and from point 2 to 1 crs21
        if sin(lon-self.lon) > 0:
            crs12=acos((sin(lat)-sin(self.lat)*cos(dst12))/(sin(dst12)*cos(self.lat)))
            crs21=2.*pi-acos((sin(self.lat)-sin(lat)*cos(dst12))/(sin(dst12)*cos(lat)))
        else:
            crs12=2.*pi-acos((sin(lat)-sin(self.lat)*cos(dst12))/(sin(dst12)*cos(self.lat)))
            crs21=acos((sin(self.lat)-sin(lat)*cos(dst12))/(sin(dst12)*cos(lat)))

        #calculate angles in the triangle(P1, P2, P3), ang1=(P2,P1,P3), ang2=(P1,P2,P3), 
        ang1 = (crs13 - crs12 + pi)%(2*pi) - pi
        ang2 =  (crs21-crs23 + pi)%(2*pi) - pi

        #check for parallel lines and ambiguous condition(i.e antipodal point)
        if (sin(ang1)==0 and sin(ang2)==0):

            # dst13="infinity"; dst23="infinity"; lat3="infinity"; lon3="infinity"
            # return dst12, dst13, dst23, lat3, lon3
            raise ValueError("infinity")
        elif sin(ang1)*sin(ang2)<0:

            # dst13="ambiguous"; dst23="ambiguous"; lat3="ambiguous"; lon3="ambiguous"
            # return dst12, dst13, dst23, lat3, lon3
            raise ValueError("ambiguous intersection")
        else:
            ang1=abs(ang1)
            ang2=abs(ang2)
            ang3=acos(-cos(ang1)*cos(ang2)+sin(ang1)*sin(ang2)*cos(dst12)) 
            dst13=atan2(sin(dst12)*sin(ang1)*sin(ang2),cos(ang2)+cos(ang1)*cos(ang3))
            lat3=asin(sin(self.lat)*cos(dst13)+cos(self.lat)*sin(dst13)*cos(crs13))
            dlon=atan2(sin(crs13)*sin(dst13)*cos(self.lat),cos(dst13)-sin(self.lat)*sin(lat3))
            lon3=(self.lon+dlon+pi)%(2*pi) - pi
            
            # 6371 Radius of earth in kilometers to convert angular unit to distance unit. Use 3956 for miles, 
            dst13 = dst13*6371
            dst12 = dst12*6371
            lat3 = (lat3*180/pi) # in decimal degrees,
            lon3 = (lon3*180/pi) # in decimal degrees,
            return dst13, lat3, lon3


    def best_intersection(self, lat2, lon2, crs13, crs23):
        #calculate the beamwidth edges for source and target cell 
        pos_source_crs13 = radians((crs13 + self.half_bw) % 360)
        neg_source_crs13 = radians((crs13 - self.half_bw + 360) % 360)
        pos_target_crs23 = radians((crs23 + self.half_bw) % 360)
        neg_target_crs23 = radians((crs23 - self.half_bw + 360) % 360)

        all_intersection = pd.Series()
        #intersection 1
        try:
            pos_source_pos_target_x = self.intersection(lat2, lon2, pos_source_crs13, pos_target_crs23)
        except ValueError as e:
            all_intersection[0] = self.earth_circum
        else:
            all_intersection[0] = pos_source_pos_target_x[0]
        #intersection 2
        try:
            pos_source_neg_target_x = self.intersection(lat2, lon2, pos_source_crs13, neg_target_crs23)
        except ValueError as e:
            all_intersection[1] = self.earth_circum
        else:
            all_intersection[1] = pos_source_neg_target_x[0]
        #intersection 3
        try:
            neg_source_pos_target_x = self.intersection(lat2, lon2, neg_source_crs13, pos_target_crs23)
        except ValueError as e:
            all_intersection[2] = self.earth_circum
        else:
            all_intersection[2]= neg_source_pos_target_x[0]  
        #intersection 4
        try:
            neg_source_neg_target_x = self.intersection(lat2, lon2, neg_source_crs13, neg_target_crs23)
        except ValueError as e:
            all_intersection[3] = self.earth_circum
        else:
            all_intersection[3] = neg_source_neg_target_x[0]

        #return the closest neighbor
        print(all_intersection)
        return all_intersection.min()
  
# #test data
# #lat lon in radians
# lat1=radians(-1.2814722) #0.592539 -1.2814722 36.8209444
# lon1=radians(36.8209444) #2.066470
# #lat lon in radians
# lat2=radians(-1.280823) #0.709186 -1.280823 36.822151
# lon2=radians(36.822151) #1.287762
# #confirm bearing and distance
# source = Geodesic(lat1, lon1)
# crs13 = radians(50)
# crs23 = radians(270)
# print("distance to point 2", source.distance(lat2, lon2))
# try:
#     print(source.bearing(lat2, lon2))
#     print(source.intersection(lat2, lon2, crs13, crs23))
# except ZeroDivisionError as error:
#     print("same location")


# test_azimuth = np.arange(0, 360, 30)
# ambigous_cases = 0
# infinity_cases = 0
# for a in test_azimuth:    
#     print(f'for azimuth {a}')
#     print(f'-----------------------')
#     a= radians(a)
#     try:
#         dst13, lat3, lon3 = source.intersection(lat2, lon2, crs13, a)
#         print(dst13, lat3, lon3)
#     except ValueError as e:
#          print("message from function:", str(e))
#          ambigous_cases +=1
     
# print(f'total number = {len(test_azimuth)}, ambiguous case:{ambigous_cases}, infinity cases:{infinity_cases}')
     