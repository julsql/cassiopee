# Generate correct JSON files to represent the Étoile building
import json
import re
import matplotlib.pyplot as plt


room = [(0, 0), 763, 328]
winds = [[0, 0, 0], [0, 1, 1], [0, 2, 2], [0, 2, 3]]
obj = "window"

wind_size = [30, 60, 120]
door_size = [30, 40]

room2 = [(0.0, 0.0), (7.63, 0.0), (7.63, 3.28), (0.0, 3.28), (0.0, 0.0)]

def coordinates_obj(coor_obj, coor_room, obj):
    """Give the 4 points of an object given:
    value, type of the windows and wich wall
    and the coordinates of the room
    val match with type : val_windows = {1 : 3.5, 2 : 4.5, 3 : 5.5}
    coor_wind : [a, type, wall]
    coor_room : [(x, y), length, width] -> 1st point, length, width
    return 2 points
    """
    epaisseur = 10
    a = int(coor_obj[0])
    type = int(coor_obj[1])
    wall = int(coor_obj[2])

    x = int(coor_room[0][0])
    y = int(coor_room[0][1])
    length = int(coor_room[1])
    width = int(coor_room[2])

    if obj == "window":
        val = wind_size
    else:
        val = door_size

    # wall = 0 : mur gauche
    # wall = 1 : mur haut
    # wall = 2 : mur droit
    # wall = 3 : mur bas

    # type = 0 : petit fenêtre
    # type = 1 : double fenêtre
    # type = 2 : triple fenêtre

    l = val[type]

    if wall == 0:
        z1 = ((x + a)/100, (y)/100)
        z2 = ((x + a)/100, (y + epaisseur)/100)
        z3 = ((x + a + l)/100, (y + epaisseur)/100)
        z4 = ((x + a + l)/100, (y)/100)

    if wall == 1:
        z1 = ((x + length)/100, (y + a)/100)
        z2 = ((x + length + epaisseur)/100, (y + a)/100)
        z3 = ((x + length + epaisseur)/100, (y + a + l)/100)
        z4 = ((x + length)/100, (y + a + l)/100)

    if wall == 2:
        z1 = ((x + a)/100, (y + width)/100)
        z2 = ((x + a)/100, (y + width + epaisseur)/100)
        z3 = ((x + a + l)/100, (y + width + epaisseur)/100)
        z4 = ((x + a + l)/100, (y + width)/100)

    if wall == 3:
        z1 = ((x)/100, (y + a)/100)
        z2 = ((x + epaisseur)/100, (y + a)/100)
        z3 = ((x + epaisseur)/100, (y + a + l)/100)
        z4 = ((x)/100, (y + a + l)/100)

    return [z1, z2, z3, z4, z1]

def afficher(rectangles):
        """Affiche des rectangles sur un graphe
        Coordonées sous la forme
        [rect1, rect2, …]
        avec rect = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]"""

        fig, ax = plt.subplots()

        for rect1 in rectangles:

            try:
                x = [rect1[i][0] for i in range(5)]
                y = [-rect1[i][1] for i in range(5)]

                # Ajout des rectangles à l'axe
                ax.plot(x, y)
            except:
                None

        # L'axe x et y sont identiques
        ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
        ax.set_aspect('equal')

        fig.subplots_adjust(left=0.1, right=0.78)
        # Affichage de la figure
        plt.show()

coor = [room2]
for wind in winds:
    coor.append(coordinates_obj(wind, room, obj))
print(coor)
afficher(coor)