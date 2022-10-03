def color(r,g,b):
        return bytes([min(max(round(b), 0), 255),min(max(round(g), 0), 255),min(max(round(r), 0), 255)])

def zcolor(z):
        z = int(z*255)
        return bytes([z,z,z])
