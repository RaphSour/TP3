# TP3_Comparateur_Couche

Description

Ce plugin QGIS permet de comparer deux couches spatiales sélectionnées et d'en extraire :

Le nom de chaque couche

Le type de géométrie (Point, Ligne, Polygone)

Le nombre total d'entités

La projection

La surface totale (pour les polygones)

La longueur totale (pour les lignes)

Des statistiques sur un champ numérique sélectionné (moyenne, médiane, écart-type, minimum, maximum, somme, nombre d'entités)

Option de limitation aux entités visibles dans l'étendue de la vue

Export CSV des métadonnées, de la bounding box (si option activée) et des statistiques

Prérequis

QGIS 3.x

Python 3

Aucune dépendance externe supplémentaire (utilise uniquement les bibliothèques QGIS et Python standard)

Installation

Copier le dossier du plugin (TP3_Comparateur_Couche) dans le répertoire des plugins de QGIS :

Sous Windows : %APPDATA%\QGIS\QGIS3\profiles\default\python\plugins

Sous Linux : ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins

Redémarrer QGIS.

Activer le plugin dans le gestionnaire d’extensions (Plugins ▶️ Gestionnaire d’extensions).

Utilisation

Ouvrir le plugin via la barre d’outils ou le menu "Comparateur de couche".

Sélectionner la Couche 1 et la Couche 2 dans les listes déroulantes.

Visualiser instantanément :

Les informations de base (nom, géométrie, projection, surface/longueur, nombre d’entités).

Remplissage du QTableWidget avec les statistiques sur le champ sélectionné.

Cocher "Limiter à la vue" pour ne prendre en compte que les entités visibles dans l’étendue actuelle.

Cliquer sur Export CSV pour enregistrer :

Les coordonnées de la bounding box (si option activée)

Les métadonnées des deux couches

Les valeurs de statistiques
