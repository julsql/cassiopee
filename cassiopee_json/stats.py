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


def read(filename):
    """Convert a JSON file in a python dictionary"""

    with open(filename, "r") as f:
        data = json.load(f)
    return data


def affiche(nom, file):
    print(f"Il y a {len(read(file))} {nom}")

affiche("pièces", rooms_file)
affiche("portes", doors_file)
affiche("fenêtres", windows_file)