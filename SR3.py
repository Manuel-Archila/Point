import gl

gl.glCreateWindow(2000, 2000)

gl.glClear()
gl.glColor(0, 0, 1)
gl.generate('burger.obj', (500, 500), [600, 500])

gl.glFinish("Trex.bmp")
