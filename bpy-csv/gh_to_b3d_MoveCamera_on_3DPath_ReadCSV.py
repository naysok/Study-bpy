import bpy
import csv
import math
scene = bpy.data.scenes["Scene"]
filePath = 'C:\\Users\\yoshioca\\Desktop\\181105.csv'
f = open(filePath, "r")
reader = csv.reader(f)
for i, row in enumerate(reader):
    # print(row)
    ### manege parameter
    x_rad = math.radians(float(row[3]))
    y_rad = math.radians(float(row[4]))
    z_rad = math.radians(float(row[5]))
    Camlocation = (float(row[0]), float(row[1]), float(row[2]))
    CamRotation = (x_rad, y_rad, z_rad)
    ### operate Blender
    scene.camera.location = Camlocation
    scene.camera.rotation_euler = CamRotation
    scene.camera.keyframe_insert(data_path = "location", frame=i)
    scene.camera.keyframe_insert(data_path = "rotation_euler", frame=i)
