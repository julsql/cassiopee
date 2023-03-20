#!/opt/homebrew/bin/python3

# Génère des fichiers JSON corrects pour représenter le bâtiment étoile
import json
import re

floor = 2 # Étage dans lequel on ajoute les pièces

windows_file = "windows.json" # Fichier des fenêtres du bâtiment
doors_file = "doors.json" # Fichier des portes du bâtiment
rooms_file = "rooms.json" # Fichier des pièces du bâtiment
building_file = "building.json" # Fichier des pièces du bâtiment
floors_file = "floors.json" # Fichier des étages du bâtiment
models_file = "models.json" # Fichier des pièces du bâtiment

id_model = "urn:ngsi-ld:{0}:SmartCitiesdomain:SmartBuildings:{1}" # Model de l'ID d'un objet

def read(filename):
    """Fonction pour convertir un fichier JSON en un tableau python"""

    with open(filename, "r") as f:
        data = json.load(f)
    return data



def write(filename, json_array):
    """Fonction pour écrire le tableau dans un fichier JSON"""

    to_write = json.dumps(json_array, indent=4) # Converti du json en string avec mise en page
    with open(filename, 'w') as f:
        f.write(to_write)
    return None



def clean(file_array):
    """Fonction pour vider les fichiers JSON en un tableau vide"""

    for file in file_array:
        write(file, [])
    return None



def add(filename, json_array):
    """Fonction pour ajouter un tableau à un fichier JSON"""

    json_file = read(filename)
    for data in json_file:
        if data["id"] == json_array["id"]:
            # On vérifie l'id de chaque objet du fichier JSON
            # Si l'id de l'objet qu'on veut ajouter existe déjà, on lève une erreur
            raise(ValueError("id non unique : {}".format(json_array["id"])))

    json_file.append(json_array)
    write(filename, json_file)
    return None



def add_floors():
    """Fonction pour ajouter tous les étages"""

    # Infos de tous les étages
    floors = [{"id": id_model.format("Floor", "B1F0a"), "name" : "TERRAIN", "description": "TERRAIN"},
    {"id": id_model.format("Floor", "B1F0b"), "name" : "Sub-Structure (foundations)", "description": "Sub-Structure (foundations)"},
    {"id": id_model.format("Floor", "B1F0"), "name" : "Ground Floor", "description": "Ground Floor"},
    {"id": id_model.format("Floor", "B1F1"), "name" : "Level 1", "description": "Level 1"},
    {"id": id_model.format("Floor", "B1F2"), "name" : "Level 2", "description": "Level 2"},
    {"id": id_model.format("Floor", "B1F3"), "name" : "Level 3", "description": "Level 3"},
    {"id": id_model.format("Floor", "B1F4"), "name" : "Level 4", "description": "Level 4"},
    {"id": id_model.format("Floor", "B1F5"), "name" : "Roof Level", "description": "Roof Level"}]
    
    for etage in floors:
        floor_model = read(models_file)["floors"] # On récupère le modèle JSON d'un étage
        floor_model["id"] = etage["id"] # On lui donne le bon ID
        floor_model["name"]["value"] = etage["name"] # On lui donne le bon nom
        floor_model["description"]["value"] = etage["description"] # On lui donne la bonne description
        add(floors_file, floor_model) # On ajoute cet étage dans le fichier JSON des étages

    building_json = read(models_file)["building"] # On récupère le modèle JSON d'un bâtiment
    building_json["HasFloors"]["object"] = [etage["id"] for etage in floors] # On lui ajoute les id des étages
    write(building_file, building_json) # On l'écrit dans le fichier du bâtiment
    return None



def initialize():
    """Fonction qui réinitialise tous les fichiers JSON et mettre le fichier du bâtiment et des étages à 0"""
    clean([windows_file, doors_file, rooms_file, building_file, floors_file])
    add_floors()
    return None



def clear_cache():
    """Fonction qui vide les fichiers JSON"""
    clean([windows_file, doors_file, rooms_file, building_file, floors_file])



def coordinates(coor):
    """Fonction qui renvoie les quatre points de la pièce à partir :
    du point en bas à gauche
    de la longueur,
    de la largeur:
    coor : [(a, b), length, width] -> 1st point, longueur, largeur
    -> point en bas à gauche, en bas à droite, en haut à gauche, en haut à droite
    """

    a = coor[0][0]
    b = coor[0][1]
    length = coor[1]
    width = coor[2]

    return [(a, b), (a+length, b), (a+length, b+width), (a, b+width)]



