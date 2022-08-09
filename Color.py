def color(r,g,b):
        return bytes([round(r),round(g),round(b)])

def zcolor(z):
        z = int(z*255)
        return bytes([z,z,z])