# Python 3 program to calculate Distance Between Two Points on Earth
from math import radians, cos, sin, asin, acos, sqrt, atan2, atan, pi
import numpy as np

class geodesic:
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

    #earth radius constant in kms
    EARTH_RADIUS = 6371
    lead = 0
    def __init__(self, lat, lon, azimuth) -> None:
        self.lat = lat
        self.lon = lon
        self.azimuth = azimuth  
        
        
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
        #method 1
        # y = sin(lon2-lon1) * cos(lat2)
        # x = cos(lat1)*sin(lat2) - sin(lat1)*cos(lat2)*cos(lon2-lon1)
        # z = atan2(y,x)
        # brng = (z*180/pi+360) % (360) # in degrees, mod of 360

        #method2
        #calculate distance between point 1 and point 2
        d=2*asin(sqrt((sin((self.lat-lat)/2))**2 +  cos(self.lat)*cos(lat)*(sin((self.lon-lon)/2))**2))

        #calculate the bearing based on position
        if sin(lon-self.lon)>0:      
            tc1=acos((sin(lat2)-sin(self.lat)*cos(d))/(sin(d)*cos(self.lat)))    
        else:
            tc1=2*pi-acos((sin(lat)-sin(self.lat)*cos(d))/(sin(d)*cos(self.lat)))    

        #convert the radian angle to degree
        tc1 = tc1*180/pi
        return tc1

    def intersection(self, lat, lon, crs23):
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
            print(f'crs12 = {crs12} angle {crs12*180/pi} and crs21={crs21} and angle {crs21*180/pi}')
        else:
            crs12=2.*pi-acos((sin(lat)-sin(self.lat)*cos(dst12))/(sin(dst12)*cos(self.lat)))
            crs21=acos((sin(self.lat)-sin(lat)*cos(dst12))/(sin(dst12)*cos(lat)))
            print(f'crs12 = {crs12} and crs21={crs21}')

        #calculate angles in the triangle(P1, P2, P3), ang1=(P2,P1,P3), ang2=(P1,P2,P3), 
        ang1 = (self.azimuth - crs12 + pi)%(2*pi) - pi
        ang2 =  (crs21-crs23 + pi)%(2*pi) - pi
        print(f'ang1={ang1*180/pi} and ang2={ang2*180/pi}')

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
            lat3=asin(sin(self.lat)*cos(dst13)+cos(self.lat)*sin(dst13)*cos(self.azimuth))
            dlon=atan2(sin(self.azimuth)*sin(dst13)*cos(self.lat),cos(dst13)-sin(self.lat)*sin(lat3))
            lon3=(self.lon+dlon+pi)%(2*pi) - pi
            
            # 6371 Radius of earth in kilometers to convert angular unit to distance unit. Use 3956 for miles, 
            dst13 = dst13*6371
            dst12 = dst12*6371
            lat3 = (lat3*180/pi) # in decimal degrees,
            lon3 = (lon3*180/pi) # in decimal degrees,
            return dst12, dst13, lat3, lon3
    

#test data
#lat lon in radians
lat1=radians(-1.2814722) #0.592539 -1.2814722 36.8209444
lon1=radians(36.8209444) #2.066470
#lat lon in radians
lat2=radians(-1.280823) #0.709186 -1.280823 36.822151
lon2=radians(36.822151) #1.287762
#confirm bearing and distance
source = geodesic(lat1, lon1, radians(50) )
print("distance to point 2", source.distance(lat2, lon2))
try:
    print(source.bearing(lat2, lon2))
    print(source.intersection(lat2, lon2, radians(270)))
except ZeroDivisionError as error:
    print("same location")

# #test data
# #lat lon in radians
# lat2=radians(-1.2814722) #0.592539 -1.2814722 36.8209444
# lon2=radians(36.8209444) #2.066470
# #lat lon in radians
# lat1=radians(-1.280823) #0.709186 -1.280823 36.822151
# lon1=radians(36.822151) #1.287762
# #azimuths to the intersection point
# azim13 = radians(51)
# azim23 =radians(300)

# #intersection example
# #check the intersection function
# source = geodesic(lat1, lon1,azim13)
# dst12, dst13, dst23, lat3, lon3 = source.intersection(lat2, lon2, azim23)
# print(dst12, dst13, dst23, lat3, lon3)
# source2 = geodesic(lat2, lon2, azim23)
# print('confirm distance dst23', source2.distance(radians(lat3), radians(lon3), radians(240)))

test_azimuth = np.arange(0, 360, 30)
ambigous_cases = 0
infinity_cases = 0
for a in test_azimuth:    
    print(f'for azimuth {a}')
    print(f'-----------------------')
    a= radians(a)
    try:
        dst12, dst13, lat3, lon3 = source.intersection(lat2, lon2, a)
        print(dst12, dst13, lat3, lon3)
    except ValueError as e:
         print("message from function:", str(e))
         ambigous_cases +=1
         infinity_cases +=1
    
print(f'total number = {len(test_azimuth)}, ambiguous case:{ambigous_cases}, infinity cases:{infinity_cases}')
     