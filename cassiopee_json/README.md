# cassiopee_json

## The files

autofill.py creates the JSON file with the relations thanks to the text files in json.

>It also adds relations for windows and doors that are in common with 2 rooms!

The files created are in JSON:

* building.json
* floors.json
* rooms.json
* doors.json
* windows.json

## Remplir les étages

chaque étage est un tableau de valeurs :

    [id, nom, coor_bas_gauche, longueur, largeur, windows : [dist, type, mur], doors : [dist, type, mur]]

ex :

    [1, "Laboratoire", [0, 0], 763, 328, [[0, 1, 1], [0, 1, 1]], [[0, 1, 1], [0, 1, 1]]]

![aide pour les longueur/largeur](/cassiopee_json/2d-plans/aide.jpeg)

## Epaisseur des murs

### Mur creux

* Petit : 6,75 cm
* Normal : 13,5 cm

### Mur plein

* Petit : 10,125 cm
* Normal : 13,5 cm
* Grand : 20,25 cm
