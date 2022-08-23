from WriteUtilities import * 
from Color import *
import Obj
from vector import *
import Textures as t

class Render(object):
    def __init__(self, width, height):
        self.current_color = color(0, 0, 0)
        self.clearer = color(255, 255, 255)
        self.width = width
        self.height = height
        self.texture = None
        self.clear()
    
    def clear(self):
        self.framebuffer=[
            [self.clearer for x in range(self.width)]
            for y in range(self.height)
        ]

        self.zbuffer = [
        [-9999999999999999999999999999 for x in range(self.width)]
        for y in range(self.height)
        ]

        self.ebuffer = [
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
        for y in range(self.height):
            for x in range(self.width):
                f.write(self.framebuffer[y][x])
        f.close()

    def writeZ(self, filename):
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
        for y in range(self.height):
            for x in range(self.width):
                f.write(self.ebuffer[y][x])
        f.close()
        
    def point(self, x, y):
        #print(x, y)
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
                self.point(x, y)
            else:
                self.point(y, x)
            offset += dy * 2

            if offset >= treshold:
                y += 1 if y0 < y1 else - 1
                treshold += dx * 2

    def lineVector(self, v1, v2):
        x0 = round(v1.x)
        y0 = round(v1.y)
        x1  = round(v2.x)
        y1 = round(v2.y)
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
                self.point(x, y)
            else:
                self.point(y, x)
            offset += dy * 2

            if offset >= treshold:
                y += 1 if y0 < y1 else - 1
                treshold += dx * 2

    def verifier(self, number):
        colorin = max(min(number, 1), 0)
        actual = int(colorin * 255)
        return actual

    def setClearer(self, r, g, b):
        self.clearer = color(self.verifier(r), self.verifier(g), self.verifier(b))
    
    def setColor(self, r, g, b):
        self.current_color = color(self.verifier(r), self.verifier(g), self.verifier(b))

    
    def drawSquare(self, v1, v2, v3, v4):
        #print(v1, v2, v3, v4)
        self.line(round(v1.x), round(v1.y), round(v2.x), round(v2.y))
        self.line(round(v2.x), round(v2.y), round(v3.x), round(v3.y))
        self.line(round(v3.x), round(v3.y), round(v4.x), round(v4.y))
        self.line(round(v4.x), round(v4.y), round(v1.x), round(v1.y))
        
    
    def drawTriangle(self, v1, v2, v3):
        #print(v1, v2, v3, v4)
        self.line(round(v1.x), round(v1.y), round(v2.x), round(v2.y))
        self.line(round(v2.x), round(v2.y), round(v3.x), round(v3.y))
        self.line(round(v3.x), round(v3.y), round(v1.x), round(v1.y))
    
    def transform_vertex(self, vertex, scale, translate):
        return V3((vertex[0] * scale[0]) + translate[0], (vertex[1] * scale[1] + translate[1]), (vertex[2] * scale[2] + translate[2]))
    
    def modelGenerator(self, filename, scale_factor, translate_factor):
        cube = Obj.Obj(filename)
        for face in cube.faces:
            #print(face)
            if len(face) == 4:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
                f4 = face[3][0] - 1
    
                v1 = self.transform_vertex(cube.vertices[f1], scale_factor, translate_factor)
                v2 = self.transform_vertex(cube.vertices[f2], scale_factor, translate_factor)
                v3 = self.transform_vertex(cube.vertices[f3], scale_factor, translate_factor)
                v4 = self.transform_vertex(cube.vertices[f4], scale_factor, translate_factor)
                if self.texture:
                    ft1 = face[0][1] - 1
                    ft2 = face[1][1] - 1
                    ft3 = face[2][1] - 1
                    ft4 = face[3][1] - 1

                    vt1 = V3(*cube.vt_vertices[ft1])
                    vt2 = V3(*cube.vt_vertices[ft2])
                    vt3 = V3(*cube.vt_vertices[ft3])
                    vt4 = V3(*cube.vt_vertices[ft4])
                    self.triangle((v1, v2, v3), (vt1, vt2, vt3))
                    self.triangle((v3, v4, v1), (vt3, vt4, vt1))
                else:
                    self.triangle((v1, v3, v4))
                    self.triangle((v1, v2, v3))

            elif len(face) == 3:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
    
                v1 = self.transform_vertex(cube.vertices[f1], scale_factor, translate_factor)
                v2 = self.transform_vertex(cube.vertices[f2], scale_factor, translate_factor)
                v3 = self.transform_vertex(cube.vertices[f3], scale_factor, translate_factor)
                if self.texture:
                    ft1 = face[0][1] - 1
                    ft2 = face[1][1] - 1
                    ft3 = face[2][1] - 1

                    vt1 = V3(*cube.vt_vertices[ft1])
                    vt2 = V3(*cube.vt_vertices[ft2])
                    vt3 = V3(*cube.vt_vertices[ft3])
                    self.triangle((v1, v2, v3), (vt1, vt2, vt3))
                else:
                    self.triangle((v1, v2, v3))

    def wireframeGenerator(self, filename, scale_factor, translate_factor):
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

    def bounding_box(self, A, B, C):
        xs = sorted([A.x, B.x, C.x])
        ys = sorted([A.y, B.y, C.y])
        return V3(xs[0], ys[0]), V3(xs[2], ys[2])
    
    def cross(self, v1, v2):
        return (v1.y * v2.z - v1.z * v2.y, 
                v1.z * v2.x - v1.x * v2.z, 
                v1.x * v2.y - v1.y * v2.x)
    
    def barycentric(self, A, B, C, P):
        cx, cy, cz = self.cross(V3(B.x - A.x, C.x - A.x, A.x - P.x), V3(B.y - A.y, C.y - A.y, A.y - P.y))
        if cz == 0:
            cz = 1
        u = cx/cz
        v = cy/cz
        w = 1 - (cx + cy)/cz
        return [w, v, u]
    
    def triangle(self, vertices, tvertices = None):
        A, B, C = vertices
        if self.texture:
            tA, tB, tC = tvertices
        L = V3(0, 0, -1)
        N = (C - A) * (B - A)
        i = N.norm() @ L.norm()

        if i <= 0 or i > 1:
            return

        self.current_color = color(round(25 * i * 10), round(25 * i * 10), round(25 * i * 10))

        bbox_min, bbox_max = self.bounding_box(A, B, C)
        for x in range(round(bbox_min.x), round(bbox_max.x + 1)):
            for y in range(round(bbox_min.y), round(bbox_max.y + 1)):
                w, v, u = self.barycentric(A, B, C, V3(x, y))
                if w < 0 or v < 0 or u < 0:
                    continue

                z = A.z * w + B.z * v + C.z * u
                #print(z)
                conv = z/self.width
                if self.zbuffer[x][y] < z:
                    self.zbuffer[x][y] = z
                    self.ebuffer[x][y] = color(255 * conv, 255 * conv, 255 * conv)
                    if self.texture:
                        tx = tA.x * w + tB.x * u + tC.x * v
                        ty = tA.y * w + tB.y * u + tC.y * v
                        self.current_color = self.texture.get_color_with_intensity(tx, ty, i)
                    self.point(y, x)