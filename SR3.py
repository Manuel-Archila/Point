import gl

gl.glCreateWindow(4000, 4000)

gl.glClear()
gl.glColor(0, 0, 1)
gl.generate('burger.obj', (500, 500), [600, 500])
#gl.generate('Trex.obj', (600, 600), [2000, 50])

gl.glFinish("Trex.bmp")
