# Nathan's Blender Python Notebook  

180909 - 190102  

[http://wiki.theprovingground.org/blender-python](http://wiki.theprovingground.org/blender-python)  



---


### Index  

- [x] Environment  
- [x] SetUp  
- [ ] ~~Meshes~~  
- [x] MeshDefinition  
- [x] Modifiers  
- [x] MathematicalMesh  
- [x] RandomMesh  
- [x] Supershape3D  


---  

---  


### Environment  

x  


---  


### SetUp  

// 諸設定  


Import Libraries  
```python
import bpy # Blender Python API
import mathutils # Blender vector math utilities
import math # standard Python math library
```

Print  
```python
hello = "Hello World.\nHello bpy."
print(hello)

```

Create Cube  
```python
import bpy

bpy.ops.mesh.primitive_cube_add(location = (1,2,3))

x1 = 2
y1 = 3
z1 = 4
bpy.ops.mesh.primitive_cube_add(location = (x1,y1,z1))

```

for Loop  
```python
for m in range(0,10):
    x2 = 3*m
    y2 = 0
    z2 = 0
    bpy.ops.mesh.primitive_cube_add(location=(x2,y2,z2))


for i in range(0,10):
    for j in range(0,10):
        x3 = 3*i
        y3 = 3*j
        z3 = 0
        bpy.ops.mesh.primitive_cube_add(location=(x3,y3,z3))


for i in range(0, 10):
    for j in range(0, 10):
        x4 = i*3
        y4 = j*3
        z4 = 0
        bpy.ops.mesh.primitive_monkey_add(location=(x4,y4,z4))
```


---  


### ~~Meshes~~  


---  


### MeshDefinition  

// メッシュを構築する  


複数の頂点情報から、ポリメッシュを構築する。  

4つの頂点から、Plane を作成する   
```python
import bpy

# Define Vertices and faces
verts = [(0,0,0), (0,5,0), (5,5,0), (5,0,0)]
face = [(0,1,2,3)]

# Define mesh and variables
mymesh = bpy.data.meshes.new("plane1")
myobject = bpy.data.objects.new("plane1", mymesh)

# Set location and scene of object
myobject.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(myobject)

# Create mesh
mymesh.from_pydata(verts, [], face)
mymesh.update(calc_edges = True)

```
![photo](photo/Nathan-s-Blender-Python-Create-Plane.png)  



8つの頂点から、Cube を作成する  
```python
import bpy

# Define vertices, faecs, edges
verts = [(0,0,0), (0,5,0), (5,5,0), (5,0,0), (0,0,5), (0,5,5), (5,5,5), (5,0,5)]
faces = [(0,1,2,3), (4,5,6,7), (0,4,5,1), (1,5,6,2), (2,6,7,3), (3,7,4,0)]

# Define mesh and objects
mesh = bpy.data.meshes.new("cube1")
object = bpy.data.objects.new("cube1", mesh)

# Set location and scene of object
object.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(object)

# Create mesh
mesh.from_pydata(verts, [], faces)
mesh.update(calc_edges = True)
```
![photo](photo/Nathan-s-Blender-Python-Create-Cube.png)  




5つの頂点から、Pyramid を作成する  
```python
import bpy

# Define vertices and face
verts = [(0,0,0), (0,5,0), (5,5,0), (5,0,0), (2.5,2.5,4)]
faces = [(0,1,2,3), (0,4,1), (1,4,2), (2,4,3), (3,4,0)]

# Define mesh and object
mesh = bpy.data.meshes.new("pyramid1")
object = bpy.data.objects.new("pyramid1", mesh)

# Set location and scene of object
object.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(object)

# Create mesh
mesh.from_pydata(verts, [], faces)
mesh.update(calc_edges = True)

```
![photo](photo/Nathan-s-Blender-Python-Create-Pyramid.png)  


---  


### Modifiers  

// モディファイアーを操作する  


Subdivision Modifier  

```python
import bpy

# Difine Vertices, Faces, edges
verts = [(0,0,0),(0,5,0),(5,5,0),(5,0,0),(0,0,5),(0,5,5),(5,5,5),(5,0,5)]
faces = [(0,1,2,3), (7,6,5,4), (0,4,5,1), (1,5,6,2), (2,6,7,3), (3,7,4,0)]

# Define Mesh and Object
mymesh = bpy.data.meshes.new("Cube")
myobject = bpy.data.objects.new("Cube", mymesh)

# Set Location and Scene of Object
myobject.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(myobject)

# Create meshes
mymesh.from_pydata(verts, [], faces)
mymesh.update(calc_edges = True)

# Subdivide Modifier
myobject.modifiers.new("subd", type = "SUBSURF")

# Increase Subdivision
myobject.modifiers["subd"].levels = 3

# Smooth Shading
mypolys = mymesh.polygons
for p in mypolys:
    p.use_smooth = True

```

![photo](photo/Nathan-s-Blender-Python-Subdivide.png)  

![photo](photo/Nathan-s-Blender-Python-Subdivide-Levels.png)  

![photo](photo/Nathan-s-Blender-Python-Shading-Smooth.png)  


---  


### MathematicalMesh  

// 数式を使ってジオメトリを作る  


wave surface  

```python
import bpy
import math


# Variables
verts = []
faces = []

numX = 10
numY = 10

# wave Variables
freq = 1
amp = 1
scale = 1


# Vertices
for i in range(0, numX):
    for j in range(0, numY):
        x = scale * i
        y = scale * j
        z = scale * ((amp*math.cos(i*freq)) + (amp*math.sin(j*freq)))
        vert = (x,y,z)
        verts.append(vert)


# Faces
count = 0

for i in range(0, numY*(numX -1)):
    if count < numX -1:
        A = i
        B = i + 1
        C = (i + numY) + 1
        D = (i + numY)
        face = (A,B,C,D)
        faces.append(face)
        count = count + 1
    else:
        count = 0;


# Create mesh and object
mesh = bpy.data.meshes.new("wave")
object = bpy.data.objects.new("wave", mesh)

# Set Mesh Location
object.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(object)

# Create Mesh From Python data
mesh.from_pydata(verts, [], faces)
mesh.update(calc_edges = True)


# Smooth Shading
mypolys = mesh.polygons
for p in mypolys:
    p.use_smooth = True

```

![photo](photo/Nathan-s-Blender-Python-MathematicalMesh.png)  


---  


### RandomMesh  

// random module を使ったモデリング  


ライブラリの読み込み  
```python
import bpy
import random


# Variables
verts = []
faces = []

numX = 20
numY = 20

amp = 0.65
scale = 1


# Vertices
for i in range(0, numX):
    for j in range(0, numY):
        x = scale * i
        y = scale * j
        z = (i * random.random()) * amp
        vert = (x,y,z)
        verts.append(vert)


# Faces
count = 0

for i in range(0, numY*(numX-1)):
    if count < numY - 1:
        A = i
        B = i + 1
        C = (i + numY) + 1
        D = (i + numY)
        # face = (A,B,C,D)
        face = (D,C,B,A)
        faces.append(face)
        count = count + 1
    else:
        count = 0


# Create Mesh and Object
mymesh = bpy.data.meshes.new("random_mesh")
myobject = bpy.data.objects.new("random_mesh", mymesh)


# Set Mesh Location
# myobject.location = bpy.context.scene.cursor_location
myobject.location = (0,0,0)
bpy.context.scene.objects.link(myobject)


# Create Mesh from Python Data
mymesh.from_pydata(verts, [], faces)
mymesh.update(calc_edges = True)


# Subdivide Modifier
myobject.modifiers.new("subd", type = "SUBSURF")
myobject.modifiers["subd"].levels = 3


# Smooth Shading
mypolys = mymesh.polygons
for p in mypolys:
    p.use_smooth = True


```

![photo](photo/Nathan-s-Blender-Python-RandomSurface.png)  


---  


### Supershape3D  


// parametric geometry  


```python
import bpy
import math

# Variables
verts = []
faces = []
edges = []


# 3D Supershape
m = 14.23
a = -0.06
b = 2.78
n1 = 0.5
n2 = -0.48
n3 = 1.5

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


```

![photo](photo/Nathan-s-Blender-Python-Supershape.png)  

---  
