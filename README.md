# projet-TAM
Ce programme permet d'utiliser plusieurs fonctions dans une ligne de commande pour interagir avec le fichier.csv des horaires de la tam.

-Si aucun argument n'est spécifié, le fichier est telechargé automatiquement et mis à jour dans la base de donnée.
Si l'argument update est préciser la mise à jour de la base de donnée se fera avec un ficier renseigné.

-L'argument (args.station) permet d'afficher les prochains passages à la station toutes lignes et destinations confondus. 
les infos renvoyé seront enregistré dans un fichier txt si l'argument (-f) est spécifié.
Exemple : python transport.py -s 'CORUM T1 -f

-Les arguments (args.destination) et (args.ligne) couplé à l'argument (args.station) permettent d'afficher le delai d'attente 
pour le prochain transport rentré avec ces paramètres. 
 les infos renvoyé seront enregistré dans un fichier txt si l'argument (-f) est spécifié.
Exemple : python transport.py -s 'CORUM T1' -l 1 -d ODYSSEUM -f

-Si l'argument (args.action) est égale à "next", le programme renvoie les infos de (args.station) et si la station n'est pas 
indiqué dans la ligne de commande, un message d'erreur indique qu'il faut spécifier la station
Exemple : python transport.py next -s 'CORUM T1' -f

-Si l'argument (args.action) est égale à "wait", le programme renvoie les infos de (args.station, args.destination, args.ligne)
et si les paramètres ne sont pas bien indiqué, le programme renvoie un message d'erreur indiquant qu'il faut rentrer 
la Station, la Destination ainsi que la Ligne.
Exemple : python transport.py wait -s 'CORUM T1' -l 1 -d ODYSSEUM -f