def calc_mesh(m, a, b, n1, n2, n3):
    # Variables
    verts = []
    faces = []
    edges = []
    # 3D Supershape
    ### m = 14.23
    ### a = -0.06
    ### b = 2.78
    ### n1 = 0.5
    ### n2 = -0.48
    ### n3 = 1.5
    scale = 3
    Unum = 50
    Vnum = 50
    Uinc = math.pi / (Unum/2)
    Vinc = (math.pi/2) / (Vnum/2)
    # Vertices
    theta = -math.pi
    for i in range (0, (Vnum + 1)*(Unum)):
        phi = -math.pi/2
        r1 = 1 / (((abs(math.cos(m*theta/4)/a))**n2 + (abs(math.sin(m*theta/4)/b))**n3)**n1)
        for j in range(0, Vnum+1):
            r2 = 1 / (((abs(math.cos(m*phi/4)/a))**n2 + (abs(math.sin(m*phi/4)/b))**n3)**n1)
            x = scale * (r1 * math.cos(theta) * r2 * math.cos(phi))
            y = scale * (r1 * math.sin(theta) * r2 * math.cos(phi))
            z = scale * (r2 * math.sin(phi))
            vert = (x,y,z)
            verts.append(vert)
            # Increment phi
            phi = phi + Vinc
        # Increment theta
        theta = theta + Uinc
    # Faces
    count = 0
    for i in range(0, (Vnum + 1)*Unum):
        if count < Vnum:
            A = i
            B = i + 1
            C = (i + (Vnum+1)) + 1
            D = (i + (Vnum+1))
            face = (D,C,B,A)
            faces.append(face)
            count = count + 1
        else:
            count = 0
    # Create Mesh and Object
    mymesh = bpy.data.meshes.new("Supershape")
    myobject = bpy.data.objects.new("Supershape", mymesh)
    # Set Mesh Location
    myobject.location = (0,0,0)
    # myobject.locaiton = bpy.context.scene.cursor_location
    bpy.context.scene.objects.link(myobject)
    # Create Mesh from Python data
    mymesh.from_pydata(verts, [], faces)
    mymesh.update(calc_edges = True)
    # Set the Object to Edit Mode
    bpy.context.scene.objects.active = myobject
    bpy.ops.object.mode_set(mode = "EDIT")
    # Remove Duplicate Vertices
    bpy.ops.mesh.remove_doubles()
    # Recalculate Normals
    bpy.ops.mesh.normals_make_consistent(inside = False)
    bpy.ops.object.mode_set(mode = "OBJECT")
    # Subdivide Modifier
    myobject.modifiers.new("subd", type = "SUBSURF")
    myobject.modifiers["subd"].levels = 3
    # Smooth Shading
    myploys = mymesh.polygons
    for p in myploys:
      p.use_smooth = True

