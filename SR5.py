import gl

gl.glCreateWindow(4000, 4000)

gl.glClear()
gl.glColor(0, 0, 1)

#gl.assign_texture('./earth.bmp')
gl.assign_texture('./Pokemon.bmp')
gl.generate_model('Ivysaur.obj', (1000, 1000, 500), [2000, 1000, 500])
#gl.generate_model('earth.obj', (4, 4, 6), [2000, 2000, 100])
#gl.assign_texture('./R2_diffuse.bmp')
#gl.generate_model('R2D2.obj', (100, 100, 10), [1000, 1000, 100])
#gl.generate_model('burger.obj', (700, 700, 700), [2000, 1000, 800])
#gl.assign_texture('./model.bmp')
#gl.generate_model('model.obj', (700, 700, 700), [2000, 1000, 800])
gl.glFinish("SR5.bmp")