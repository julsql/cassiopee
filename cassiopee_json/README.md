# cassiopee_json

## Remplir les étages

Pour remplir les fenêtres et les portes, aller dans coordinates_1.json (1=numéro étage)
et remplir les valeurs MESURÉES À LA RÈGLE comme ça :
    [
        ref,
        mesure,
        [[fenêtre1, fenêtre2, fenêtre3], [porte1, porte2]],
        …
    ]

avec fenêtre1 = [distance, type, mur]…

exemple :
    [
        4,
        4,
        [[[111 , 0, 3],[74, 1, 0],[23, 1, 0]],[[46, 0, 2]]],
        [[[0, 0, 0],[204, 0, 0]],[[18.5, 0, 2]]],
        [[[0, 1, 0],[408, 0, 0]],[[18.5, 0, 2]]]
    ]

chaque étage est un tableau de valeurs :

    [id, nom, coin_bas_gauche, longueur, largeur, windows : [dist, type, mur], doors : [dist, type, mur]]

ex :

    [1, "Laboratoire", [0, 0], 763, 328, [[0, 1, 1], [0, 1, 1]], [[0, 1, 1], [0, 1, 1]]]

Attention à prendre en compte l'épaisseur des murs : 13,5cm (l'ajouter quand vous mettez les coordoonées de la pièce)

![aide pour les longueur/largeur](/cassiopee_json/2d-plans/aide.jpeg)

## The files

autofill.py creates the JSON file with the relations thanks to the text files in json.

>It also adds relations for windows and doors that are in common with 2 rooms!

The files created are in JSON:

* building.json
* floors.json
* rooms.json
* doors.json
* windows.json

## Epaisseur des murs

### Mur creux

* Petit : 6,75 cm
* Normal : 13,5 cm

### Mur plein

* Petit : 10,125 cm
* Normal : 13,5 cm
* Grand : 20,25 cm

## Mesures

### Grande Fenêtre

* Hauteur: 177cm
* Largeur : 190cm
* Hauteur sous fenêtre : 81cm
* Épaisseur mur : 10cm

### Petite fenêtre

* Hauteur : idem, 177cm
* Largeur : 94cm

### Triple fenêtre

* Largeur : 288cm

### Hauteur plafond

* 363cm

## Mur

* Mur 1 : 10cm
* Mur 2 : 14cm
* Mur toilettes : 7.5cm

### Porte

* hauteur : 204cm
* Largeur : 90cm

### Placard couloir

* largeur : 102cm
* hauteur : 206cm
