import gl
gl.glCreateWindow(4100, 4100)

gl.glClear()
gl.glViewPort(0, 0, 1024, 1024)
gl.glShader()
gl.assign_texture('./Pokemon.bmp')
#Medium
#gl.glLookat((0, 0.5, 2), (0, 0, 0), (0, 1, 0))
#gl.generate_model('Ivysaur.obj', (0.7, 0.7, 0.7), (0.5, 0, 0), (0, -1, 0))
#gl.glFinish("SR6_medium.bmp")
#Low angle
#gl.glLookat((0, -0.3, 2), (0, 0, 0), (0, 1, 0))
#gl.generate_model('Ivysaur.obj', (0.7, 0.7, 0.7), (0.5, 0, 0), (0, -1, 0))
#gl.glFinish("SR6_lowAngle.bmp")
#High angle
#gl.glLookat((0, 3, 2), (0, 0, 0), (0, 1, 0))
#gl.generate_model('Ivysaur.obj', (0.7, 0.7, 0.7), (0.5, 0, 0), (0, -1, 0))
#gl.glFinish("SR6_highAngle.bmp")
#Dutch Angle
gl.glLookat((0, 0.5, 2), (0, 0, 0), (0.3, 1, 0))
gl.generate_model('Ivysaur.obj', (0.7, 0.7, 0.7), (0.5, 0, 0), (0, -1, 0))
gl.glFinish("SR6_dutchAngle.bmp")
