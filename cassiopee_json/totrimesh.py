# Generate correct JSON files to represent the Étoile building
import trimesh
import json

path = "/Users/juliettedebono/Documents/TSP/Cassioppée/cassiopee/cassiopee_json/"
# path = ""
path_json = path + "json/"
windows_file = path_json + "windows.json" # Windows File
doors_file = path_json + "doors.json" # Doors File
rooms_file = path_json + "rooms.json" # Rooms File
files = [rooms_file, windows_file, doors_file]

height = 3.63 # Hauteur du bâtiment en mètre



def toTrimesh(coor):
    """Convert Polygon coordinates into Trmesh coordinates"""

    vertices_2D = coor[:-1]

    # Ajouter une troisième coordonnée pour chaque point
    vertices_3D = [[x, y, 0] for x, y in vertices_2D]
    vertices_3D += [[x, y, height] for x, y in vertices_2D]

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

    for file in files:
        json_file = read(file)
        for data in json_file:
            if data["relativePosition"]["value"]["type"] == "Polygon":
                data["relativePosition"]["value"]["type"] = "Trimesh"
                data["relativePosition"]["value"]["Dimensions"] = "3D"
                coor = data["relativePosition"]["value"]["coordinates"]
                vertices_3D, faces = toTrimesh(coor)
                data["relativePosition"]["value"]["faces"] = faces
                data["relativePosition"]["value"]["coordinates"] = vertices_3D
                print("Trimesh sur {}".format(data["id"].split(":")[-1]))
        write(file, json_file)

convert()