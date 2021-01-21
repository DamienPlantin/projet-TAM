import sqlite3
import argparse
import sys
import urllib.request
from time import *
import logging

logger = logging.getLogger('RandomGroup')
logger.setLevel(logging.DEBUG)

# créer un gestionnaire de console et niveau de réglage pour le débogage
ch = logging.StreamHandler()
ch = logging.FileHandler('Log.txt', encoding='utf-8')
ch.setLevel(logging.DEBUG)

# créer un format d'affichage
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

# ajoute le format au ch
ch.setFormatter(formatter)

# ajoute le ch au logger
logger.addHandler(ch)


def temps_arrive(horaire):
    """Docstring de la fonction temps_arrive :
    
    strftime : permet de convertir la variable horaire donnée en seconde et la sortir en minutes et secondes 
    """
    logger.debug("Appel de la fonction temps_arrive()")
    logger.debug("Conversion de %s sec en %s", horaire, strftime('%M min %S sec', gmtime(horaire)))
    return strftime('%M min %S sec', gmtime(horaire))


def download():
    """Docstring de la fonction download :
    
    urllib.request.urlretrieve : permet de télécharger le fichier donné dans le lien et de le renommer
    """
    logger.debug("Appel de la fonction download")
    logger.debug("Tentative de téléchargement du fichier .csv à l'@ https://data.montpellier3m.fr/sites/default/files/ressources/TAM_MMM_TpsReel.csv")
    urllib.request.urlretrieve('https://data.montpellier3m.fr/sites/default/files/ressources/TAM_MMM_TpsReel.csv', "TpsReel.csv")
    dl = "TpsReel.csv"
    logger.debug("Téléchagement réussi, nom du fichier : %s", dl)
    return dl


def clear_rows(cursor):
    """Docstring de la fonction clear_rows :

    Cette fonction permet de supprimer le tableau présent dans la table 'infoarret'
    
    cursor : commande SQL possible avec la librairie sqlite3 de python
    permet de se placer dans la table 'infoarret'
    """
    cursor.execute("""DELETE FROM infoarret""") # Dans la parenthèse on peut faire une requête SQL


def insert_csv_row(csv_row, cursor):
    """Docstring de la fonction insert_csv_row
    
    Cette fonction permet d'inserer les informations du fichier csv dans la table 'infoarret'
    """
    cursor.execute("""INSERT INTO infoarret VALUES (?,?,?,?,?,?,?,?,?,?,?) """,
                   csv_row.strip().split(";"))


def load_csv(path, cursor):
    """Docstring de la fonction load_csv
    
    Cette fonction permet de charger le fichier csv dans la table 'infoarret'
    avec la fonction insert_csv_row

    path : chemin d'accès et/ou fichier csv
    """
    logger.debug("Appel de la fonction load_csv()")
    logger.debug("Tentative d'ouverture du fichier %s", path)
    with open(path, "r") as f:
        # ignore the header (ignorer la première ligne qui correspond au nom des colonnes)
        f.readline()            # On lit la première ligne
        line = f.readline()
        logger.debug("Ouverture du fichier et lecture de la première ligne réussi")
        logger.debug("Appel de la fonction insert_csv_row() pour chaque ligne du fichier csv")
        # loop over the lines in the file (boucle la lecture des lignes tant qu'il y a des lignes dans le fichier csv)
        while line:
            insert_csv_row(line, cursor)
            line = f.readline()


def remove_table(cursor):
    """Docstring de la fonction remove_table 
    
    Cette fonction permet de supprimer la table 'infoarret' s'il y a une table de présente
    dans la base de donnée
    """
    logger.debug("Appel de la fonction remove_table()")
    cursor.execute("""DROP TABLE IF EXISTS infoarret""")
    logger.debug("Si une table 'infoarret' est présente dans la base de donnée, suppression de cette table")


def create_schema(cursor):
    """Docstring de la fonction create_schema
    
    Cette fonction permet de créer une table 'infoarret' si elle n'existe pas et
    de lui renseigner les colonnes avec leurs types
     """
    logger.debug("Appel de la fonction create_schema()")
    cursor.execute("""CREATE TABLE IF NOT EXISTS "infoarret" (
    "course"	INTEGER,
    "stop_code"	TEXT,
    "stop_id"	INTEGER,
    "stop_name"	TEXT,
    "route_short_name"	TEXT,
    "trip_headsign"	TEXT,
    "direction_id"	INTEGER,
    "is_theorical" INTEGER,
    "departure_time"	TEXT,
    "delay_sec"	INTEGER,
    "dest_arr_code"	INTEGER
    );""")
    logger.debug("Création de la table 'infoarret'")


