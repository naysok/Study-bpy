# bpy-csv  

Python で、csv の操作をするモジュールは、csv や pandas など。  
pandas は、i X j で、csv にアクセスできるので便利だけど、
モジュールのインストールが必要。pip とかあるっぽい。  
デフォルトで使える csv で行けるところまで行ってみる。  


この辺の整備としてモチベーションとして、  
アニメーションのレンダリングは Blender でやるのだけど、  
絵作りの骨は Rhinoceros + Grasshopper で作り込みたい。  
位置関係や、変形、マテリアルなど。  


結果↓  
[![](https://img.youtube.com/vi/5v_j0n8Drtc/0.jpg)](https://www.youtube.com/watch?v=5v_j0n8Drtc)  


---  


###  異なるソフトウェアをまたぐこと  

異なるソフトをまたぐとき、ソフトごとに、仕様やネイティブなファイル形式などが違うので、値の操作やファイル処理にがギャップが生じる。  

異なるソフトをまたがって操作する際、連携の方法やそこでのギャップを吸収するために、何かの値を飛ばし続けることや、中間ファイルの作成、データベースを噛ませるなどのいくつかの方法がある。


- 値を飛ばし続ける  
  - シリアル通信や、OSC、Socket など  
  - リアルタイム性ある  

- 中間ファイルの作成  
  - png, csv など、どのソフトでも読み込めて処理できるファイルを作る  
  - ローカルの簡易なものならこれでok。
  - 僕の個人的な環境でいうと、Blender と、Rhino + Grasshopper には、Python が組み込まれているので、csv の処理が楽。さらに Python で細かな処理を書くこともあるので、まとめて python で繋いでいる。  

- データベース  
  - トランザクションとか堅牢性ある。データベースの中での高速な処理とか  
  - 書き込み、読み出しにネックがありそう  



---  


### Grasshopper で カメラの軌跡を作り、csv  

カメラのパスを、Rhinoceros で作り込む。大きさだけ注意。  
ライノの方が、 3次元のカーブをいじりやすいので（個人的に使い慣れているので）。

Curve を、DivideCurve で、ポイントのリストに。  
その時に、i番目の点と、i+1番目の点から、角度を算出しておく。  

それらを、GH_CPython で、位置と角度を csv にまとめる  
csv として書き出されるのは、  
x_pos, y_pos, z_pos, x_rot, y_rot, z_rot  

GH_CPython の中に書くのはこんな感じ  
```python
import math
a= []


path = "C:\Users\yoshioca\Desktop\\" + str(path_out) + ".csv"

for i in xrange(len(x)):
    pos = str(x[i]) + ", " +  str(y[i]) + ", " + str(z[i]) + ", "
    rot = str(x_Rot[i]) + ", " + str(y_Rot[i]) + ", " + str(z_Rot[i])
    temp = pos + rot
    a.append(temp)

    if i &lt; len(x)-1:
        a.append("\n")

if TF:
    f = open(path, "w")
    f.writelines(a)
    f.close
```

書き出される csv  
x_pos, y_pos, z_pos, x_rot, y_rot, z_rot  
```csv
2.777595, -4.640368, 1.289455, 447.869818, 0.0, 42.055181
2.961478, -4.474479, 1.298666, 447.790723, 0.0, 44.73034
3.137409, -4.300195, 1.30822, 447.722924, 0.0, 47.283463
3.305396, -4.118255, 1.318067, 447.665546, 0.0, 49.724327
3.465477, -3.929332, 1.328162, 447.617767, 0.0, 52.063274
3.61771, -3.734039, 1.338463, 447.578838, 0.0, 54.310856
3.762163, -3.53293, 1.348932, 447.548096, 0.0, 56.477593
（以下略）  
```





---  


### Blender で、csv から値を抜いてきて、キーフレームにアサイン  

for ループ内で無駄な行開けは NG（インタプリタの仕様）  

```python
import bpy
import csv
import math
scene = bpy.data.scenes["Scene"]
filePath = 'C:\\Users\\yoshioca\\Desktop\\181105.csv'
f = open(filePath, "r")
reader = csv.reader(f)
for i, row in enumerate(reader):
    ### manege parameter
    x_rad = math.radians(float(row[3]))
    y_rad = math.radians(float(row[4]))
    z_rad = math.radians(float(row[5]))
    CamLocation = (float(row[0]), float(row[1]), float(row[2]))
    CamRotation = (x_rad, y_rad, z_rad)
    ### operate Blender
    scene.camera.location = CamLocation
    scene.camera.rotation_euler = CamRotation
    scene.camera.keyframe_insert(data_path = "location", frame=i)
    scene.camera.keyframe_insert(data_path = "rotation_euler", frame=i)

```


---  


### テストとして書いたのはこんな感じ

x,y,z をタプルにして、  
```python
scene.camera.keyframe_insert(data_path = "location", frame=i)
```  

x,y,z それぞれやるときは、インデックスを指定（index = 0 or 1 or 2）  
```python
scene.camera.keyframe_insert(data_path = "scale", index=0, frame=i)
```

これは、ボックスを置くところからやっている  

```python  
import bpy
import csv

filePath = 'hogehoge.csv'

f = open(filePath, "r")
reader = csv.reader(f)
# header = next(reader)

bpy.ops.mesh.primitive_cube_add(location=(0,0,0))
cube = bpy.data.objects[bpy.context.object.name]


# for loop 内で、無駄な行空け NG

for i, row in enumerate(reader):
    # print(row)
    if (i > 0): # ヘッダーを処理
        ### manege parameter
        size = abs(float(row[2]))*1.25 + 0.1
        rot = float(row[2])*0.5
        ### operate Blender
        cube.scale.x = size
        cube.scale.y = size
        cube.scale.z = size
        cube.keyframe_insert(data_path = "scale", index=0, frame=i)
        cube.keyframe_insert(data_path = "scale", index=1, frame=i)
        cube.keyframe_insert(data_path = "scale", index=2, frame=i)
        # cube.rotation_euler.z = rot
        cube.rotation_euler.z = float(row[1])*0.005
        cube.keyframe_insert(data_path = "rotation_euler", index=2, frame=i)
```

