import sqlite3
import argparse
from sqlite3.dbapi2 import Cursor
from time import *

def temps_attente(horaire):
    return strftime('%M min %S sec', gmtime(horaire))

parser = argparse.ArgumentParser("Script to interact with data from the TAM API")
# parser.add_argument("db_path", help="path to sqlite database")
# parser.add_argument("csv_path", help="path to csv file to load into the db")
parser.add_argument("-s","--station", help="next passages to a stop")
parser.add_argument("-d", "--destination", help="time to wait")
parser.add_argument("-l", "--ligne", help="time to wait")
args = parser.parse_args()
conn = sqlite3.connect("tam.db")
c = conn.cursor()

def clear_rows(cursor):
    cursor.execute("""DELETE FROM infoarret""")


def insert_csv_row(csv_row, cursor):
    cursor.execute("""INSERT INTO infoarret VALUES (?,?,?,?,?,?,?,?,?,?,?) """,
                   csv_row.strip().split(";"))


def load_csv(path, cursor):
    with open(path, "r") as f:
        # ignore the header
        f.readline()
        line = f.readline()
        # loop over the lines in the file
        while line:
            insert_csv_row(line, cursor)
            line = f.readline()

def remove_table(cursor):
    cursor.execute("""DROP TABLE infoarret""")

def create_schema(cursor):
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

def download_csv():
    url = ("https://www.data.gouv.fr/fr/datasets/r/773ea45c-d7b0-4d75-94e3-47a5ad70f2ef")
    path = mypath.getcwd()

def main():
    args = parser.parse_args()
    if not args.csv_path or not args.db_path:
        print("Error : missing command line arguments")
        return 1

    if not conn:
        print("Error : could not connect to database {}".format(args.db_path))
        return 1

    
def time_wait():
    
    c.execute(f"SELECT stop_name, route_short_name, trip_headsign, delay_sec FROM infoarret WHERE stop_name = '{args.station}' AND trip_headsign = '{args.destination}' AND route_short_name = '{args.ligne}'")
    for contact in c.fetchall():
        print(f"Arrêt {contact[0]} Ligne {contact[1]} Destination {contact[2]} Temps d'attente {temps_attente(contact[3])}")

def stop_all():

    c.execute(f"SELECT stop_name, route_short_name, trip_headsign, delay_sec FROM infoarret WHERE stop_name = '{args.station}'")
    for contact in c.fetchall():
        print(f"Arrêt {contact[0]} Ligne {contact[1]} Destination {contact[2]} Temps d'attente {temps_attente(contact[3])}")

if args.station and args.destination and args.ligne:
    time_wait()
elif args.station:
    stop_all()

    # # remove_table(c)
    # create_schema(c)

    # load_csv(args.csv_path, c)

    # #write changes to database
    # conn.commit()
    # conn.close()
    # return 0


# if __name__ == "__main__":
#     sys.exit(main())
