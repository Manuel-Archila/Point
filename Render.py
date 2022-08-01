from WriteUtilities import * 
from Color import *
import Obj

class Render(object):
    def __init__(self, width, height):
        self.current_color = color(0, 0, 0)
        self.clearer = color(255, 255, 255)
        self.width = width
        self.height = height
        self.clear()
    
    def clear(self):
        self.framebuffer=[
            [self.clearer for x in range(self.width)]
            for y in range(self.height)
        ]

    def write(self, filename):
        f = open(filename, 'bw')
        
        #pixel header
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height*3))
        f.write(word(0))
        f.write(word(0))
        f.write(dword(14 + 40))
        
        #info header
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.height * self.width * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        
        #pixel data
        for x in range(self.height):
            for y in range(self.width):
                f.write(self.framebuffer[y][x])
        f.close()
        
    def point(self, x, y):
        self.framebuffer[x][y] = self.current_color
    
    def line(self, x0, y0, x1, y1):
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        m = dy * 2

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        offset = 0
        treshold = dx
        y = y0

        for x in range(x0, x1+1):
            if steep:
                self.point(y, x)
            else:
                self.point(x, y)
            offset += dy * 2

            if offset >= treshold:
                y += 1 if y0 < y1 else - 1
                treshold += dx * 2

    def verifier(self, number):
        color = max(min(number, 1), 0)
        actual = int(color * 255)
        return actual

    def setClearer(self, r, g, b):
        self.clearer = color(self.verifier(r), self.verifier(g), self.verifier(b))
    
    def setColor(self, r, g, b):
        self.current_color = color(self.verifier(r), self.verifier(g), self.verifier(b))

    
    def drawSquare(self, v1, v2, v3, v4):
        #print(v1, v2, v3, v4)
        self.line(round(v1[0]), round(v1[1]), round(v2[0]), round(v2[1]))
        self.line(round(v2[0]), round(v2[1]), round(v3[0]), round(v3[1]))
        self.line(round(v3[0]), round(v3[1]), round(v4[0]), round(v4[1]))
        self.line(round(v4[0]), round(v4[1]), round(v1[0]), round(v1[1]))
        
    
    def drawTriangle(self, v1, v2, v3):
        #print(v1, v2, v3, v4)
        self.line(round(v1[0]), round(v1[1]), round(v2[0]), round(v2[1]))
        self.line(round(v2[0]), round(v2[1]), round(v3[0]), round(v3[1]))
        self.line(round(v3[0]), round(v3[1]), round(v1[0]), round(v1[1]))
    
    def transform_vertex(self, vertex, scale, translate):
        return ((vertex[0] * scale[0]) + translate[0], (vertex[1] * scale[0] + translate[1]))
    
    def modelGenerator(self, filename, scale_factor, translate_factor):
        cube = Obj.Obj(filename)
        for face in cube.faces:
            if len(face) == 4:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
                f4 = face[3][0] - 1
    
                v1 = self.transform_vertex(cube.vertices[f1], scale_factor, translate_factor)
                v2 = self.transform_vertex(cube.vertices[f2], scale_factor, translate_factor)
                v3 = self.transform_vertex(cube.vertices[f3], scale_factor, translate_factor)
                v4 = self.transform_vertex(cube.vertices[f4], scale_factor, translate_factor)

                self.drawSquare(v1, v2, v3, v4)

            elif len(face) == 3:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
    
                v1 = self.transform_vertex(cube.vertices[f1], scale_factor, translate_factor)
                v2 = self.transform_vertex(cube.vertices[f2], scale_factor, translate_factor)
                v3 = self.transform_vertex(cube.vertices[f3], scale_factor, translate_factor)

                self.drawTriangle(v1, v2, v3)