import bpy


def add_cubes(count):

    for i in range(count):

        ### set location
        location = (i, i, i)

        ### add cube
        bpy.ops.mesh.primitive_cube_add(location = location)


add_cubes(10)



