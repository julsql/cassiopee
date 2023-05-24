# Generate correct JSON files to represent the Étoile building
import json
import re
import matplotlib.pyplot as plt
import os

path = os.getcwd() + "/"

path_json = path + "json_ld/"
windows_file = path_json + "windows.json" # Windows File
doors_file = path_json + "doors.json" # Doors File
rooms_file = path_json + "rooms.json" # Rooms File
floors_file = path_json + "floors.json" # Floors File
building_file = path_json + "building.json" # Building File
templates_file = path + "templates.json" # JSON Models File

wind_size = [94, 94*2, 288]
door_size = [90, 125.5, 154]
epaisseur = 15

id_model = "urn:ngsi-ld:{0}:SmartCitiesdomain:SmartBuildings:{1}" # model of an id

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



def clean(file_array):
    """Clean the JSON files to an empty array"""

    for file in file_array:
        write(file, [])
    return None



def add(filename, json_array):
    """Add a python dictionary to a JSON file"""

    json_file = read(filename)
    for data in json_file:
        if data["id"] == json_array["id"]:
            # Check the uniqueness of an id
            raise(ValueError("id non unique : {}".format(json_array["id"])))

    json_file.append(json_array)
    write(filename, json_file)
    return None



def add_floors():
    """Add all the empty floors"""

    # Floors data
    floors = [{"id": id_model.format("Floor", "B1F0a"), "name" : "TERRAIN", "description": "TERRAIN"},
    {"id": id_model.format("Floor", "B1F0b"), "name" : "Sub-Structure (foundations)", "description": "Sub-Structure (foundations)"},
    {"id": id_model.format("Floor", "B1F0"), "name" : "Ground Floor", "description": "Ground Floor"},
    {"id": id_model.format("Floor", "B1F1"), "name" : "Level 1", "description": "Level 1"},
    {"id": id_model.format("Floor", "B1F2"), "name" : "Level 2", "description": "Level 2"},
    {"id": id_model.format("Floor", "B1F3"), "name" : "Level 3", "description": "Level 3"},
    {"id": id_model.format("Floor", "B1F4"), "name" : "Level 4", "description": "Level 4"},
    {"id": id_model.format("Floor", "B1F5"), "name" : "Roof Level", "description": "Roof Level"}]
    
    for floor in floors:
        floor_model = read(templates_file)["floors"] # Get floor JSON template
        floor_model["id"] = floor["id"] # Give the id
        floor_model["name"]["value"] = floor["name"] # Give the name
        floor_model["description"]["value"] = floor["description"] # Give the description
        add(floors_file, floor_model) # Add this floor in the floors file

    building_json = read(templates_file)["building"] # Get building template
    building_json["HasFloors"]["object"] = [floor["id"] for floor in floors] # Add floor id
    write(building_file, building_json) # Write in the building file
    return None



def initialize():
    """Initialize JSON files and set building and floor file"""
    clean([windows_file, doors_file, rooms_file, building_file, floors_file])
    add_floors()
    return None



def clear_cache():
    """Empty all the JSON files"""
    clean([windows_file, doors_file, rooms_file, building_file, floors_file])
    return None



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

    return [z1, z2, z3, z4, z1]



def coordinates_obj(coor_obj, coor_room, obj):
    """Give the 4 points of an object given:
    value, type of the windows and wich wall
    and the coordinates of the room
    val match with type : val_windows = {1 : 3.5, 2 : 4.5, 3 : 5.5}
    coor_wind : [a, type, wall]
    coor_room : [(x, y), length, width] -> 1st point, length, width
    return coordinates of the object
    """
    err = 1
    a = int(coor_obj[0])
    type = int(coor_obj[1])
    wall = int(coor_obj[2])

    x = int(coor_room[0][0])
    y = int(coor_room[0][1])
    length = int(coor_room[1])
    width = int(coor_room[2])

    if obj == "window":
        val = wind_size
    elif obj == "door":
        val = door_size
    else:
        raise TypeError(obj + "n'est ni door ni window")

    # wall = 0 : mur gauche
    # wall = 1 : mur haut
    # wall = 2 : mur droit
    # wall = 3 : mur bas

    # type = 0 : petit fenêtre
    # type = 1 : double fenêtre
    # type = 2 : triple fenêtre

    l = val[type]

    if wall == 0:
        z1 = ((x + a)/100, (y - epaisseur)/100)
        z2 = ((x + a)/100, (y + err)/100)
        z3 = ((x + a + l)/100, (y + err)/100)
        z4 = ((x + a + l)/100, (y - epaisseur)/100)

    if wall == 1:
        z1 = ((x + length - err)/100, (y + a)/100)
        z2 = ((x + length + epaisseur)/100, (y + a)/100)
        z3 = ((x + length + epaisseur)/100, (y + a + l)/100)
        z4 = ((x + length - err)/100, (y + a + l)/100)

    if wall == 2:
        z1 = ((x + a)/100, (y + width - err)/100)
        z2 = ((x + a)/100, (y + width + epaisseur)/100)
        z3 = ((x + a + l)/100, (y + width + epaisseur)/100)
        z4 = ((x + a + l)/100, (y + width - err)/100)

    if wall == 3:
        z1 = ((x - epaisseur)/100, (y + a)/100)
        z2 = ((x + err)/100, (y + a)/100)
        z3 = ((x + err)/100, (y + a + l)/100)
        z4 = ((x - epaisseur)/100, (y + a + l)/100)

    return [z1, z2, z3, z4, z1]



