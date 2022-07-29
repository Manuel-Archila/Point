import gl

gl.glCreateWindow(2000, 2000)

gl.glClear()
gl.glColor(0, 0, 1)
gl.generate('Moon_Knight.obj', (50, 50), [1000, 500])

gl.glFinish("Trex.bmp")
