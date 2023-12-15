from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def anzeigen():
    # SQLite-Datenbank verbinden
    connection = sqlite3.connect('hydrodata.db')
    cursor = connection.cursor()

    # Filter-Wert abrufen (wird 'None' sein, wenn nicht im Formular gepostet)
    abfluss_filter = request.form.get('abfluss_filter')

    # Filter zurücksetzen, wenn der entsprechende Button geklickt wurde
    if 'reset_filter' in request.form:
        abfluss_filter = None

    # Daten aus der Tabelle abrufen und absteigend nach der ID sortieren
    if abfluss_filter is not None:
        cursor.execute('SELECT * FROM reuss WHERE abfluss >= ? ORDER BY id DESC', (abfluss_filter,))
    else:
        cursor.execute('SELECT * FROM reuss ORDER BY id DESC')
    daten = cursor.fetchall()

    # Verbindung schließen
    connection.close()

    # HTML-Template rendern und Daten hergeben
    return render_template('index.html', daten=daten, abfluss_filter=abfluss_filter)

if __name__ == '__main__':
    app.run(debug=True)