def add_room(number : int, typ : str , coor, windows, doors, floor : int):
    """Add a room
    number : room number
    typ : room type (ex: bureau)
    coor : [(), length, width] (longueur->length largeur->width) : Room coordinates
    windows : windows charac for each window
    doors : doors charac for each door"""

    id_floor = id_model.format("Floor", "B1F{}".format(floor))

    # Add the room
    room_model = read(templates_file)["rooms"] # Get JSON room template
    room_id = id_model.format("Room", "B1F{}R{}".format(floor, number)) # Generate the id
    room_model["id"] = room_id # Give the id
    room_model["name"]["value"] = "Room {}".format(number)
    room_model["description"]["value"] = typ
    room_model["onFloor"]["object"] = id_floor
    room_model["relativePosition"]["value"]["coordinates"] = coordinates_room(coor)

    # Add room id in the building file
    building_json = read(building_file) # Get JSON building template
    building_json["HasRooms"]["object"].append(room_id) # Add the room id
    write(building_file, building_json) # Write in the building JSON file

    # Add room id in the building floor file
    floors_json = read(floors_file) # Get floor JSON
    for floor_json in floors_json:
        if floor_json["id"] == id_floor:
            # In the write floor
            floor_json["roomsOnFloor"]["object"].append(room_id) # Add room id
            floor_json["numberOfRooms"]["value"] += 1 # Increment room associate number
    write(floors_file, floors_json) # Write in the rooms file

    id_windows = []
    id_doors = []

    # Add the windows
    for i in range(len(windows)):
        window = windows[i]
        window_model = read(templates_file)["windows"] # Get JSON windows template
        id = id_model.format("Window", "B1F{}R{}W{}".format(floor, number, i + 1)) # Generate id
        id_windows.append(id) # Add id in windows list
        window_model["id"] = id # Give id
        coor_wind = coordinates_obj(window, coor, "window")
        window_model["relativePosition"]["value"]["coordinates"] = coor_wind
        add(windows_file, window_model) # Add window in the windows JSON file

    # Add the doors
    for i in range(len(doors)):
        door = doors[i]
        door_model = read(templates_file)["doors"] # Get JSON windows template
        id = id_model.format("Door", "B1F{}R{}D{}".format(floor, number, i + 1)) # Generate id
        id_doors.append(id) # Add id in windows list
        door_model["id"] = id # Give id
        coor_door = coordinates_obj(door, coor, "door")
        door_model["relativePosition"]["value"]["coordinates"] = coor_door
        add(doors_file, door_model) # Add window in the windows JSON file

    # Add the relation between rooms and windows/doors
    room_model["windowsInRoom"]["object"] = id_windows
    room_model["DoorsInRoom"]["object"] = id_doors

    # Add number of windows/doors
    room_model["numberOfWindows"]["value"] = len(id_windows)
    room_model["numberOfDoors"]["value"] = len(id_doors)
    
    add(rooms_file, room_model) # Add the room into room json file
    return None


