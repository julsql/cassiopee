# cassiopee_json

Help to fullfil the json file of the building. Different steps.

## Fullfil the floors

In the folder [json_hand](json_hand) fullfil the files of the floors. It's a json array with each rooms of the floors. The informations are taken from the [floor plans](/cassiopee_json/2d-plans/B%C3%A2timent%20%C3%89toile.pdf).

[id, name, bottom left coordinate: [x, y], length, width, windows, doors]

windows/doors: array of all the windows/doors in the rooms
[distance, type, wall]

* wall is on wich wall is the windows/doors (0: left wall, 1: upper wall, 2: right wall, 3: bottom wall)
* type is the length (0: simple, 2: double, 3: triple)
* distance is the distance from the left wall if the windows/doors is on a vertical wall and distance from the bottom wall if the wall is horizontal (see the map of the building).

ex :

    [1, "Laboratoire", [0, 0], 763, 328, [[0, 1, 1], [0, 1, 1]], [[0, 1, 1], [0, 1, 1]]]

Warning: consider the thickness of the wall in the coordinates of the windows. If a window/door is in two rooms, add it to only one room.

![aide pour les longueur/largeur](/cassiopee_json/2d-plans/aide.jpeg)

Some doors are not connected to a wall, they can be added in the file [doors.json](json_hand/doors.json)
[floor, room_id, bottom-left coordinates: [x, y], type, wall]

## The files

Once the json_hand file is fullfiled, run [autofil.py](/cassiopee_json/autofill.py).

autofill.py creates the JSON file with the relations thanks to the text files in json.

It use templates.json to formalize the json-ld fils.

>It also adds relations for windows and doors that are in common with 2 rooms!

The files created are in JSON:

* building.json
* floors.json
* rooms.json
* doors.json
* windows.json

## The trimesh

Once the 2D json-ld files created, run totrimesh.py. It will create json_trimesh file (same as before but with the coordinates in trimesh) and the objects file .obj of each floors, separating rooms, doors and windows add adding colors. These files will be used in the Flutter app.

## Measures

### Large Window

* Height: 177cm
* Width: 190cm
* Height under window: 81cm
* Wall thickness: 10cm

### Small window

* Height: 177cm
* Width: 94cm

### Triple window

* Width: 288cm

### Ceiling height

* 363cm

## Wall

* Wall 1: 10cm
* Wall 2: 14cm
* Toilet wall: 7.5cm

### Door

* Height: 204cm
* Width: 90cm

### Hallway cupboard

* width: 102cm
* height: 206cm