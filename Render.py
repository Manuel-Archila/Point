from WriteUtilities import * 
from Color import *

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

        for x in range(x0, x1):
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
        