def verify_coordinates():
    """Fonction qui vérifie qu'aucune pièce de l'étage ne se chevauche (dû à des erreurs dans les informations entrées)"""
    

    def afficher(rectangles, titre):
        """Affiche des rectangles sur un graphe
        Coordonées sous la forme
        [rect1, rect2, …]
        avec rect = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]"""

        fig, ax = plt.subplots()

        for key1, rect1 in rectangles.items():
            color = "gray"
            if "W" in key1:
                color = "blue"
            elif "D" in key1:
                color = "red"

            try:
                x = [rect1[i][0] for i in range(5)]
                y = [-rect1[i][1] for i in range(5)]

                # Ajout des rectangles à l'axe
                ax.plot(x, y, color=color)#, label=key1)
            except:
                None

        # L'axe x et y sont identiques
        #ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
        ax.set_aspect('equal')
        ax.set_title(titre)

        #fig.subplots_adjust(left=0.1, right=0.78)
        # Affichage de la figure
        plt.show()


    def check_overlap(rect1, rect2):
        """Fonction qui vérifie si les deux rectangles se chevauchent ou non
        rect1 et rect2 sont des listes de quatre tuples représentant les points des rectangles
        Les tuples contiennent les coordonnées (x, y) des points"""

        # Calculate rectangles coordinates
        x1, y1 = zip(*rect1)
        x2, y2 = zip(*rect2)
        min_x1, max_x1 = min(x1), max(x1)
        min_y1, max_y1 = min(y1), max(y1)
        min_x2, max_x2 = min(x2), max(x2)
        min_y2, max_y2 = min(y2), max(y2)

        # Check rectangles collisions
        if max_x1 <= min_x2 or max_x2 <= min_x1:
            return False
        if max_y1 <= min_y2 or max_y2 <= min_y1:
            return False
        return True


    def check_overlap_all(rooms):
        """Check the overlapping of the rooms
        rooms: list of 4 tuples representing the 4 corner of the rectangle
        tuple: coordinates of the points: (x, y)"""

        overlap = set()
        for key1, rect1 in rooms.items():
            for key2, rect2 in rooms.items():
                if key1 < key2 and check_overlap(rect1, rect2):
                    overlap.add((key1, key2))
        return overlap
    
    def ajout_relation(winds, rooms):
        """Check the overlapping of the rooms
        rooms: list of 4 tuples representing the 4 corner of the rectangle
        tuple: coordinates of the points: (x, y)"""

        overlap = set()
        for key1, rect1 in winds.items():
            for key2, rect2 in rooms.items():
                if check_overlap(rect1, rect2):
                    overlap.add((key1, key2))
        return overlap


    def get_all_rectangles(floor):
        """Get the list of the rooms coordinates of the floor
        in a dictionary where the key is the room id and the value its coordinates"""

        rooms_json = read(rooms_file)
        winds_json = read(windows_file)
        doors_json = read(doors_file)
        rooms = dict()
        doors = dict()
        winds = dict()
        affichage = dict()
        for room in rooms_json:
            id_room = re.search(r':(\w+)$', room["id"]).group(1) # Get room id
            floor_room = int(re.search(r'F(\d+)', room["id"]).group(1)) # get room floor id

            if floor_room == floor:
                # If write floor: get coordinates
                rooms[id_room] = room["relativePosition"]["value"]["coordinates"]
                affichage[id_room] = room["relativePosition"]["value"]["coordinates"]
                for windid in room["windowsInRoom"]["object"]:
                    for wind in winds_json:
                        if wind["id"] == windid:
                            id_wind = re.search(r':(\w+)$', windid).group(1) # Get room id
                            winds[id_wind] = wind["relativePosition"]["value"]["coordinates"]
                            affichage[id_wind] = wind["relativePosition"]["value"]["coordinates"]
                for doorid in room["DoorsInRoom"]["object"]:
                    for door in doors_json:
                        if door["id"] == doorid:
                            id_door = re.search(r':(\w+)$', doorid).group(1) # Get room id
                            doors[id_door] = door["relativePosition"]["value"]["coordinates"]
                            affichage[id_door] = door["relativePosition"]["value"]["coordinates"]

        afficher(affichage, "Étage {}".format(floor))
        return rooms, winds, doors
    
    for flr in range(1, 3):

        rooms, winds, doors = get_all_rectangles(flr)
        overlap = check_overlap_all(rooms)
        if overlap == set():
            print("Il n'y a aucun chevauchement dans les pièces de l'étage {}".format(flr))
        for i, j in overlap:
            # afficher({i: rooms[i], j: rooms[j]}, "Pièce n°{} et {}".format(i, j))
            print("Les pièces {} et {} se chevauchent".format(i, j))
        
        relation = ajout_relation(winds, rooms)
        if relation == set():
            print("Il n'y a aucune relation à ajouter dans les pièces et les fenêtres de l'étage {}".format(flr))
        for i, j in relation:
            wind = "urn:ngsi-ld:Window:SmartCitiesdomain:SmartBuildings:" + i
            room = "urn:ngsi-ld:Room:SmartCitiesdomain:SmartBuildings:" + j
            add_relations(room, wind)

        relation = ajout_relation(doors, rooms)
        if relation == set():
            print("Il n'y a aucune relation à ajouter dans les pièces et les portes de l'étage {}".format(flr))
        for i, j in relation:
            door = "urn:ngsi-ld:Door:SmartCitiesdomain:SmartBuildings:" + i
            room = "urn:ngsi-ld:Room:SmartCitiesdomain:SmartBuildings:" + j
            add_relations(room, door)

        print()
    return None



