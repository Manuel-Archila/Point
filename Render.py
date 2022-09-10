from WriteUtilities import * 
from Color import *
import Obj
from vector import *
import Textures as t
from math import *
from matrix import *

class Render(object):
    def __init__(self, width, height):
        self.current_color = color(0, 0, 0)
        self.clearer = color(255, 255, 255)
        self.width = width
        self.height = height
        self.texture = None
        self.Model = None
        self.View = None
        self.Projection = None
        self.Viewport = None
        self.viewport = {}
        self.active_shader = None
        self.light = V3(0, 0, -1)
        self.vertex_buffer_object = []
        self.clear()

    def loadModelMatrix(self, translate=(0, 0, 0), scale=(1, 1, 1), rotate = (0, 0, 0)):
        translate = V3(*translate)
        scale = V3(*scale)
        rotate = V3(*rotate)

        translationMatrix = M([
            [1, 0, 0, translate.x],
            [0, 1, 0, translate.y],
            [0, 0, 1, translate.z],
            [0, 0, 0, 1],
            ])
        
        scaleMatrix = M([
            [scale.x, 0, 0, 0],
            [0, scale.y, 0, 0],
            [0, 0, scale.z, 0],
            [0, 0, 0, 1]
        ])

        a = rotate.x
        rotation_x = M([
            [1,      0,       0, 0],
            [0, cos(a), -sin(a), 0],
            [0, sin(a),  cos(a), 0],
            [0,      0,       0, 1],
        ])

        a = rotate.y
        rotation_y = M([
            [cos(a), 0, sin(a), 0],
            [     0,      1, 0, 0],
            [-sin(a), 0, cos(a), 0],
            [     0,      0, 0, 1],
        ])

        a = rotate.z
        rotation_z = M([
            [cos(a), -sin(a), 0, 0],
            [sin(a), cos(a), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ])

        rotationMatrix = rotation_x * rotation_y
        rotationMatrix = rotationMatrix * rotation_z
        self.Model = translationMatrix * rotationMatrix * scaleMatrix
    
    def loadViewMatrix(self, x, y, z, center):
        Mi = M([
            [x.x, x.y, x.z, 0],
            [y.x, y.y, y.z, 0],
            [z.x, z.y, z.z, 0],
            [0, 0, 0, 1]
        ])

        O = M([
            [1, 0, 0, -center.x],
            [0, 1, 0, -center.y],
            [0, 0, 1, -center.z],
            [0, 0, 0, 1]
        ])

        self.View = Mi * O

    def lookAt(self, eye, center, up):
        eye = V3(*eye)
        center = V3(*center)
        up = V3(*up)
        z = (eye - center).norm()
        x = (up * z).norm()
        y = (z * x).norm()
        self.loadViewMatrix(x, y, z, center)
        self.loadProjectionMatrix(eye, center)
        

    def loadProjectionMatrix(self, eye, center):
        coef = -1/(eye.length() - center.length())
        self.Projection = M([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, coef, 1]
        ])
    
    def loadViewportMatrix(self):
        x = 0
        y = 0
        self.Viewport = M([
            [self.viewport["width"], 0, 0, x + self.viewport["width"]],
            [0, self.viewport["height"], 0, y + self.viewport["height"]],
            [0, 0, 128, 128],
            [0, 0, 0, 1]
        ])

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
    
    def transform_vertex(self, vertex):
        augmented_vertex =M([
            [vertex[0]],
            [vertex[1]],
            [vertex[2]],
            [1]
        ])
        if(self.View and self.Projection):
            transformed_vertex = self.Viewport * self.Projection * self.View * self.Model * augmented_vertex
        else:
            transformed_vertex = self.Model * augmented_vertex
        #return transformed_vertex
        return V3(
            transformed_vertex.mat[0][0] / transformed_vertex.mat[3][0],
            transformed_vertex.mat[1][0] / transformed_vertex.mat[3][0],
            transformed_vertex.mat[2][0] / transformed_vertex.mat[3][0]
        )
    
    def modelGenerator(self, filename, scale = (1, 1, 1), translate = (0, 0, 0), rotate = (0, 0, 0)):
        self.loadModelMatrix(translate, scale, rotate)
        cube = Obj.Obj(filename)
        for face in cube.faces:
            #print(face)
            if len(face) == 4:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
                f4 = face[3][0] - 1
    
                v1 = self.transform_vertex(cube.vertices[f1])
                v2 = self.transform_vertex(cube.vertices[f2])
                v3 = self.transform_vertex(cube.vertices[f3])
                v4 = self.transform_vertex(cube.vertices[f4])
                
                if self.texture:
                    ft1 = face[0][1] - 1
                    ft2 = face[1][1] - 1
                    ft3 = face[2][1] - 1
                    ft4 = face[3][1] - 1

                    vt1 = V3(*cube.vt_vertices[ft1])
                    vt2 = V3(*cube.vt_vertices[ft2])
                    vt3 = V3(*cube.vt_vertices[ft3])
                    vt4 = V3(*cube.vt_vertices[ft4])

                    self.vertex_buffer_object.append(v1)
                    self.vertex_buffer_object.append(v2)
                    self.vertex_buffer_object.append(v3)
                    self.vertex_buffer_object.append(vt1)
                    self.vertex_buffer_object.append(vt2)
                    self.vertex_buffer_object.append(vt3)

                    self.vertex_buffer_object.append(v3)
                    self.vertex_buffer_object.append(v4)
                    self.vertex_buffer_object.append(v1)
                    self.vertex_buffer_object.append(vt3)
                    self.vertex_buffer_object.append(vt4)
                    self.vertex_buffer_object.append(vt1)


                else:
                    self.vertex_buffer_object.append(v1)
                    self.vertex_buffer_object.append(v2)
                    self.vertex_buffer_object.append(v3)

                    self.vertex_buffer_object.append(v3)
                    self.vertex_buffer_object.append(v4)
                    self.vertex_buffer_object.append(v1)
                
                if self.active_shader:
                    print("estoy entrando")
                    fn1 = face[0][2] - 1
                    fn2 = face[1][2] - 1
                    fn3 = face[2][2] - 1
                    fn4 = face[3][2] - 1
    
                    vn1 = V3(*cube.nvertices[fn1])
                    vn2 = V3(*cube.nvertices[fn2])
                    vn3 = V3(*cube.nvertices[fn3])
                    vn4 = V3(*cube.nvertices[fn4])

                    self.vertex_buffer_object.append(vn1)
                    self.vertex_buffer_object.append(vn2)
                    self.vertex_buffer_object.append(vn3)

                    self.vertex_buffer_object.append(vn3)
                    self.vertex_buffer_object.append(vn4)
                    self.vertex_buffer_object.append(vn1)
                

            elif len(face) == 3:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
    
                v1 = self.transform_vertex(cube.vertices[f1])
                v2 = self.transform_vertex(cube.vertices[f2])
                v3 = self.transform_vertex(cube.vertices[f3])
                
                if self.texture:
                    ft1 = face[0][1] - 1
                    ft2 = face[1][1] - 1
                    ft3 = face[2][1] - 1

                    vt1 = V3(*cube.vt_vertices[ft1])
                    vt2 = V3(*cube.vt_vertices[ft2])
                    vt3 = V3(*cube.vt_vertices[ft3])

                    self.vertex_buffer_object.append(v1)
                    self.vertex_buffer_object.append(v2)
                    self.vertex_buffer_object.append(v3)
                    self.vertex_buffer_object.append(vt1)
                    self.vertex_buffer_object.append(vt2)
                    self.vertex_buffer_object.append(vt3)
                else:
                    self.vertex_buffer_object.append(v1)
                    self.vertex_buffer_object.append(v2)
                    self.vertex_buffer_object.append(v3)

                if self.active_shader:
                    print("estoy entrando")
                    fn1 = face[0][2] - 1
                    fn2 = face[1][2] - 1
                    fn3 = face[2][2] - 1

                    vn1 = V3(*cube.nvertices[fn1])
                    vn2 = V3(*cube.nvertices[fn2])
                    vn3 = V3(*cube.nvertices[fn3])

                    self.vertex_buffer_object.append(vn1)
                    self.vertex_buffer_object.append(vn2)
                    self.vertex_buffer_object.append(vn3)
                    
        self.generate()

    def wireframeGenerator(self, filename, scale = (1, 1, 1), translate = (0, 0, 0), rotate = (0, 0, 0)):
        self.loadModelMatrix(translate, scale, rotate)
        cube = Obj.Obj(filename)
        for face in cube.faces:
            if len(face) == 4:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
                f4 = face[3][0] - 1
    
                v1 = self.transform_vertex(cube.vertices[f1])
                v2 = self.transform_vertex(cube.vertices[f2])
                v3 = self.transform_vertex(cube.vertices[f3])
                v4 = self.transform_vertex(cube.vertices[f4])

                self.drawSquare(v1, v2, v3, v4)

            elif len(face) == 3:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
    
                v1 = self.transform_vertex(cube.vertices[f1])
                v2 = self.transform_vertex(cube.vertices[f2])
                v3 = self.transform_vertex(cube.vertices[f3])

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
    
    def triangle(self):
        A = next(self.vertex_buffer_object)
        B = next(self.vertex_buffer_object)
        C = next(self.vertex_buffer_object)
        if self.texture:
            tA = next(self.vertex_buffer_object)
            tB = next(self.vertex_buffer_object)
            tC = next(self.vertex_buffer_object)
        if self.active_shader:
            nA = next(self.vertex_buffer_object)
            nB = next(self.vertex_buffer_object)
            nC = next(self.vertex_buffer_object)

        N = (C - A) * (B - A)
        L = V3(0, 0, -1)
        i = N.norm() @ L.norm()

        if i <= 0 or i > 1:
            return
        
        grey = round(255 * i)

        self.current_color = color(grey, grey, grey)

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

                    if(self.active_shader):
                        self.current_color = self.active_shader(
                                            self,
                                            bar = (w, u, v),
                                            vertices = (A, B, C),
                                            texture_coords = (tA, tB, tC),
                                            normals = (nA, nB, nC),
                                            light = self.light
                                            )
                    else:
                        if self.texture:
                            tx = tA.x * w + tB.x * u + tC.x * v
                            ty = tA.y * w + tB.y * u + tC.y * v
                            self.current_color = self.texture.get_color_with_intensity(tx, ty, i)
                    self.point(y, x)
    
    def generate(self):
        self.vertex_buffer_object = iter(self.vertex_buffer_object)
        try:
            while True:
                self.triangle()
        except Exception:
            StopIteration
   
    def shader(render, **kwargs):
        tA, tB, tC = kwargs['texture_coordinates']
        w, u, v = kwargs['bar']
        L = kwargs['light']
        A, B, C = kwargs['vertices']
        nA, nB, nC = kwargs['normals']

        
        iA = nA.norm() @ L.norm()
        iB = nB.norm() @ L.norm()
        iC = nC.norm() @ L.norm()

        i = iA * w + iB * u + iC * v

        if render.texture:
            tx = tA.x * w + tB.x * u + tC.x * v
            ty = tA.y * w + tB.y * u + tC.y * v
            b, g, r = render.texture.get_color_with_intensity(tx, ty, i)
            return color(r, g, b) 