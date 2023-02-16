# Génère des fichiers JSON corrects pour représenter le bâtiment étoile

floor = 2 # Étage dans lequel on ajoute les pièces

windows_file = "windows.json" # Fichier des fenêtres du bâtiment
doors_file = "doors.json" # Fichier des portes du bâtiment
rooms_file = "rooms.json" # Fichier des pièces du bâtiment
list_rooms_id = "rooms_id_{}.txt".format(floor) # Fichier de la liste des pièces ajoutées (pour l'ajouter dans les relations du l'étage)

id_floors = ["urn:ngsi-ld:Floor:Test:SmartCitiesdomain:SmartBuildings:3RyjwofOz3vvsZpar0bnNE", 
"urn:ngsi-ld:Floor:Test:SmartCitiesdomain:SmartBuildings:3UJUMM1bDCBgmCqkHMEXhC", 
"urn:ngsi-ld:Floor:Test:SmartCitiesdomain:SmartBuildings:0qhLuYaYTFh9RfDz4_Uz0J", 
"urn:ngsi-ld:Floor:Test:SmartCitiesdomain:SmartBuildings:1UvglCkzrEARla$C$lIgDX", 
"urn:ngsi-ld:Floor:Test:SmartCitiesdomain:SmartBuildings:0znMx7WDj4_PU8mJxrfoof"] # ID des étage (0 -> Rez de Chaussée, 1 -> 1er étage…)
id_room_model = "urn:ngsi-ld:Room:Test:SmartCitiesdomain:SmartBuildings:" # Modèle de l'ID des pièces
id_door_model = "urn:ngsi-ld:Door:Test:SmartCitiesdomain:SmartBuildings:" # Modèle de l'ID des portes
id_window_model = "urn:ngsi-ld:Window:Test:SmartCitiesdomain:SmartBuildings:" # Modèle de l'ID des fenêtres

wind_model = """,
    {
        "id": "ID_WIND",
        "type": "Window",
        "relativePosition": {
            "type": "Property",
            "value": {
                "type": "Trimesh",
                "measurementUnit": "m",
                "Dimensions": "3D",
                "coordinates": [
                    [
                        0,
                        0
                    ]
                ],
                "faces": [
                    [
                        0,
                        0
                    ]
                ]
            }
        },
        "@context": [
            "https://gitlab.isl.ics.forth.gr/api/v4/projects/82/repository/files/ngsild-models%2FBuilding%2Fcontext.json/raw",
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
        ]
    }""" # Modèle JSON d'une fenêtre dans la spécification
door_model = """,
    {
        "id": "ID_DOOR",
        "type": "Door",
        "relativePosition": {
            "type": "Property",
            "value": {
                "type": "Trimesh",
                "measurementUnit": "m",
                "Dimensions": "3D",
                "coordinates": [
                    [
                        0,
                        0
                    ]
                ],
                "faces": [
                    [
                        0,
                        0
                    ]
                ]
            }
        },
        "@context": [
            "https://gitlab.isl.ics.forth.gr/api/v4/projects/82/repository/files/ngsild-models%2FBuilding%2Fcontext.json/raw",
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
        ]
    }
    """ # Modèle JSON d'une porte dans la spécification
room_model = """,
    {
        "id": "ID_ROOM",
        "type": "Room",
        "name": {
            "type": "Property",
            "value": "NAME_ROOM"
        },
        "description": {
            "type": "Property",
            "value": "TYPE_ROOM"
        },
        "onFloor": {
            "type": "Relationship",
            "object": "ID_FLOOR"
        },
        "relativePosition": {
            "type": "Property",
            "value": {
                "type": "Trimesh",
                "measurementUnit": "m",
                "Dimensions": "3D",
                "coordinates": [
                    [
                        0,
                        0
                    ]
                ],
                "faces": [
                    [
                        0,
                        0
                    ]
                ]
            }
        },
        "DoorsInRoom": {
            "type": "Relationship",
            "object": [
                ID_DOORS
            ]
        },
        "windowsInRoom": {
            "type": "Relationship",
            "object": [
                ID_WINDOWS
            ]
        },
        "numberOfDoors": {
            "type": "Property",
            "value": NB_DOORS
        },
        "numberOfWindows": {
            "type": "Property",
            "value": NB_WINDOWS
        },
        "@context": [
            "https://gitlab.isl.ics.forth.gr/api/v4/projects/82/repository/files/ngsild-models%2FBuilding%2Fcontext.json/raw",
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
        ]
    }
""" # Modèle JSON d'une pièce dans la spécification


