import csv
import requests
import schedule
import time
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

# Funktion zum Crawlen der Website und Speichern der Daten in einer CSV-Datei, CSV Daten bereinigen und in DB abspeichern
def crawl_and_save():
    url = "https://www.hydrodaten.admin.ch/de/seen-und-fluesse/stationen-und-daten/2018"
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
    else:
        print("Fehler beim Abrufen der Webseite.")
    
    soup = BeautifulSoup(html_content, "html.parser")

    # Suchen <table>-Element mit der gesuchten Klasse
    table = soup.find("table", class_="table-carousel sensors-table columns-3")

    if table:
        # Das <table>-Element wurde gefunden
        # Table wird in CSV abgespeichert
        rows = table.find_all("tr")
        
        with open("raw_data.csv", "w", newline="", encoding="utf-8") as csvfile:
            csvwriter = csv.writer(csvfile)
                    
            for row in rows:
                cells = row.find_all(["th", "td"])  # Hier werden sowohl Headerzellen ("th") als auch Datenzellen ("td") berücksichtigt
                data = [cell.get_text() for cell in cells]
                csvwriter.writerow(data)
            
    else:
        print("Die Tabelle mit der Klasse" "table-carousel sensors-table columns-3" "wurde nicht gefunden.")


    # Öffnen Sie die CSV-Datei zum Lesen und eine neue CSV-Datei zum Schreiben
    with open("raw_data.csv", "r", newline="", encoding="utf-8") as infile, \
        open("clean_data.csv", "w", newline="", encoding="utf-8") as outfile:
        
        # CSV-Reader und -Writer erstellen
        csvreader = csv.reader(infile)
        csvwriter = csv.writer(outfile)
        
        # Erste Zeile löschen
        zeilen_zum_loeschen = [0]  # Zeile 0 löschen
        
        for zeilennummer, row in enumerate(csvreader):
            # Überprüfen ob die Zeile gelöscht werden soll
            if zeilennummer not in zeilen_zum_loeschen:
                # Für die verbleibenden Zeilen entfernen Zeilenumbrüche
                bereinigte_zeile = [zelle.strip() for zelle in row]
                csvwriter.writerow(bereinigte_zeile)

    # Daten aus der CSV-Datei lesen
    with open("clean_data.csv", "r", newline="", encoding="utf-8") as csv_datei:
        csv_reader = csv.reader(csv_datei)
        zeilen = list(csv_reader)

    # \n in der ersten Zeile entfernen, wird im vorherigen bereinigen Schritt nicht richtig ausgeführt
    zeilen[0][0] = zeilen[0][0].replace("\n", " ")

    # Daten zurück in die CSV-Datei schreiben
    with open("clean_data.csv", "w", newline="", encoding="utf-8") as csv_datei:
        csv_writer = csv.writer(csv_datei)
        csv_writer.writerows(zeilen)

    # CSV-Datei lesen um in DB zu speichern
    with open("clean_data.csv", "r", newline="", encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile)
        daten = list(csvreader)


    # SQLite-Datenbank verbinden
    connection = sqlite3.connect("hydrodata.db")
    cursor = connection.cursor()

    # Tabelle erstellen
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reuss (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            abfluss INTEGER,
            wasserstand REAL,
            temperatur REAL
        )
    """)
    connection.commit()

    # Daten in die Datenbank einfügen ohne Primärschlüssel
    for datensatz in daten:
        cursor.execute("INSERT INTO reuss (timestamp, abfluss, wasserstand, temperatur) VALUES (?, ?, ?, ?)", datensatz)



    connection.commit()

    # Verbindung schließen
    connection.close()
    
    print("Daten in die Datenbank eingefügt")

# Scheduler für alle halbe Stunde
schedule.every(1).minutes.do(crawl_and_save)

# Endlosschleife, um das Skript am Laufen zu halten
while True:
    schedule.run_pending()
    time.sleep(1)