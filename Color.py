def color(r,g,b):
        return bytes([round(b),round(g),round(r)])

def zcolor(z):
        z = int(z*255)
        return bytes([z,z,z])