def write(filename, text):
    """Fonction pour écrire un texte dans un fichier"""
    if filename[-5:] == ".json":
        # Si on écrit dans un fichier JSON, on vérifie qu'il est valide
        with open(filename, 'r') as f:
            result = f.read()
        if not "[" in result:
            # Si le fichier JSON est vide (ie. il n'y a pas d'ouverture de [])
            # On enlève la virgule au début des valeurs à ajouter, s'il y en a bien une
            if text[0] == "," :
                text = """[
                """ + text[1:]
            else :
                text = """[
                """ + text
            
        if len(result) > 0 and result[-1] == "]":
            # Si le fichier était fermé (ie. il fini par ])
            # On réécrit le fichier en enlevant ce caractère pour pouvoir ajouter nos valeurs
            with open(filename, 'w') as f:
                f.write(result[:-1])

    # On ajoute au fichier (modifié ou non) les valeur (que ce soit un fichier JSON ou autre)
    with open(filename, 'a') as f:
        f.write(text)

def close(filenames):
    """Fonction pour fermer un fichier JSON (ie. on ajoute ] à la fin)"""
    for filename in filenames:
        write(filename, "]")

def clean(filenames):
    """Fonction pour vider completement un fichier"""
    for filename in filenames:
        with open(filename, "w") as f:
            f.write("")

def room(number : int, typ : str , windows : int, doors : int):
    """Fonction pour ajouter une chambre
    number : le numéro de la chambre
    typ : son type (ex : bureau)
    windows : le nombre de fenêtre à ajouter
    doors : le nombre de porte à ajouter"""

    id_windows = "" # Liste des id des fenêtres pour l'ajouter dans les relations de la pièces
    id_doors = "" # Liste des id des portes pour l'ajouter dans les relations de la pièces
    id_floor = id_floors[floor] # Choix du bon id de l'étage

    for window in range(windows):
        # On ajoute au fichier JSON des fenêtres chaque fenêtre, on sauvegarde son id
        id_window = id_window_model + "B1F{}R{}W{}".format(floor, number, window + 1) # id de la fenêtre
        id_windows += '"' + id_window + '",\n' # Sauvegarde de l'ID
        write(windows_file, wind_model.replace("ID_WIND", id_window)) # Écriture dans le fichier JSON des fenêtres

    for door in range(doors):
        # On ajoute au fichier JSON des portes chaque porte, on sauvegarde son id
        id_door = id_door_model + "B1F{}R{}D{}".format(floor, number, door + 1)
        id_doors += '"' + id_door + '",\n'
        write(doors_file, door_model.replace("ID_DOOR", id_door))

    # On enlève les derniers caractères des id : ,\n
    if len(id_windows) > 0 and id_windows[-2:] == ",\n":
        id_windows = id_windows[:-2]
    if len(id_doors) > 0 and id_doors[-2:] == ",\n":
        id_doors = id_doors[:-2]

    # On ajoute la pièce dans le fichier JSON avec les bonnes valeurs
    id_room = id_room_model + "B1F{}R{}".format(floor, number)
    room_to_write = room_model.replace("ID_ROOM", id_room).replace("NAME_ROOM", "Room " + str(number)).replace("TYPE_ROOM", typ).replace("ID_FLOOR", id_floor)
    room_to_write = room_to_write.replace("ID_DOORS", id_doors).replace("ID_WINDOWS", id_windows).replace("NB_DOORS", str(doors)).replace("NB_WINDOWS", str(windows))

    write(rooms_file, room_to_write) # On écrit dans le fichier JSON des pièces
    write(list_rooms_id, '"' + id_room + '",\n') # On ajout l'id de la pièce pour l'ajouter manuellement dans les relations des étages

clean([windows_file, doors_file, rooms_file, list_rooms_id])

room(1, "Laboratoire", 3, 2)
room(2, "Serveur", 1, 3)
room(3, "Closet", 0, 1)

close([windows_file, doors_file, rooms_file])


# clean([windows_file, doors_file, rooms_file, list_rooms_id])