import json
import os

path = os.getcwd() + "/json_hand/"

coef = 5

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



def convert(coordinates_json, coef):
    """Convert a json file of room&windows coordinates for the value mesured on the map to the real value"""
    for i in range(len(coordinates_json)):
        for j in range(len(coordinates_json[i])):
            for k in range(len(coordinates_json[i][j])):
                coordinates_json[i][j][k][0] = coordinates_json[i][j][k][0]*coef
    return coordinates_json



def add(coordinates_file, floor_file):
    """take the file with musured values and convert & add them to the floor file"""

    coordinates_json = read(coordinates_file)
    floor_json = read(floor_file)
    coef = coordinates_json[0]/coordinates_json[1]

    coordinates_json = convert(coordinates_json[2:], coef)
    for i in range(min(len(coordinates_json), len(floor_json))):

        floor_json[i][5] = coordinates_json[i][0]
        floor_json[i][6] = coordinates_json[i][1]
    write(floor_file, floor_json)

add(path + "coordinates_1.json", path + "floor_1.json")
#add(path + "coordinates_2.json", path + "floor_2.json")