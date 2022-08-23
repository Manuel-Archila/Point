import Render as rend
import Textures as text
from vector import V3
import Obj
from Color import color
r = rend.Render(4096, 4096)
t = text.Texture('./Pokemon.bmp')
r.width = t.width
r.height = t.height

r.framebuffer = t.pixels

cube = Obj.Obj('./Ivysaur.obj')
r.current_color = color(255, 255, 255)

for face in cube.faces:

  if len(face) == 3:

    ft1 = face[0][1] - 1
    ft2 = face[1][1] - 1
    ft3 = face[2][1] - 1

    vt1 = V3(
      cube.vt_vertices[ft1][0] * t.width,
      cube.vt_vertices[ft1][1] * t.height
    )
    vt2 = V3(
      cube.vt_vertices[ft2][0] * t.width,
      cube.vt_vertices[ft2][1] * t.height
    )
    vt3 = V3(
      cube.vt_vertices[ft3][0] * t.width,
      cube.vt_vertices[ft3][1] * t.height
    )

    r.lineVector(vt1, vt2)
    r.lineVector(vt2, vt3)
    r.lineVector(vt3, vt1)

  if len(face) == 4:

      ft1 = face[0][1] - 1
      ft2 = face[1][1] - 1
      ft3 = face[2][1] - 1
      ft4 = face[3][1] - 1


      vt1 = V3(
      cube.vt_vertices[ft1][0] * t.width,
      cube.vt_vertices[ft1][1] * t.height
      )
      vt2 = V3(
      cube.vt_vertices[ft2][0] * t.width,
      cube.vt_vertices[ft2][1] * t.height
      )
      vt3 = V3(
      cube.vt_vertices[ft3][0] * t.width,
      cube.vt_vertices[ft3][1] * t.height
      )
      vt4 = V3(
      cube.vt_vertices[ft4][0] * t.width,
      cube.vt_vertices[ft4][1] * t.height
      )
      
      r.lineVector(vt1, vt2)
      r.lineVector(vt2, vt3)
      r.lineVector(vt3, vt4)
      r.lineVector(vt4, vt1)

r.write("Texture_SR5.bmp")