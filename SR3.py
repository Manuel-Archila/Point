import gl

gl.glCreateWindow(4000, 4000)

gl.glClear()
gl.glColor(0, 0, 1)
gl.generate_wireframe('burger.obj', (700, 700, 0), [2000, 1000, 0])
#gl.generate('Trex.obj', (600, 600), [2000, 50])

gl.glFinish("SR3.bmp")
