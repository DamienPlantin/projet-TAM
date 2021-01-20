import sqlite3
import argparse
from sqlite3.dbapi2 import Cursor
from time import *

def temps_attente(horaire):
    return strftime('%M min %S sec', gmtime(horaire))

parser = argparse.ArgumentParser("Script to interact with data from the TAM API")
# parser.add_argument("db_path", help="path to sqlite database")
# parser.add_argument("csv_path", help="path to csv file to load into the db")
parser.add_argument("next", help="next passages to a stop")
args = parser.parse_args()

# arret = args.next
# arret.append(args.next)
# print(arret)
conn = sqlite3.connect("tam.db")
c = conn.cursor()
c.execute(f"SELECT stop_name, route_short_name, trip_headsign, delay_sec FROM infoarret WHERE stop_name = '{args.next}'")
for contact in c.fetchall():
    print(f"Arrêt {contact[0]} Ligne {contact[1]} Destination {contact[2]} Temps d'attente {temps_attente(contact[3])}")