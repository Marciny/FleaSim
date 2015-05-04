import math, random

def vector_to_angle (evpos, pos):
    vector = (evpos[0] - pos[0], evpos[1] - pos[1])
    
    if vector[0] == 0 :
        vector = (vector[0] + 0.000001, vector[1])    
    if vector[1] == 0 :
        vector = (vector[0], vector[1] + 0.000001)

    if vector[0] < 0 and vector[1] < 0:
        angle = math.degrees( math.atan( vector[0]/ vector[1] ) )
    elif vector[0] < 0 and vector[1] > 0:
        angle = math.degrees( math.atan( vector[0]/ vector[1] ) ) + 180
    elif vector[0] > 0 and vector[1] > 0:
        angle = math.degrees( math.atan( vector[0]/ vector[1] ) ) + 180
    elif vector[0] > 0 and vector[1] < 0:
        angle = math.degrees( math.atan( vector[0]/ vector[1] ) ) + 360
        
    return vector, angle

def vector_to_dist(vector):
    dist = math.sqrt(math.pow(vector[0], 2) + math.pow(vector[1], 2))
    return dist

def angle_dist_to_vector(angle, distance):
    x = -math.sin(math.radians(angle)) * distance
    y = math.cos(math.radians(angle)) * distance
    vector = (x,y)
    return vector

def angle_mirror_y (angle):
    angle = 360 - angle
    return angle

def angle_mirror_x (angle):
    if angle <= 180:
        angle = 180 - angle
    else :
        angle = 540 - angle
    return angle

def minus_angle_convert(angle):
    if angle < 0:
        angle += 360
        angle = minus_angle_convert(angle)
    return angle

def linterp(vx, vy, x):
    y=x*(vy[1]-vy[0])/(vx[1]-vx[0])
    return y

def vecterp(v, x):
    y=x*v[1]/v[0]
    return y

def randpoint(borders_x, borders_y, step):
    point = (random.randrange(borders_x[0], borders_x[1], step), random.randrange(borders_y[0], borders_y[1], step))
    return point



##                0/360
##                |
##                |
##                |
##                |
##    90 ------------------ 270
##                |
##                |
##                |
##                |
##                180