def add_floor(filename, floor):
    """Add a floor from a file containing the rooms:
    room_nb room_name x y longueur largeur windows doors"""
    data = read(filename)
    for room in data:
        number = int(room[0])
        name = room[1].replace("_", " ")
        coor = [(room[2][0], room[2][1]), room[3], room[4]]
        windows = room[5]
        doors = room[6]
        add_room(number, name, coor, windows, doors, floor)

    print("le fichier {} a bien été ajouté".format(filename))
    return None



def add_relations(relation_1, relation_2):
    """Add the missing relations
    relation_1 : room
    relation_2 : door/window"""
    # get the objects type
    type_1 = relation_1.split(":")[2]
    assert type_1 == "Room" # First id must be a room
    type_2 = relation_2.split(":")[2]
    if type_2 == "Window":
        rooms_json = read(rooms_file) # Get the rooms JSON file
        for room_json in rooms_json:
            if room_json["id"] == relation_1:
                # Right room
                if relation_2 not in room_json["windowsInRoom"]["object"]:
                    print("La fenêtre {} est également dans la pièce {}".format(relation_2.split(":")[-1], relation_1.split(":")[-1]))
                    room_json["windowsInRoom"]["object"].append(relation_2) # Add windows id
                    room_json["numberOfWindows"]["value"] += 1 # Increment related windows number
        write(rooms_file, rooms_json) # Write in the JSON rooms file
    elif type_2 == "Door":
        rooms_json = read(rooms_file) # Get the rooms JSON file
        for room_json in rooms_json:
            if room_json["id"] == relation_1:
                # Right room
                if relation_2 not in room_json["DoorsInRoom"]["object"]:
                    print("La porte {} est également dans la pièce {}".format(relation_2.split(":")[-1], relation_1.split(":")[-1]))
                    room_json["DoorsInRoom"]["object"].append(relation_2) # Add doors id
                    room_json["numberOfDoors"]["value"] += 1 # Increment related doors number
        write(rooms_file, rooms_json) # Write in the JSON rooms file
    return None

def additional_doors(filename):
    add_door = read(filename)
    doors = read(doors_file)
    rooms = read(rooms_file)
    for door in add_door:
        door_template = read(templates_file)["doors"]
        id_room = id_model.format("Room", f"B1F{door[0]}R{door[1]}")
        id_door = id_model.format("Door", f"B1F{door[0]}R{door[1]}D1")
        door_model = door_template
        door_model['id'] =  id_door
        a = door[2][0]
        b = door[2][1]
        l = door_size[door[3]]
        
        if door[4] == 0:
            door_model['relativePosition']['value']['coordinates'] = [
                [a/100, b/100],
                [int(a+epaisseur)/100, b/100],
                [int(a+epaisseur)/100, int(b+l)/100],
                [a/100, int(b+l)/100],
                [a/100, b/100],
                ]
        else:
            door_model['relativePosition']['value']['coordinates'] = [
                [a/100, b/100],
                [int(a+l)/100, b/100],
                [int(a+l)/100, int(b+epaisseur)/100],
                [a/100, int(b+epaisseur)/100],
                [a/100, b/100],
                ]

        doors.append(door_model)

        for i in range(len(rooms)):
            if rooms[i]['id'] == id_room:
                print(id_room)
                rooms[i]['DoorsInRoom']['object'].append(door_model['id'])
                rooms[i]['numberOfDoors']["value"] += 1

    write(doors_file, doors)
    write(rooms_file, rooms)



initialize() # Empty JSON files

#add_floor(path + "json_hand/floor_0.json", 0)
add_floor(path + "json_hand/floor_1.json", 1)
add_floor(path + "json_hand/floor_2.json", 2)
add_floor(path + "json_hand/floor_3.json", 3)
add_floor(path + "json_hand/floor_4.json", 4)


additional_doors(path + "json_hand/doors.json")

print()
verify_coordinates() # Check if rooms don't overlap