def add_room(number : int, typ : str , coor, windows : int, doors : int):
    """Fonction pour ajouter une pièce
    number : le numéro de la chambre
    typ : son type (ex : bureau)
    coor : [(), length, width] (longueur->length largeur->width) : Coordonnées pièce
    windows : le nombre de fenêtre à ajouter
    doors : le nombre de porte à ajouter"""

    id_floor = id_model.format("Floor", "B1F{}".format(floor))

    # Ajouter la pièce
    room_model = read(models_file)["rooms"] # On récupère le modèle JSON d'une pièce
    room_id = id_model.format("Room", "B1F{}R{}".format(floor, number)) # On génère l'ID
    room_model["id"] = room_id # On lui donne le bon ID
    room_model["name"]["value"] = "Room {}".format(number)
    room_model["description"]["value"] = typ
    room_model["onFloor"]["object"] = id_floor
    room_model["relativePosition"]["value"]["coordinates"] = coordinates(coor)

    # Ajouter l'id de la pièce dans le fichier du bâtiment
    building_json = read(building_file) # On récupère le JSON du bâtiment
    building_json["HasRooms"]["object"].append(room_id) # On lui ajoute l'ID de la pièce
    write(building_file, building_json) # On l'écrit dans le fichier du bâtiment

    # Ajouter l'id de la pièce dans le fichier des étages
    floors_json = read(floors_file) # On récupère le JSON des étages
    for floor_json in floors_json:
        if floor_json["id"] == id_floor:
            # On est dans le bon étage
            floor_json["roomsOnFloor"]["object"].append(room_id) # On ajoute l'id de la pièce
            floor_json["numberOfRooms"]["value"] += 1 # On incrément le nombre de pièces reliées
    write(floors_file, floors_json) # On l'écrit dans le fichier des pièces

    id_windows = []
    id_doors = []

    # Ajouter les fenêtres
    for window in range(windows):
        window_model = read(models_file)["windows"] # On récupère le modèle JSON d'une fenêtre
        id = id_model.format("Window", "B1F{}R{}W{}".format(floor, number, window + 1)) # On génère l'ID
        id_windows.append(id) # On ajoute l'id dans la liste des id des fenêtres
        window_model["id"] = id # On lui donne le bon ID
        add(windows_file, window_model) # On ajoute cette fenêtre dans le fichier JSON des fenêtres

    # Ajouter les portes
    for door in range(doors):
        door_model = read(models_file)["doors"] # On récupère le modèle JSON d'une porte
        id = id_model.format("Door", "B1F{}R{}D{}".format(floor, number, door + 1)) # On génère l'ID
        id_doors.append(id) # On ajoute l'id dans la liste des id des portes
        door_model["id"] = id # On lui donne le bon ID
        add(doors_file, door_model) # On ajoute cette porte dans le fichier JSON des portes

    # On ajoute les relations avec les fenêtres et les portes
    room_model["windowsInRoom"]["object"] = id_windows
    room_model["DoorsInRoom"]["object"] = id_doors

    # On ajoute le nombre de fenêtres et de portes
    room_model["numberOfWindows"]["value"] = len(id_windows)
    room_model["numberOfDoors"]["value"] = len(id_doors)
    
    add(rooms_file, room_model) # On ajoute cette pièce dans le fichier JSON des pièces
    return None



