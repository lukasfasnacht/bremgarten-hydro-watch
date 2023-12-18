import sqlite3

# Verbindung zur Datenbank herstellen
conn = sqlite3.connect('hydrodata.db')
cursor = conn.cursor()

# SQL-Abfrage zum Löschen des Eintrags mit der ID 86
entry_id = 86
sql_query = f"DELETE FROM reuss WHERE id = {entry_id}"

# Abfrage ausführen
cursor.execute(sql_query)

# Änderungen speichern
conn.commit()

# Verbindung schließen
conn.close()