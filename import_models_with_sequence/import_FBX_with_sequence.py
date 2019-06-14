### WIMDOWS7

### Models [1 to N]



import bpy



for i in range(60):

    number = "%03d"%(i+1)
    tmp_name = "obj_" + number

    path = "C:\\Users\\yoshioca\\Documents\\Study-bpy\\import_models_with_sequence\\FBX_with_Sequence\\" + number + ".fbx"
    print(path)


    ### Import FBX
    bpy.ops.import_scene.fbx(filepath = path)


    ### get Scene
    scene = bpy.context.selected_objects[0]
    scene.name = "scene"
    scene.scale = (1, 1 ,1)
    scene.rotation_euler = (0,0,0)

    obj = bpy.context.selected_objects[1]
    obj.name = tmp_name
    obj.scale = (1, 1 ,1)
    obj.rotation_euler = (0, 0, 0)


    ### Get material
    mat_tmp = bpy.data.materials.get("NormalVec")

    ### Assign it to object
    if obj.data.materials:
        # assign to 1st material slot
        obj.data.materials[0] = mat_tmp
    else:
        # no slots
        obj.data.materials.append(mat_tmp)


    ### operate Blender
    obj.location = (0, 0, 10)
    obj.keyframe_insert(data_path = "location", frame=i-1)
    obj.location = (0, 0, 0)
    obj.keyframe_insert(data_path = "location", frame=i)
    obj.location = (0, 0, 10)
    obj.keyframe_insert(data_path = "location", frame=i+1)