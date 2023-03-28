# Generate correct JSON files to represent the Étoile building
import json
import re
import matplotlib.pyplot as plt

path = "/Users/juliettedebono/Documents/TSP/Cassioppée/cassiopee/cassiopee_json/"
path = ""
path_json = path + "json/"
windows_file = path_json + "windows.json" # Windows File
doors_file = path_json + "doors.json" # Doors File
rooms_file = path_json + "rooms.json" # Rooms File
floors_file = path_json + "floors.json" # Floors File
building_file = path_json + "building.json" # Building File
templates_file = path + "templates.json" # JSON Models File

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



def coordinates(coor):
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



def add_room(number : int, typ : str , coor, windows : int, doors : int, floor):
    """Add a room
    number : room number
    typ : room type (ex: bureau)
    coor : [(), length, width] (longueur->length largeur->width) : Room coordinates
    windows : windows number
    doors : doors number"""

    id_floor = id_model.format("Floor", "B1F{}".format(floor))

    # Add the room
    room_model = read(templates_file)["rooms"] # Get JSON room template
    room_id = id_model.format("Room", "B1F{}R{}".format(floor, number)) # Generate the id
    room_model["id"] = room_id # Give the id
    room_model["name"]["value"] = "Room {}".format(number)
    room_model["description"]["value"] = typ
    room_model["onFloor"]["object"] = id_floor
    room_model["relativePosition"]["value"]["coordinates"] = coordinates(coor)

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
    for window in range(windows):
        window_model = read(templates_file)["windows"] # Get JSON windows template
        id = id_model.format("Window", "B1F{}R{}W{}".format(floor, number, window + 1)) # Generate id
        id_windows.append(id) # Add id in windows list
        window_model["id"] = id # Give id
        add(windows_file, window_model) # Add window in the windows JSON file

    # Add the doors
    for door in range(doors):
        door_model = read(templates_file)["doors"] # Get JSON doors template
        id = id_model.format("Door", "B1F{}R{}D{}".format(floor, number, door + 1)) # Generate id
        id_doors.append(id) # Add id in doors list
        door_model["id"] = id # Give id
        add(doors_file, door_model) # Add door in the doors JSON file

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

            try:
                x = [rect1[i][0] for i in range(5)]
                y = [-rect1[i][1] for i in range(5)]

                # Ajout des rectangles à l'axe
                ax.plot(x, y, label=key1)
            except:
                None

        # L'axe x et y sont identiques
        ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
        ax.set_aspect('equal')
        ax.set_title(titre)

        fig.subplots_adjust(left=0.1, right=0.78)
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


    def check_overlap_all(rectangles):
        """Check the overlapping of the rectangles
        rectangles: list of 4 tuples representing the 4 corner of the rectangle
        tuple: coordinates of the points: (x, y)"""

        overlap = set()
        for key1, rect1 in rectangles.items():
            for key2, rect2 in rectangles.items():
                if key1 < key2 and check_overlap(rect1, rect2):
                    overlap.add((key1, key2))
        return overlap


    def get_all_rectangles(floor):
        """Get the list of the rooms coordinates of the floor
        in a dictionary where the key is the room id and the value its coordinates"""

        rooms_json = read(rooms_file)
        rectangles = dict()
        affichage = []
        for room in rooms_json:
            id_room = re.search(r':(\w+)$', room["id"]).group(1) # Get room id
            floor_room = int(re.search(r'F(\d+)', room["id"]).group(1)) # get room floor id

            if floor_room == floor:
                # If write floor: get coordinates
                rectangles[id_room] = room["relativePosition"]["value"]["coordinates"]
                affichage.append(room["relativePosition"]["value"]["coordinates"])
        afficher(rectangles, "Étage {}".format(floor))
        return rectangles
    
    for flr in range(1,5):

        rectangles = get_all_rectangles(flr)
        overlap = check_overlap_all(rectangles)
        if overlap == set():
            print("Il n'y a aucun chevauchement dans les pièces de l'étage {}".format(flr))
        for i, j in overlap:
            afficher({i: rectangles[i], j: rectangles[j]}, "Pièce n°{} et {}".format(i, j))
            print("Les pièces {} et {} se chevauchent".format(i, j))
        print()
    return None



def add_floor(filename, floor):
    """Add a floor from a file containing the rooms:
    room_nb room_name x y longueur largeur windows doors"""

    with open(filename, 'r') as f:
        # Read à floor txt file
        f.readline() # First line useless
        line = f.readline().strip("\n")
        while line != "":
            # Get line value
            values = line.split(" ")
            number = int(values[0])
            name = values[1].replace("_", " ")
            coor = [(values[2], values[3]), values[4], values[5]]
            windows = int(values[6])
            doors = int(values[7])
            # Add the room in the JSON room file from the given values
            add_room(number, name, coor, windows, doors, floor)
            line = f.readline().strip("\n")
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
                room_json["windowsInRoom"]["object"].append(relation_2) # Add windows id
                room_json["numberOfWindows"]["value"] += 1 # Increment related windows number
        write(rooms_file, rooms_json) # Write in the JSON rooms file
    elif type_2 == "Door":
        rooms_json = read(rooms_file) # Get the rooms JSON file
        for room_json in rooms_json:
            if room_json["id"] == relation_1:
                # Right room
                room_json["DoorsInRoom"]["object"].append(relation_2) # Add doors id
                room_json["numberOfDoors"]["value"] += 1 # Increment related doors number
        write(rooms_file, rooms_json) # Write in the JSON rooms file
    return None



def add_relations_floor(filename):
    """Add the relations from a file
    relation_1 : room
    relation_2 : door/window"""
    with open(filename, 'r') as f:
        # Read a file txt floor relations
        f.readline()
        line = f.readline().strip("\n")
        while line != "":
            # Get the line values
            values = line.split(" ")
            relation_1 = values[0]
            relation_2 = values[1]
            # Add the relations the the JSON files
            add_relations(relation_1, relation_2)
            line = f.readline().strip("\n")
    print("les relations {} ont bien été ajouté".format(filename))
    return None



initialize() # Empty JSON files

add_floor(path + "txt/floor_1.txt", 2)
add_floor(path + "txt/floor_2.txt", 2)
add_floor(path + "txt/floor_3.txt", 3)
add_floor(path + "txt/floor_4.txt", 4)
add_relations_floor(path + "txt/relation_1.txt")
add_relations_floor(path + "txt/relation_2.txt")
add_relations_floor(path + "txt/relation_3.txt")
add_relations_floor(path + "txt/relation_4.txt")

print()
verify_coordinates() # Check if rooms don't overlap