from math import *
import gl
gl.glCreateWindow(800, 450)
gl.glClear()
gl.glViewPort(0, 0, 800, 450)
#gl.assign_background('./fondin.bmp')
gl.glLookat((0, 0.5, 2), (0, 0, 0), (0, 1, 0))
gl.assign_texture('./Raptor.bmp')
gl.assign_normalmap('./RaptorN.bmp')
gl.glIntensity(-1)
gl.generate_model('Raptor.obj', (0.3, 0.3, 0.3), (0, 0, 0), (0, 0, 0))
gl.glFinish("pruebin.bmp")