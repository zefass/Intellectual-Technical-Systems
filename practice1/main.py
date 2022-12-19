import numpy as np
from math import atan, pi

lin_vel = float(input("Введите линейную скорость(м/сек):"))
angle_vel = float(input("Введите скорость поворота(град/сек):"))

def readData(filenm):
    try:
        f = open(filenm, 'r')
    except OSError:
        print('Could not open/read file:', filenm)
    with f:
        points = np.loadtxt(filenm, dtype=float)
        return points

def dist(x, y, xstart, ystart):
    distance = (xstart - x)**2 + (ystart - y)**2
    return distance**(0.5)

def calctime(distance:float):
    return distance/lin_vel

def calcangle(x, y, xstart, ystart) -> float:
    if x*xstart + y*ystart == 0:
        gradangle = 0
    else:
        angle = abs(atan(y/x)-atan(ystart/xstart))
        gradangle = angle * 180 / pi
    return gradangle
def calcrotatetime(angle:float):
    return angle / angle_vel

def message():
    msg = {"cmd": "", "val": ""}
    points = readData("data.txt")
    print(points)
    x1, y1 = points[0][0], points[0][1]

    for index, value in enumerate(points[1:]):
        xnew, ynew = value[0], value[1]
        distance = dist(x=xnew, y=ynew, xstart=x1, ystart=y1)
        distance_time = calctime(distance)
        angle = calcangle(x=xnew, y=ynew, xstart=x1, ystart=y1)
        rotate_time = calcrotatetime(angle)
        x1+=xnew
        y1+=ynew
        if angle == 0:
            msg["cmd"] = "forward"
            msg["val"] = distance_time
            print(msg)
        elif 0<angle<179:
            msg["cmd"] = "left"
            msg["val"] = rotate_time
            print(msg)
        elif 181<angle<359:
            msg["cmd"] = "right"
            msg["val"] = rotate_time
            print(msg)
    print('{\'cmd\': \'stop\'}')
message()
