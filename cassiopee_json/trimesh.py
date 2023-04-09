# Generate correct JSON files to represent the Étoile building
import numpy as np
import trimesh # pip install trimesh


def coordinates_room(coor):
    """Give the 4 room points given:
    Fonction qui renvoie les quatre points de la pièce à partir :
    down left point, length, width
    coor : [(a, b), length, width] -> 1st point, length, width
    return point down-left, down-right, up-left, up-right
    """
    a = int(coor[0][0])
    b = int(coor[0][1])
    length = int(coor[1])
    width = int(coor[2])

    # zi = (xi, yi)
    z1 = ((a)/100, (b)/100)
    z2 = ((a+length)/100, (b)/100)
    z3 = ((a+length)/100, (b+width)/100)
    z4 = ((a)/100, (b+width)/100)

    return [z1, z2, z3, z4]


def polygon_trimesh(coor):
    rect = np.array(coor)
    height = 2.0 # hauteur du pavé en 3D
    pave = np.hstack((rect, np.ones((4,1))*height))
    triangles = np.array([[0, 1, 2], [0, 2, 3]])
    # Création de l'objet Trimesh
    mesh = trimesh.Trimesh(vertices=pave, faces=triangles)

    # Affichage de l'objet Trimesh
    mesh.show()
    return None

coor = coordinates_room([(0, 0), 400, 400])
polygon_trimesh(coor)