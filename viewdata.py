import sqlite3

# SQLite-Datenbank verbinden
connection = sqlite3.connect('hydrodata.db')
cursor = connection.cursor()

# Alle Datensätze aus der Tabelle abrufen
cursor.execute('SELECT * FROM reuss')
daten = cursor.fetchall()

# Verbindung schließen
connection.close()

# Ergebnisse anzeigen
for datensatz in daten:
    print(datensatz)
