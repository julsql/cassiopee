# Génère des fichiers JSON corrects pour représenter le bâtiment étoile
import json

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
    # Ajouter vérification id
    for data in json_file:
        if data["id"] == json_array["id"]:
            raise(ValueError("id non unique : {}".format(json_array["id"])))

    json_file.append(json_array)
    write(filename, json_file)
    return None



def add_floors():
    """Ajouter tous les étages"""

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


def coordinates(coor):
    """Renvoie les quatre points de la pièce à partir :
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

    return [(a, b), (a+length, b), (a+width, b), (a+width, b+length)]



def add_room(number : int, typ : str , coor, windows : int, doors : int):
    """Fonction pour ajouter une pièce
    number : le numéro de la chambre
    typ : son type (ex : bureau)
    coor : [(), length, width] (longueur->length largeur->width) : Coordonnées pièce
    windows : le nombre de fenêtre à ajouter
    doors : le nombre de porte à ajouter"""

    id_floor = id_model.format("Room", "B1F{}".format(floor))

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



clean([windows_file, doors_file, rooms_file, building_file, floors_file])
# add_floors()
# add_room(1, "Laboratoire", [(0, 0), 10, 5], 3, 2)
# add_room(2, "Serveur", 1, 3)
# add_room(3, "Closet", 0, 1)