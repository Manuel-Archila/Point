import gl

gl.glCreateWindow(4000, 4000)

gl.glClear()
gl.glColor(0, 0, 1)

#gl.generate_model('burger.obj', (700, 700, 700), [2000, 1000, 800])
gl.generate_model('Trex.obj', (600, 600, 200), [2000, 50, 2000])
#gl.generate('model.obj', (700, 700, 700), [2000, 1000, 800])

gl.glFinish("SR4.bmp")
gl.glFinishZ("Zbuffer.bmp")