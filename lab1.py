from gl import *

def draw(poligono):
    temp = ""
    inicial = ""
    for element in poligono:
        if  poligono.index(element) == 0:
            temp = element
            inicial = element
        else:
            rawLine(element[0], element[1], temp[0], temp[1])

            if poligono.index(element) == len(poligono)-1:
                rawLine(inicial[0], inicial[1], element[0], element[1])
        temp = element

def is_point_in_path(x: int, y: int, poly) -> bool:
    num = len(poly)
    j = num - 1
    c = False
    for i in range(num):
        if (x == poly[i][0]) and (y == poly[i][1]):
            # point is a corner
            return True
        if ((poly[i][1] > y) != (poly[j][1] > y)):
            slope = (x-poly[i][0])*(poly[j][1]-poly[i][1])-(poly[j][0]-poly[i][0])*(y-poly[i][1])
            if slope == 0:
                # point is on boundary
                return True
            if (slope < 0) != (poly[j][1] < poly[i][1]):
                c = not c
        j = i
    return c

def paint(poligono):
    width = getX()
    height = getY()
    for i in range(height):
        for j in range(width):
            if is_point_in_path(j, i, poligono):
                rawPoint(j, i)


def getmax(poligono, index):
    if index == 0:
        MaxX = max([x for x, y in poligono])
        return MaxX
    else:
        MaxY = max([y for x, y in poligono])
        return MaxY

def getmin(poligono, index):
    if index == 0:
        MinX = min([x for x, y in poligono])
        return MinX
    else:
        MinY = min([y for x, y in poligono])
        return MinY
    

p1 = [(165, 380), (185, 360), (180, 330), (207, 345), (233, 330), (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)]
p2 = [(321, 335), (288, 286), (339, 251), (374, 302)]
p3 = [(377, 249), (411, 197), (436, 249)]
p4 = [(413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37), (660, 52),
(750, 145), (761, 179), (672, 192), (659, 214), (615, 214), (632, 230), (580, 230),
(597, 215), (552, 214), (517, 144), (466, 180)]
p5 = [(682, 175), (708, 120), (735, 148), (739, 170)]
glCreateWindow(800, 800)
glClearColor(1, 1, 1)
glClear()
glColor(0, 0, 1)
glViewPort(0, 0, 800, 800)

draw(p1)
draw(p2)
draw(p3)
draw(p4)
draw(p5)

maxx = getmax(p1, 0)
maxy = getmax(p1, 1)
minx = getmin(p1, 0)
miny = getmin(p1, 1)

centerx = int(((maxx - minx)/2) + minx)
centery = int(((maxy - miny)/2) + miny)

paint(p1)
paint(p2)
paint(p3)
paint(p4)
glColor(1, 1, 1)
paint(p5)



glFinish("lab1.bmp")