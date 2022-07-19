from hashlib import new
from Render import *

rend = None

def glInit():
    pass

def glCreateWindow(width, height):
    global rend
    adjusted = width

    if width % 4 != 0:
        adjusted = width + (4 - (width % 4))
    rend = Render(adjusted, height)
    
def glViewPort(x, y, width, height):
    global rend

    if width > rend.width and height > rend.height:
        print("los dos son mas largos")
        newwidth = rend.width - 1
        newheight = rend.height - 1 
        rend.viewport = {"x": x, "y": y, "width": newwidth, "height": newheight}
    elif width > rend.width:
        print("width es mas largo")
        newwidth = rend.width - 1 
        rend.viewport = {"x": x, "y": y, "width": newwidth, "height": height}
    elif height > rend.height:
        print("height es mas largo")
        newheight = rend.height - 1
        rend.viewport = {"x": x, "y": y, "width": width, "height": newheight}
    else:
        print("fresco")
        rend.viewport = {"x": x, "y": y, "width": width, "height": height}


def glClear():
    global rend
    rend.clear()

def glClearColor(r, g, b):
    global rend
    rend.setClearer(r, g , b)
    
def glVertex(x, y):
    global rend

    ini_x = (x + 1)
    ini_y = (y + 1)
    prop_x= (ini_x  * rend.viewport["width"])/2
    prop_y = (ini_y * rend.viewport["height"])/2
    point_x = int(prop_x )
    point_y = int(prop_y )

    rend.point(point_x, point_y)

     
def glColor(r, g, b):
    rend.setColor(r, g, b)
    
def glFinish():
    global rend
    rend.write("a.bmp")