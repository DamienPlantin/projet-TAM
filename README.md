# Projet-TAM

Ce programme permet d'utiliser plusieurs fonctions dans une ligne de commande pour interagir avec le fichier.csv des horaires de la Tam.
Pour utiliser ce programme, le client doit avoir installé python au préalable.

Auteurs: Damien, Yoan, Juljan. /ORGANISME SIMPLON/

Ce script respecte les conventions PEP8 et PEP257,
Une documentation est disponible au format html.

Les principales fonctionnalités de ce programme sont:

-Télécharger le fichier.csv de la tam en database
-Update la database si le fichier est déjà telechargé
-Afficher tous les prochains passages des transports à la station toutes lignes et destinations confondues
-Afficher le délai d'attente du prochain transport avec les paramètres entrés avec les arguments dans la ligne de commande
-Enregistrer les résultats de vos recherches dans un fichier.txt avec un argument

Fonctionnalités spécifiques:

-Si aucun argument n'est spécifié, le fichier est téléchargé automatiquement et mis à jour dans la base de donnée.
Si l'argument update est préciser la mise à jour de la base de données se fera avec un fichier renseigné.

-l'argument -s (args.station) permet d'afficher les prochains passages à la station toutes lignes et destinations confondues. 
les infos renvoyées seront enregistrées dans un fichier txt si l'argument (-f) est spécifié.
Exemple : python transport.py next -s 'CORUM T1 -f

-les arguments -d (args.destination) et -l (args.ligne) couplé à l'argument -s (args.station) permettent d'afficher le délai d'attente 
pour le prochain transport rentré avec ces paramètres. 
 les infos renvoyées seront enregistrées dans un fichier txt si l'argument (-f) est spécifié.
Exemple : python transport.py wait -s 'CORUM T1' -l 1 -d ODYSSEUM -f

-si l'argument action (args.action) est égale à "next", le programme renvoie les infos de (args.station) et si la station n'est pas 
indiquée dans la ligne de commande, un message d'erreur dit qu'il faut spécifier la station
Exemple : python transport.py next -s 'CORUM T1' -f

-si l'argument action (args.action) est égale à "wait", le programme renvoie les infos de (args.station, args.destination, args.ligne)
et si les paramètres ne sont pas bien indiqués, le programme renvoie un message d'erreur indiquant qu'il faut rentrer 
la station, la destination ainsi que la ligne.
Exemple : python transport.py wait -s 'CORUM T1' -l 1 -d ODYSSEUM -f

Difficultés rencontrées pendant le développement du programme:

-Les normes PEP8 et PEP257 rendre plus compliqué la simplification et la clarté du code
-Mise en place des logs pour l'intégralité du script
-Manque d'effectifs dans la réalisation du projet
-Utilisation des fonctionnalités de git


 
