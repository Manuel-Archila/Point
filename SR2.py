from gl import *

glCreateWindow(400, 400)
glClearColor(1, 1, 1)
glClear()
glColor(0, 0, 1)
glViewPort(0, 0, 400, 400)

glColor(0.7, 0.0, 0.0)
x1 = -0.5
x2 = 0
y1 = -0.25
y2 = -0.5
glLine(x1, y1, x2, y2)
for i in range(500):
    y1 += 0.0005
    y2 += 0.0005
    glLine(x1, y1, x2, y2)

glColor(0.9, 0, 0.0)


x1 = -0.5
x2 = -0.28
y1 = 0
y2 = 0.44
glLine(x1, y1, x2, y2)
for i in range(1000):
    x1+=0.0005
    x2+=0.0005
    y1 -= 0.00025
    y2 -= 0.00025
    glLine(x1, y1, x2, y2)

glColor(0.8, 0, 0)
x1 = 0
y1 = -0.5
x2 = 0.5
y2 = -0.3
glLine(x1, y1, x2, y2)
for i in range(500):
    y1 += 0.0005
    y2 += 0.0005
    glLine(x1, y1, x2, y2)

y1 = -0.25
for i in range(460):
    y1 += 0.0005
    y2 += 0.0005
    x1 += 0.00027
    x2 -= 0.0006
    glLine(x1, y1, x2, y2)

glColor(0.7, 0, 0)
x1 = -0.1
y1 = 0.35
x2 = -0.1
y2 = 0.475
glLine(x1, y1, x2, y2)
for i in range(200):
    y1 -= 0.00025
    y2 -= 0.00025
    x1 += 0.0005
    x2 += 0.0005
    glLine(x1, y1, x2, y2)

glColor(0.8, 0, 0)
for i in range(200):
    x1 += 0.0005
    x2 += 0.0005
    y1 -= 0.00025
    y2 += 0.0001
    glLine(x1, y1, x2, y2)

glColor(0.9, 0, 0)
x1 = -0.1
y1 = 0.475
x2 = 0.02
y2 = 0.5
glLine(x1, y1, x2, y2)
for i in range(350):
    y1 -= 0.00015
    y2 -= 0.00015
    x1 += 0.00025
    x2 += 0.00025
    glLine(x1, y1, x2, y2)

glColor(0, 0, 0)
x1 = 0.23
y1 = -0.41
x2 = 0.33
y2 = -0.37
glLine(x1, y1, x2, y2)
for i in range(300):
    y1 += 0.0005
    y2 += 0.0005
    glLine(x1, y1, x2, y2)


glFinish("SR2.bmp")
