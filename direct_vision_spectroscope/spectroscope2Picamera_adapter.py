
from build123d import *

# Parameters
diam_through = 18       # mm (goes all the way through)
diam_partial = 25       # mm (top cavity only)
depth_partial = 25      # mm
wall_thickness = 6      # mm

outer_diameter = diam_partial + 2 * wall_thickness  # 37 mm
total_height = 55  # 25 mm for the large cavity + 30 mm of continuous through-hole

# Build the part
with BuildPart() as connector:
    # Outer shell
    outer = Cylinder(radius=outer_diameter / 2, height=total_height)

    # Through hole (18 mm full length)
    hole_through = Cylinder(radius=diam_through / 2, height=total_height)

    # Larger cavity (25 mm, 25 mm deep at the top)
    hole_large = Cylinder(radius=diam_partial / 2, height=depth_partial).translate((0, 0, 0))  # start from top

    # Combine both holes
    internal = Compound([hole_through, hole_large])

    # Subtract from the shell
    connector.part = outer - internal

# Export to STL
export_stl(connector.part, "spectroscope_adapter_18mm_through_25mm_top.stl")