def next_passage(cursor):
    """Docstring de la fonction next_passage
    
    cette fonction permet de renseigner sur les prochains passages prévu à un arrêt donné
    """
    logger.debug("Appel de la fonction next_passage()")
    logger.debug("Selection des colonnes pour le résultat de la recherche")
    cursor.execute('SELECT stop_name, route_short_name, trip_headsign, delay_sec FROM infoarret WHERE stop_name = ?', (args.station,))
    for contact in cursor.fetchall():
        if args.fichier:
            passage = str(f"Arrêt {contact[0]} Ligne {contact[1]} Destination {contact[2]} Temps d'attente {temps_arrive(contact[3])}\n")
            sys.stdout = open('test.txt', 'a', encoding='utf-8')
            sys.stdout.write(passage)
        else:
            print(f"Arrêt {contact[0]} Ligne {contact[1]} Destination {contact[2]} Temps d'attente {temps_arrive(contact[3])}")
            logger.info(f"Arrêt {contact[0]} Ligne {contact[1]} Destination {contact[2]} Temps d'attente {temps_arrive(contact[3])}")


def next_wait(c):
    """Docstring de la fonction next_wait
    
    Cette fonction permet de sélectionner soit la fonction next_passage si l'action est next,
    soit time_wait si l'action est wait
    """
    logger.debug("Appel de la fonction next_wait()")
    if not args.action:
        print("Attention, veuillez précisez next ou wait")
        logger.warning("Attention, argument next ou wait manquants")
    if args.action =="next":
        logger.debug("Utilisation de l'argument 'next'")
        if args.station:
            logger.debug("Utilisation de l'argument -s %s pour la station", args.station)
            next_passage(c)
            return 1
        else:
            print("Il manque -s STATION")
            logger.warning("Attention, argument -s STATION manquant")
            return 1
    if args.action =="wait":
        logger.debug("Utilisation de l'argument 'wait'")
        if args.station and args.destination and args.ligne:
            logger.debug("Utilisation des arguments -s %s -d %s -l %s", args.station, args.destination ,args.ligne)
            time_wait(c)
            return 1
        else:
            print("Il manque -s STATION -d DESTINATION -l LIGNE")
            logger.warning("Attention, argument -s STATION -d DESTINATION -l LIGNE manquants")
            return 1


def time_wait(cursor):
    """Docstring de la fonction time_wait
    
    Cette fonction permet d'afficher le temps d'attente à un arrêt, pour une ligne vers une destination
    """
    logger.debug("Appel de la fonction time_wait()")
    cursor.execute(f"SELECT stop_name, route_short_name, trip_headsign, delay_sec FROM infoarret WHERE stop_name = ? AND trip_headsign = ? AND route_short_name = ?", (args.station, args.destination, args.ligne))
    for contact in cursor.fetchall():
        if args.fichier:
            passage = str(f"Arrêt {contact[0]} Ligne {contact[1]} Destination {contact[2]} Temps d'attente {temps_arrive(contact[3])}\n")
            sys.stdout = open('test.txt', 'a', encoding='utf-8')
            sys.stdout.write(passage)            
        else:
            print(f"Arrêt {contact[0]} Ligne {contact[1]} Destination {contact[2]} Temps d'attente {temps_arrive(contact[3])}")
            logger.info(f"Arrêt {contact[0]} Ligne {contact[1]} Destination {contact[2]} Temps d'attente {temps_arrive(contact[3])}")


parser = argparse.ArgumentParser("Script to interact with data from the TAM API")
parser.add_argument("-u", "--update", help="mise à jour à partir d'un fichier ou chemin d'accés")
parser.add_argument("-s","--station", help="next passages to a stop")
parser.add_argument("-d", "--destination", help="time to wait")
parser.add_argument("-l", "--ligne", help="time to wait")
parser.add_argument("action", nargs='?', help="wait time or next passages to a stop")
parser.add_argument("-f", "--fichier", action='store_true', help='test')

args = parser.parse_args()


logger.debug("************************************** Début du script ***********************************************************")

def main():
    """Docstring de la fonction main
    
    Cette fonction permet de se connecter à la base de donnée, de supprimer la table si elle existe.
    De plus, elle permet également de mettre à jour la base de donnée soit avec un fichier csv déjà
    présent sur le périphérique, soit en téléchargent directement le fichier csv depuis le site de la TAM
    """
    conn = sqlite3.connect("tam.db") # Connection entre sqlite et notre fichier db
    logger.debug("Connection/création du fichier tam.db pour la base de donnée")
    c = conn.cursor() #permet de se positionner sur la BdD
    logger.debug("Positionnement d'un curseur dans la base de donnée")
    remove_table(c)
    

    if not conn:
        print("Error : could not connect to database {}".format("tam.db"))
        logger.warning("Attention, il n'y as pas de base de donnée")
        return 1

    if args.update:
        logger.debug("Mise à jour manuelle de la base de donnée avec le fichier %s", args.update)
        create_schema(c)
        load_csv(args.update, c)
        conn.commit()
        next_wait(c)
        conn.close()
    else:
        create_schema(c)
        load_csv(download(), c)
        conn.commit()
        next_wait(c)
        conn.close()

    
    
    logger.debug('************************************** Fin du script *****************************************************************')


if __name__ == "__main__":
    sys.exit(main())