def verify_coordinates():
    """Fonction qui vérifie qu'aucune pièce de se chevauche (dû à des erreurs dans les informations entrées)"""
    
    def check_overlap(rect1, rect2):
        """Fonction qui vérifie si les deux rectangles se chevauchent ou non
        rect1 et rect2 sont des listes de quatre tuples représentant les points des rectangles
        Les tuples contiennent les coordonnées (x, y) des points"""

        # Calcul des coordonnées des rectangles
        x1, y1 = zip(*rect1)
        x2, y2 = zip(*rect2)
        min_x1, max_x1 = min(x1), max(x1)
        min_y1, max_y1 = min(y1), max(y1)
        min_x2, max_x2 = min(x2), max(x2)
        min_y2, max_y2 = min(y2), max(y2)

        # Vérification de la collision des rectangles
        if max_x1 <= min_x2 or max_x2 <= min_x1:
            return False
        if max_y1 <= min_y2 or max_y2 <= min_y1:
            return False
        return True


    def check_overlap_all(rectangles):
        """Fonction qui vérifie si tous les rectangles se chevauchent ou non
        rectangles est une liste de listes de quatre tuples représentant les points des rectangles
        Les tuples contiennent les coordonnées (x, y) des points"""

        overlap = set()
        for key1, rect1 in rectangles.items():
            for key2, rect2 in rectangles.items():
                if key1 < key2 and check_overlap(rect1, rect2):
                    overlap.add((key1, key2))
        return overlap


    def get_all_rectangles(floor):
        """Fonction qui récupère la listes des coordoonées des pièces de l'étage floor
        sous la forme d'un dictionnaire associant l'id de la pièce avec ses coordonnées"""

        rooms_json = read(rooms_file)
        rectangles = dict()
        for room in rooms_json:
            id_room = re.search(r':(\w+)$', room["id"]).group(1) # On récupère l'id de la pièce
            floor_room = int(re.search(r'F(\d+)', room["id"]).group(1)) # On récupère l'étage de la pièce

            if floor_room == floor:
                # Si on est sur le bon étage, on récupère les coordonnées
                rectangles[id_room] = room["relativePosition"]["value"]["coordinates"]
        return rectangles
    

    for i in range(2, 3):
        rectangles = get_all_rectangles(i)
        overlap = check_overlap_all(rectangles)
        if overlap == set():
            print("Il n'y a aucun chevauchement dans les pièces du bâtiment")
            return None
        for i, j in overlap:
            print("Les pièces {} et {} se chevauchent".format(i, j))
        return None



def add_floor(filename, the_floor):
    """Ajout un étage à partir d'un fichier contenant les pièces
    room_nb room_name x y longueur largeur windows doors"""
    global floor
    floor = the_floor
    with open(filename, 'r') as f:
        line = f.readline().strip("\n")
        while line != "":
            values = line.split(" ")
            number = int(values[0])
            name = values[1].replace("_", " ")
            coor = [(int(values[2])/100, int(values[3])/100), int(values[4])/100, int(values[5])/100]
            windows = int(values[6])
            doors = int(values[7])
            add_room(number, name, coor, windows, doors)
            line = f.readline().strip("\n")
    verify_coordinates()
    print("le fichier {} a bien été ajouté".format(filename))
    return None



def add_relations(relation_1, relation_2):
    """Ajoute les relations manquantes
    relation_1 : room
    relation_2 : door/window"""
    type_1 = relation_1.split(":")[2]
    assert type_1 == "Room"
    type_2 = relation_2.split(":")[2]
    if type_2 == "Window":
        rooms_json = read(rooms_file) # On récupère le JSON des pièces
        for room_json in rooms_json:
            if room_json["id"] == relation_1:
                # On est dans la bonne pièce
                room_json["windowsInRoom"]["object"].append(relation_2) # On ajoute l'id de la pièce
                room_json["numberOfWindows"]["value"] += 1 # On incrément le nombre de pièces reliées
        write(rooms_file, rooms_json) # On l'écrit dans le fichier des pièces
    elif type_2 == "Door":
        rooms_json = read(rooms_file) # On récupère le JSON des pièces
        for room_json in rooms_json:
            if room_json["id"] == relation_1:
                # On est dans la bonne pièce
                room_json["DoorsInRoom"]["object"].append(relation_2) # On ajoute l'id de la pièce
                room_json["numberOfDoors"]["value"] += 1 # On incrément le nombre de pièces reliées
        write(rooms_file, rooms_json) # On l'écrit dans le fichier des pièces
    return None



def add_relations_floor(filename, the_floor):
    """Ajout des relations à partir d'un fichier
    relation_1 : room
    relation_2 : door/window"""
    global floor
    floor = the_floor
    with open(filename, 'r') as f:
        line = f.readline().strip("\n")
        while line != "":
            values = line.split(" ")
            relation_1 = values[0]
            relation_2 = values[1]
            add_relations(relation_1, relation_2)
            line = f.readline().strip("\n")
    print("les relations {} ont bien été ajouté".format(filename))
    return None



initialize()
add_floor("floor_2.txt", 3)
add_floor("floor_3.txt", 3)
add_floor("floor_4.txt", 3)
add_relations_floor("relation_3.txt", 3)