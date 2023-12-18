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
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer": "https://hydrodaten.admin.ch" 
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        html_content = response.text
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
                    cells = row.find_all(["th", "td"])
                    data = [cell.get_text(strip=True) for cell in cells]
                    csvwriter.writerow(data)

        else:
            print("Die Tabelle wurde nicht gefunden.")
    else:
        print("Fehler beim Abrufen der Webseite.")
    
    
    # Alle Zeilen bis auf die 2 löschen
    # Liste zum Speichern der ausgewählten Zeile
    selected_row = None

    with open("raw_data.csv", 'r', newline='') as csv_in:
        reader = csv.reader(csv_in)
        
        # Iteriere durch jede Zeile und wähle die zweite Zeile aus
        for index, row in enumerate(reader, start=1):
            if index == 2:
                selected_row = row
                break

    # Schreibe die ausgewählte Zeile in die neue CSV-Datei
    with open("clean_data.csv", 'w', newline='') as csv_out:
        writer = csv.writer(csv_out)
        writer.writerow(selected_row)

        

    # CSV-Datei lesen um in DB zu speichern
    with open("clean_data.csv", "r", newline="", encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile)
        daten = list(csvreader)
        
    # Leerzeichen zwischen Letzter Messwert10.12.2023 und Datum einfügen
    # Liste zum Speichern der ausgewählten Zeile
    selected_row = None

    with open("clean_data.csv", 'r', newline='') as csv_in:
        reader = csv.reader(csv_in)
        
        # Iteriere durch jede Zeile und wähle die zweite Zeile aus
        for index, row in enumerate(reader, start=1):
            if index == 1:
                # Füge ein Leerzeichen zwischen "Letzter Messwert" und dem Datum ein
                row[0] = row[0].replace('Letzter Messwert', '')
                selected_row = row
                break

    # Schreibe die ausgewählte Zeile in die CSV-Datei
    with open("clean_data.csv", 'w', newline='') as csv_out:
        writer = csv.writer(csv_out)
        writer.writerow(selected_row)
    
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
schedule.every(30).minutes.do(crawl_and_save)

# Endlosschleife, um das Skript am Laufen zu halten
while True:
    schedule.run_pending()
    time.sleep(1)