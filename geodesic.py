# Python 3 program to calculate Distance Between Two Points on Earth
from math import radians, cos, sin, asin, acos, sqrt, atan2, atan, pi
import numpy as np

def distance(lat1, lon1, lat2, lon2):
	
	"""calculate the distance between point 1(lat1, lon1) and point 2(lat2, lon2)
     
    args:

    returns:
        float:distance between point 1 and point 2
	"""
	# Haversine formula
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	#c is the angular distance in radians, and a is the square of half the chord length between the points
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

	c = 2 * asin(sqrt(a))
	
	# Radius of earth in kilometers. Use 3956 for miles
	r = 6371
	
	# calculate the result
	return(c * r)

def bearing(lat1, lon1, lat2, lon2):
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
    d=2*asin(sqrt((sin((lat1-lat2)/2))**2 +  cos(lat1)*cos(lat2)*(sin((lon1-lon2)/2))**2))

    #calculate the bearing based on position
    if sin(lon2-lon1)>0:      
        tc1=acos((sin(lat2)-sin(lat1)*cos(d))/(sin(d)*cos(lat1)))    
    else:
        tc1=2*pi-acos((sin(lat2)-sin(lat1)*cos(d))/(sin(d)*cos(lat1)))    

    #convert the radian angle to degree
    tc1 = tc1*180/pi
    return tc1

def intersection(lat1, lon1, lat2, lon2, crs13, crs23):
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
    dst12 = 2*asin(sqrt((sin((lat1-lat2)/2))**2 + cos(lat1)*cos(lat2)*sin((lon1-lon2)/2)**2))
    #calculating bearing from point 1 to 2 csr12 and from point 2 to 1 crs21
    if sin(lon2-lon1) > 0:
         crs12=acos((sin(lat2)-sin(lat1)*cos(dst12))/(sin(dst12)*cos(lat1)))
         crs21=2.*pi-acos((sin(lat1)-sin(lat2)*cos(dst12))/(sin(dst12)*cos(lat2)))
         print(f'crs12 = {crs12} angle {crs12*180/pi} and crs21={crs21} and angle {crs21*180/pi}')
    else:
         crs12=2.*pi-acos((sin(lat2)-sin(lat1)*cos(dst12))/(sin(dst12)*cos(lat1)))
         crs21=acos((sin(lat1)-sin(lat2)*cos(dst12))/(sin(dst12)*cos(lat2)))
         print(f'crs12 = {crs12} and crs21={crs21}')

    #calculate angles in the triangle(P1, P2, P3), ang1=(P2,P1,P3), ang2=(P1,P2,P3), 
    ang1 = (crs13 - crs12 + pi)%(2*pi) - pi
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
        lat3=asin(sin(lat1)*cos(dst13)+cos(lat1)*sin(dst13)*cos(crs13))
        dlon=atan2(sin(crs13)*sin(dst13)*cos(lat1),cos(dst13)-sin(lat1)*sin(lat3))
        lon3=(lon1+dlon+pi)%(2*pi) - pi
        dst23 = distance(lat2, lon2, lat3, lon3)
        # 6371 Radius of earth in kilometers to convert angular unit to distance unit. Use 3956 for miles, 
        dst13 = dst13*6371
        dst12 = dst12*6371
        lat3 = (lat3*180/pi) # in decimal degrees,
        lon3 = (lon3*180/pi) # in decimal degrees,
        return dst12, dst13, dst23, lat3, lon3
 

#test data
#lat lon in radians
lat1=radians(-1.2814722) #0.592539 -1.2814722 36.8209444
lon1=radians(36.8209444) #2.066470
#lat lon in radians
lat2=radians(-1.280823) #0.709186 -1.280823 36.822151
lon2=radians(36.822151) #1.287762
#confirm bearing and distance
print(distance(lat1, lon1, lat2, lon2))
try:
    print(bearing(lat1, lon1, lat2, lon2))
except ZeroDivisionError as error:
     print("same location")

#test data
#lat lon in radians
lat2=radians(-1.2814722) #0.592539 -1.2814722 36.8209444
lon2=radians(36.8209444) #2.066470
#lat lon in radians
lat1=radians(-1.280823) #0.709186 -1.280823 36.822151
lon1=radians(36.822151) #1.287762
#azimuths to the intersection point
azim13 = radians(51)
azim23 =radians(300)

#intersection example
#check the intersection function
dst12, dst13, dst23, lat3, lon3 = intersection(lat1, lon1, lat2, lon2, azim13, azim23)
print(dst12, dst13, dst23, lat3, lon3)
print('confirm distance dst23', distance(lat2, lon2, radians(lat3), radians(lon3)))

test_azimuth = np.arange(0, 360, 30)
ambigous_cases = 0
infinity_cases = 0
for a in test_azimuth:    
    print(f'for azimuth {a}')
    print(f'-----------------------')
    a= radians(a)
    try:
        dst12, dst13, dst23, lat3, lon3 = intersection(lat1, lon1, lat2, lon2, azim13, a)
        print(dst12, dst13, dst23, lat3, lon3)
    except ValueError as e:
         print("message from function:", str(e))
         ambigous_cases +=1
         infinity_cases +=1
    
print(f'total number = {len(test_azimuth)}, ambiguous case:{ambigous_cases}, infinity cases:{infinity_cases}')
     