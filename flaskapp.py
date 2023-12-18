from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def anzeigen():
    # SQLite-Datenbank verbinden
    connection = sqlite3.connect('hydrodata.db')
    cursor = connection.cursor()

    # Filter-Wert und Vergleichsoperator abrufen
    abfluss_filter = request.form.get('abfluss_filter')
    comparison_operator = request.form.get('comparison_operator', 'greater_equal')  # Standard: grösser gleich

    # Filter zurücksetzen, wenn der entsprechende Button geklickt wurde
    if 'reset_filter' in request.form:
        abfluss_filter = None
        comparison_operator = 'greater_equal'

    # Paginierungsparameter
    page = request.args.get('page', 1, type=int)
    entries_per_page = 20

    # Berechne den Offset basierend auf der Seitennummer
    offset = (page - 1) * entries_per_page

    # Datenbankabfrage mit Paginierung
    if abfluss_filter is not None:
        if comparison_operator == 'exact':
            cursor.execute('SELECT * FROM reuss WHERE abfluss = ? ORDER BY id DESC LIMIT ? OFFSET ?', (abfluss_filter, entries_per_page, offset))
        elif comparison_operator == 'greater_equal':
            cursor.execute('SELECT * FROM reuss WHERE abfluss >= ? ORDER BY id DESC LIMIT ? OFFSET ?', (abfluss_filter, entries_per_page, offset))
    else:
        cursor.execute('SELECT * FROM reuss ORDER BY id DESC LIMIT ? OFFSET ?', (entries_per_page, offset))

    daten = cursor.fetchall()

    # Berechne die Gesamtanzahl der Seiten für die Paginierung
    cursor.execute('SELECT COUNT(*) FROM reuss')
    total_entries = cursor.fetchone()[0]
    total_pages = (total_entries // entries_per_page) + (1 if total_entries % entries_per_page > 0 else 0)
    
    # Verbindung schließen
    connection.close()

    # HTML-Template rendern und Daten hergeben
    return render_template('index.html', daten=daten, abfluss_filter=abfluss_filter, comparison_operator=comparison_operator, total_pages=total_pages, current_page=page)

if __name__ == '__main__':
    app.run(debug=True)
