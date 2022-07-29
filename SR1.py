from gl import *

glCreateWindow(200, 200)
glClearColor(0.2, 0.3, 0.4)
glClear()
glColor(1, 0.5, 0.4)
glViewPort(0, 0, 300, 300)
glVertex(0, 0)
glFinish('SR1.bmp')
