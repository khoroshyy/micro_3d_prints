from build123d import *
from bd_warehouse.thread import IsoThread

# Parameters
diam_spectroscope = 18              # mm (lower bore, through)
diam_camera = 25              # mm (upper bore, cavity)
depth_camera = 25             # mm
depth_spectroscope = 30             # mm (lower bore, through)
wall_thickness = 6             # mm
thread_diameter = 6            # mm (M6)
thread_length = 10             # mm

outer_diameter = diam_camera +  2 * wall_thickness  # 
outer_radius = outer_diameter / 2
total_height = depth_camera + depth_spectroscope # mm
print(f"Total height: {total_height} mm")
# Z positions for side threads
z_thread_25 = 12.5             # middle of top cavity
z_thread_18 = 40               # middle of lower bore

with BuildPart() as connector:
    # Outer shell
    outer = Cylinder(radius=outer_radius, 
                     height=total_height)
    outer.position -= (0, 0, total_height/2)  # move to the XY plane
    # Step 1: create camera bore
    inner_partial = Cylinder(radius=diam_camera / 2, 
                             height=depth_camera)
    # Step 2: create spectrocope bore  
    inner_through = Cylinder(radius=diam_spectroscope/ 2, 
                             height=total_height)
    #move the inner bore to the XY plane
    inner_through.position -= (0, 0, total_height/2)  
    # move the partial bore to the XY plane
    inner_partial.position -= (0, 0, depth_camera/2)
    # # Subtract both cavities
    connector.part = outer - inner_through
    connector.part -= inner_partial
    # --- Embossed text on top face ---
    top_face = connector.part.faces().sort_by(Axis.Z)[-1]
    text_path = (top_face - offset(top_face, -2)).face().inner_wires()[0]

    with BuildSketch(Plane(face=top_face)) as sketch:
        Text(f"camera side {diam_camera} mm", font_size=4, path=text_path, position_on_path=0.0)

    embossed_text = extrude(sketch.sketch, amount=1)
    connector.part += embossed_text
    # Define the radius and position of the side hole
    side_hole_radius = 3  # Adjust as needed
    side_hole_position_z = z_thread_25  # Z-coordinate for the hole

	# Add a side hole
    with BuildSketch(Plane(origin=(outer_radius - wall_thickness / 2, 0, side_hole_position_z),
                       normal=Axis.Y)) as side_hole_sketch:
    	Circle(radius=side_hole_radius)

	# Extrude the side hole through the wall
    extrude(amount=-(wall_thickness), mode=Mode.SUBTRACT) 

# Export to STL
export_stl(connector.part, "spectroscope_adapter_with_step_and_threads.stl")
