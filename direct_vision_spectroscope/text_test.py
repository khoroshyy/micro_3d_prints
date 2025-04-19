from build123d import *

r2 = 100
r1 = 80
fs = 40

base_cylinder = Cylinder(r2, 300)
top = base_cylinder.faces().sort_by(Axis.Z)[-1]
text_path = (top - offset(top, r1 - r2)).face().inner_wires()[0]

text = Text(
    "around & around & around &", font_size=fs, path=text_path, position_on_path=0.45
    )
embossed_text = extrude(text, 5)

export_stl(embossed_text, "text_test.stl")
