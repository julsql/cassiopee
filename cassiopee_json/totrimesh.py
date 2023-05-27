# Generate correct JSON files to represent the Étoile building
import trimesh
import json
import re
import numpy as np
import os

path = os.getcwd() + "/"
path_json = path + "cassiopee_json/json_ld/"
windows_file = path_json + "windows.json" # Windows File
doors_file = path_json + "doors.json" # Doors File
rooms_file = path_json + "rooms.json" # Rooms File

path_json_tri = path + "cassiopee_json/json_trimesh/"
windows_file_tri = path_json_tri + "windows.json" # Windows File
doors_file_tri = path_json_tri + "doors.json" # Doors File
rooms_file_tri = path_json_tri + "rooms.json" # Rooms File

files = [rooms_file, windows_file, doors_file]
files_tri = [rooms_file_tri, windows_file_tri, doors_file_tri]

height = [(0, 3.63), (0.81, 2.58), (0, 2.04)] # Hauteur du bâtiment en mètre

def toTrimesh(coor, typeObject):
    """Convert Polygon coordinates into Trmesh coordinates"""

    vertices_2D = coor[:-1]

    # Ajouter une troisième coordonnée pour chaque point
    vertices_3D = [[x, y, height[typeObject][0]] for x, y in vertices_2D]
    vertices_3D += [[x, y, height[typeObject][1]] for x, y in vertices_2D]

    # Créer une trimesh à partir des coordonnées du pavé
    faces = [[0, 1, 2], [0, 2, 3], [4, 5, 6], [4, 6, 7], [0, 4, 5], [0, 5, 1], [1, 5, 6], [1, 6, 2], [2, 6, 7], [2, 7, 3], [3, 7, 4], [3, 4, 0]]
    # pave = trimesh.Trimesh(vertices=vertices_3D, faces=faces)
    # Afficher le pavé en 3D
    # pave.show()

    return vertices_3D, faces



def read(filename):
    """Convert a JSON file in a python dictionary"""

    with open(filename, "r") as f:
        data = json.load(f)
    return data



def write(filename, json_array):
    """Write a python dictionary in a JSON file"""

    to_write = json.dumps(json_array, indent=4) # Convert JSON in String with tab
    with open(filename, 'w') as f:
        f.write(to_write)
    return None



def convert():
    """Convert all the file with Polygon value into Trimesh"""

    typeObject = 0
    for i in range(len(files)):
        file = files[i]
        file_trimesh = files_tri[i]
        print(file, typeObject)
        json_file = read(file)
        for data in json_file:
            if data["relativePosition"]["value"]["type"] == "Polygon":
                data["relativePosition"]["value"]["type"] = "Trimesh"
                data["relativePosition"]["value"]["Dimensions"] = "3D"
                coor = data["relativePosition"]["value"]["coordinates"]
                vertices_3D, faces = toTrimesh(coor, typeObject)
                data["relativePosition"]["value"]["faces"] = faces
                data["relativePosition"]["value"]["coordinates"] = vertices_3D
                print("Trimesh sur {}".format(data["id"].split(":")[-1]))
        write(file_trimesh, json_file)
        typeObject += 1

convert()

def is_floor(id, floor):
    match = re.search(r'F(\d+)', id)

    if match:
        return floor == int(match.group(1))
    return False

def get_trimesh(file, floor):
    """Convert all the Trimesh in an .obj file"""

    json_file = read(file)
    trimesh_list = []
    for data in json_file:
        if is_floor(data["id"], floor):
            if data["relativePosition"]["value"]["type"] == "Trimesh":

                faces = data["relativePosition"]["value"]["faces"]
                vertices_3D = data["relativePosition"]["value"]["coordinates"]
                mesh = trimesh.Trimesh(vertices=vertices_3D, faces=faces)
                trimesh_list.append(mesh)
    return trimesh_list

def color_faces(mesh, color):
    # Create a per-face color array with the specified color for all faces
    face_colors = np.tile(color, (len(mesh.faces), 1))

    # Set the face_colors attribute of the mesh's visual
    mesh.visual.face_colors = face_colors

def add_color(file, color):
     # Ouvrir le fichier en mode lecture
    with open(file, 'r') as f:
        content = f.readlines()

    # Ajouter les lignes au début du fichier
    content.insert(0, 'mtllib floor_colors.mtl\n')
    content.insert(1, f'usemtl {color}_material\n')

    # Ouvrir le fichier en mode écriture et écrire le contenu modifié
    with open(file, 'w') as f:
        f.writelines(content)


def create_obj(floor):
    trimesh_list = get_trimesh(rooms_file_tri, floor)
    # Exporter l'objet trimesh au format .obj
    merged = trimesh.util.concatenate(trimesh_list)
    output_path = f'flutter/app_Etoile_building/obj/floor_{floor}_rooms.obj'
    merged.export(output_path)

    trimesh_list = get_trimesh(doors_file_tri, floor)
    # Exporter l'objet trimesh au format .obj
    merged = trimesh.util.concatenate(trimesh_list)
    output_path = f'flutter/app_Etoile_building/obj/floor_{floor}_doors.obj'
    merged.export(output_path)
    add_color(output_path, "red")

    trimesh_list = get_trimesh(windows_file_tri, floor)
    # Exporter l'objet trimesh au format .obj
    merged = trimesh.util.concatenate(trimesh_list)
    output_path = f'flutter/app_Etoile_building/obj/floor_{floor}_windows.obj'
    merged.export(output_path)
    add_color(output_path, "blue")


create_obj(1)
create_obj(2)
create_obj(3)
create_obj(4)