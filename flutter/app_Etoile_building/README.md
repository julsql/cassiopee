# flutter_json_test

This project is an application to visualize the IoT devices of the Etoile Building of the Telecom SudParis campus

## Installer flutter pour linux

1. installer :
    ```sudo snap install flutter --classic```
2. vérifier où en est l'installation et voir ce qu'il reste à installer (tout doit être en vert à la fin)
    ```flutter doctor```
3. regarder le détail de ce qu'il manque :
    ```flutter doctor -v```
4. pour régler le problème qui concerne google chrome :
    a. télécharger google chrome : [https://www.google.com/intl/fr/chrome/gsem/download/?brand=YTUH&gclid=CjwKCAjwiOCgBhAgEiwAjv5whB1bmDt1a7EU6PeNsJ6ybn_QzYBENdoCe1jFyz33cis8Yjox7neOgxoCn04QAvD_BwE&gclsrc=aw.ds](https://www.google.com/intl/fr/chrome/gsem/download/?brand=YTUH&gclid=CjwKCAjwiOCgBhAgEiwAjv5whB1bmDt1a7EU6PeNsJ6ybn_QzYBENdoCe1jFyz33cis8Yjox7neOgxoCn04QAvD_BwE&gclsrc=aw.ds)
    b. se placer dans le dossier où on a télécharger puis commande :
        ```sudo dpkg -i google-chrome-stable_current_amd64.deb```
    c. commande :
       ```export CHROME_EXECUTABLE=/usr/bin/google-chrome```
5. pour régler le problème lié à java et à PATH :
    ```export PATH="$PATH:/usr/bin/java"```
6. pour régler le problème avec JAVA_HOME :
    ```export JAVA_HOME=$(/usr/bin/java)```
7. pour régler le problème avec android studio :
    ```flutter config --android-studio-dir=```

## Installer flutter sur mac

> Il faut avoir Chrome installé

1. Télécharger l'archive [https://docs.flutter.dev/get-started/install/macos](https://docs.flutter.dev/get-started/install/macos)

2. extraire l'archive dans le fichier où l'on veut le stocker

```cd ~/development```
```unzip ~/Downloads/flutter_macos_3.10.2-stable.zip```

1. Ajouter la commande Flutter

   ```export PATH="\$PATH:$HOME/flutter/bin"```

2. vérifier où en est l'installation et voir ce qu'il reste à installer (tout doit être en vert à la fin)
    ```flutter doctor```

## les ressources utilisées

site avec tuto flutter :
    [https://docs.flutter.dev/development/ui/layout/tutorial#step-1-diagram-the-layout](https://docs.flutter.dev/development/ui/layout/tutorial#step-1-diagram-the-layout)
exemple de projet utilisant des fichier JSON :
    [https://flutter.github.io/samples/jsonexample.html](https://flutter.github.io/samples/jsonexample.html)

## Run Flutter

Dans le répertoire racine du projet Futter :

    ```flutter run -d chrome```

Lorsqu'on modifie pudspec.yaml :

    ```flutter pub get```

## Comment fonctionne Flutter

les widgets basiques :
    - Text
    - Row, Column : layout horizontal ou vertical
    - Stack : widgets qui sont placés les uns sur les autres (on peut ensuite utiliser le widget Positioned comme enfant de Stack pour placer les éléments les uns par rapport aux autres)
    - Container : élément visuel rectangle. Il peut être décoré avec BoxDecoration pour changer le fond, le contour... Il peut aussi avoir des marges (margins), padding et des contraintes de taille. On peut le transformer en élément 3D avec une matrice.

## How to code the application

ajouter une image :
    - ajouter l'image à pubspec.yaml avant
  