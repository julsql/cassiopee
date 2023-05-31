import os
import json

path = os.getcwd() + "/json_hand/"

old_file = path + "floor_0b.json"
new_file = path + "floor_0.json"

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

def rotation(old_file, new_file):
    old_json = read(old_file)
    line = len(old_json)
    for i in range(line):
        x = old_json[i][2][0]
        y = old_json[i][2][1]
        long = old_json[i][3]
        larg = old_json[i][4]
        old_json[i][2][0] = abs(y-5563+larg)
        old_json[i][2][1] = x # ok
        old_json[i][3] = larg # ok
        old_json[i][4] = long # ok
    write(new_file, old_json)

rotation(old_file, new_file)