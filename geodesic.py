# Python 3 program to calculate Distance Between Two Points on Earth
from math import radians, cos, sin, asin, acos, sqrt, atan2, atan, pi, degrees
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
   
    def __init__(self, lat, lon, azimuth, coverage) -> None:
        self.lat = lat
        self.lon = lon 
        self.coverage = coverage
        self.azim = azimuth
        self.half_bw = 30
        self.earth_circum = 40035 
        self.fdelta = 5
        
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
        """calculate the bearing based on position
        condition 1 check for points along a single longitude line(lat change only, bearing 
        can either be zero or 180)
        condition 2 check a diff lat,lon point east of source and condition 3 west of source
        """
        if self.lat > lat and self.lon == lon:
            tc1 = pi
        elif self.lat < lat and self.lon == lon:
            tc1 = 0
        elif sin(lon-self.lon)>0:  
            tc1=acos((sin(lat)-sin(self.lat)*cos(d))/(sin(d)*cos(self.lat)))    
        else:
            print((sin(lat)-sin(self.lat)*cos(d))/(sin(d)*cos(self.lat)))
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
        """special case of point along a longitude. self.lon==lon result to
        """        
        if self.lon == lon:
            if self.lat > lat: 
                crs12 = pi
                crs21 = 0               
                #print('longitude: crs12:', degrees(crs12), 'crs21', degrees(crs21))
                if degrees(crs13) == degrees(crs12) or (degrees(crs23) == degrees(crs21)):
                    #print("returning")
                    print("Above:distance for edge facing source")
                    return dst12*6371, lat, lon
            elif self.lat < lat:
                crs12 = 0
                crs21 = pi
                #if degrees(crs13) == 0 or (degrees(crs13) == 180 and degrees(crs23) == 180):
                if degrees(crs13) == degrees(crs12) or (degrees(crs23) == degrees(crs21)):
                    #print('case 2:longitude: crs12:', degrees(crs12), 'crs21', degrees(crs21))
                    #print("returning")
                    print("Below:distance for edge facing source")
                    return dst12*6371, lat, lon
        #other scenario
        elif sin(lon-self.lon) > 0:
            crs12=acos((sin(lat)-sin(self.lat)*cos(dst12))/(sin(dst12)*cos(self.lat)))
            crs21=2.*pi-acos((sin(self.lat)-sin(lat)*cos(dst12))/(sin(dst12)*cos(lat)))
            #print('crs12:', degrees(crs12), 'crs21', degrees(crs21))
        else:
            crs12=2.*pi-acos((sin(lat)-sin(self.lat)*cos(dst12))/(sin(dst12)*cos(self.lat)))
            crs21=acos((sin(self.lat)-sin(lat)*cos(dst12))/(sin(dst12)*cos(lat)))
            #print('case2: crs12', degrees(crs12), 'crs21', degrees(crs21))
        #calculate angles in the triangle(P1, P2, P3), ang1=(P2,P1,P3), ang2=(P1,P2,P3), 
        ang1 = (crs13 - crs12 + pi)%(2*pi) - pi
        ang2 =  (crs21-crs23 + pi)%(2*pi) - pi
        #print("angle1 and angle2", degrees(ang1), degrees(ang2))


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
            # print('ang3:', degrees(ang3)) 
            # print("dst12", dst12*6371)
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


    def macro_intersection(self, lat2, lon2, crs23):
        #convert angular to degrees to calculate the beamwidth edges
        crs13 = degrees(self.azim)
        crs23 = degrees(crs23)
        print("--------------")
        print("crs13", crs13, "crs23:", crs23)
        #check if same point, same point raise a zerodivisionerror
        print("distance to target", self.distance(lat2, lon2))
        try:
            crs12 = self.bearing(lat2, lon2) #bearing from source to target
            crs21 = (crs12 + 180) % 360
            print("bearings:crs12", crs12, 'crs21', crs21)
        except ZeroDivisionError as e:
            return "source point"
        
        #todo directly facing sector, intersection distance to be half dst12
        diff_crs12_crs13 = abs(((crs12+180) % 360) - ((crs13+180) % 360) ) #diff between bearing of source-target and source azimuth
        diff_crs12_crs23= abs(((crs12+180) % 360) - ((crs23+180) % 360) ) #diff between bearing of source-target and  target azimuth        
        diff_crs21_crs13 = abs(((crs21+180) % 360) - ((crs13+180) % 360) ) #diff between bearing of target-source and source azimuth
        diff_crs21_crs23= abs(((crs21+180) % 360) - ((crs23+180) % 360) ) #diff between bearing of target-source and  target azimuth        
     
        '''determine if source and target are facing in the same direction on a straight line;
        that is same azimuth and bearing equal azimuth. if that the case, good neighbor
        if dst12 is small'''
        if  diff_crs12_crs13 < self.fdelta and diff_crs12_crs23 < self.fdelta:
            dst12 = self.distance(lat2, lon2)
            print("source behind target")
            return dst12
        elif diff_crs21_crs13 < self.fdelta and diff_crs21_crs23 < self.fdelta:
            print("distance target behind source")
            dst12 = self.distance(lat2, lon2)
            return dst12
        
        #calculate the beamwidth edges for source and target cell 
        pos_source_crs13 = radians((crs13 + self.half_bw) % 360)
        neg_source_crs13 = radians((crs13 - self.half_bw + 360) % 360)
        pos_target_crs23 = radians((crs23 + self.half_bw) % 360)
        neg_target_crs23 = radians((crs23 - self.half_bw + 360) % 360)
        print("the edges", degrees(pos_source_crs13), degrees(neg_source_crs13), degrees(pos_target_crs23), degrees(neg_target_crs23))

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
    
    def micro_intersection(self, lat2, lon2, crs23, type="macro"):
        #convert azimuth from radians to degrees
        source_azim = degrees(self.azim)
        target_azim = degrees(crs23)
        #determine the bearing from source macro to target IBS
        if type == "macro":
            try:
                crs12 = self.bearing(lat2, lon2)
            except ZeroDivisionError as e:
                return "source point"
            #difference between bearing and azimuth of macro
            diff_crs12_source_azim = abs(((crs12+180) % 360) - ((source_azim+180) % 360) )
        elif type == "micro":
            #bearing from IBS to target macro site
            try:
                crs12 = self.bearing(lat2, lon2)
            except ZeroDivisionError as e:
                return "source point"          
            #get the bearing from macro to IBS
            crs12 = (crs12 + 180) % 360
            #difference between bearing and azimuth of macro
            diff_crs12_source_azim = abs(((crs12+180) % 360) - ((target_azim+180) % 360) )
        print('diff is', diff_crs12_source_azim)
        """an IBS and a macro coverage intersect if the bearing from source to IBS is within
        the macro sector edges, that is the  diff_crs12_source_azim is less than the half_BW.
        return, how well within the sector coverage. a diff of zero, macro directly facing IBS
        and a diff of 30, IBS is on the edge of the sector coverage. >30, IBS is outside the
        the sector coverage"""
        if diff_crs12_source_azim <= self.half_bw:
            #determine directness of macro to IBS
            directness = (self.half_bw-diff_crs12_source_azim)/self.half_bw
            if directness == 0:
                directness = directness + 0.1            
            return directness
        else:
            directness = 0
            return directness

    def source_neighbors(self, neighbors:pd.DataFrame):
        """a function that calculate the neighberhood of target site to the source site.
        macro to macro, determine the closest intersection of each source and target sector and
        dst12 between source and target.
        macro to ibs, determine the macro sector covering the IBS and dst12 between macro 
        to the IBS and this apply to IBS to macro
        IBS to IBS consider the dst12 between IBS to IBS

        Args:
            source_site(Geodesic): a object of Geodesic class with function for dst, inters, bearing
            neighbors(pd.DataFrame): the site neighboring the source site
            coverage(str): the type of coverage for the site, IBS, MACRO
            s_azim(float): the source site azimuth

        Returns:
            pd.DataFrame: the source site with neighbors with intersection and dst12 between
        

        """
    
        """determine if source site is macro or ibs and iterate over the neigbors site. apply
        method for determining intersection depending on type of the target site
        """
        if self.coverage == "macro":
            coverage_intersect = []
            distance12 = []
            for row in neighbors.itertuples(index=False):
                t_lat = row.radian_lat
                t_lon = row.radian_lon
                t_azim = row.radian_azim
                #determine intersite distance between source and target
                dst12 = self.distance(t_lat, t_lon)
                distance12.append(dst12)
                if row.coverage == "macro":
                    intersection = self.macro_intersection(t_lat, t_lon, t_azim)
                    coverage_intersect.append(intersection)
                elif row.coverage == "micro":
                    intersection = self.micro_intersection(t_lat, t_lon, t_azim, "macro")
                    coverage_intersect.append(intersection)
            #add column intersection and intersite distance
            neighbors["intersection"] = coverage_intersect
            neighbors["dst12"] = distance12

        elif self.coverage == "micro":
            coverage_intersect = []
            distance12 = []
            for row in neighbors.itertuples(index=False):
                #get the target lat, lon, and azimuth
                t_lat = row.radian_lat
                t_lon = row.radian_lon
                t_azim = row.radian_azim
                #determine intersite distance between source and target
                dst12 = self.distance(t_lat, t_lon)
                distance12.append(dst12)
                #if target is macro from micro determine the directness from micro to macro
                if row.coverage == "macro":
                    intersection  = self.micro_intersection(t_lat, t_lon,t_azim, "micro")
                    coverage_intersect.append(intersection)
                #if target is IBS, determine the distance between two IBS
                elif row.coverage == "micro":
                    intersection = self.distance(t_lat, t_lon)
                    coverage_intersect.append(intersection)
            #add column intersection and intersite distance
            neighbors["intersection"] = coverage_intersect
            neighbors["dst12"] = distance12
           
        return neighbors
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
     