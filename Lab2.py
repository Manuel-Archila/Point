import gl

gl.glCreateWindow(1024, 1024)
gl.glClear()
gl.glColor(0, 0, 0)
gl.glViewPort(0, 0, 1024, 1024)
gl.assign_background('./back.bmp')
gl.glLookat((0.7, 0, 1), (0, 0, 0), (0, 1, 0))
gl.assign_planet_shader()
gl.generate_model('planet.obj', (0.4, 0.4, 0.4), (0, 0, 0), (0, 0, 0))
gl.glFinish("Lab2.bmp")
