from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def anzeigen():
    # SQLite-Datenbank verbinden
    connection = sqlite3.connect('hydrodata.db')
    cursor = connection.cursor()

    # Daten aus der Tabelle abrufen
    cursor.execute('SELECT * FROM reuss')
    daten = cursor.fetchall()

    # Verbindung schlie ^=en
    connection.close()

    # HTML-Template rendern und Daten hergeben
    return render_template('index.html', daten=daten)

if __name__ == '__main__':
    app.run(debug=True)