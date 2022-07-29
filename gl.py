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
        #print("fresco")
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

     
def glColor(b, g, r):
    rend.setColor(b, g, r)
    
def glFinish(name):
    global rend
    rend.write(name)

def glLine(x1, y1, x2, y2):
    ini_x1 = (x1 + 1)
    ini_y1 = (y1 + 1)
    ini_x2 = (x2 + 1)
    ini_y2 = (y2 + 1)
    prop_x1= (ini_x1  * rend.viewport["width"])/2
    prop_y1 = (ini_y1 * rend.viewport["height"])/2
    prop_x2 = (ini_x2  * rend.viewport["width"])/2
    prop_y2 = (ini_y2 * rend.viewport["height"])/2

    rend.line(int(prop_x1), int(prop_y1), int(prop_x2), int(prop_y2))

def rawLine(x1, y1, x2, y2):
    global rend
    rend.line(x1, y1, x2, y2)

def rawPoint(x1, y1):
    global rend
    rend.point(x1, y1)

def getX():
    global rend
    return rend.width

def getY():
    global rend
    return rend.height

def generate(filename, scale_factor, translate_factor):
    global rend
    rend.modelGenerator(filename, scale_factor, translate_factor)
