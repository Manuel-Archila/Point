import gl
gl.glCreateWindow(4000, 4000)

gl.glClear()
gl.glColor(0, 0, 1)
gl.glViewPort(0, 0, 4000, 4000)

#gl.assign_texture('./earth.bmp')
gl.assign_texture('./Pokemon.bmp')
gl.glLookat((500, 0, 10), (0, 0, 0), (0, 1, 0))
gl.generate_model('Ivysaur.obj', (0.5, 0.5, 0.5), (0, 0, 0), (0, 0, 0))
gl.glFinish("matrices.bmp")
