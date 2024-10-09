# Import div. Python Module für den Webserver
from flask import Flask, render_template, request
import sqlite3
import matplotlib.pyplot as plt
plt.switch_backend("Agg")
from io import BytesIO
import base64
from datetime import datetime

app = Flask(__name__)

# Funktion für Generieren des Charts mit Matplot
def generate_plot(dates, abflussData):
    
    # Definition Grösse,x/y-Achse, Titel, Datumsformat der x-Achse
    plt.figure(figsize=(10, 6))
    plt.plot(dates, abflussData, marker="o", linestyle="-", color="blue")
    plt.xlabel("")
    plt.ylabel("Abfluss in m³/s")
    plt.title("Abflussdaten der angezeigten Messwerte")
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%d.%m.%Y %H:%M"))
    plt.gcf().autofmt_xdate()

    # Speichern Sie das Diagramm in einem BytesIO-Objekt
    image_stream = BytesIO()
    plt.savefig(image_stream, format="png")
    image_stream.seek(0)

    # Base64-Codierung für die Anzeige in HTML
    encoded_image = base64.b64encode(image_stream.read()).decode("utf-8")

    # Chart als Bild zurückgeben
    return f"data:image/png;base64,{encoded_image}"

# Funktion für das Darstellen der Website
@app.route("/", methods=["GET", "POST"])
def anzeigen():
    
    # SQLite-Datenbank verbinden
    connection = sqlite3.connect("hydrodata.db")
    cursor = connection.cursor()

    # Filter-Wert und Vergleichsoperator abrufen
    abfluss_filter = request.form.get("abfluss_filter")
    # Standard-Operator: grösser gleich
    comparison_operator = request.form.get("comparison_operator", "greater_equal")  

    # Filter zurücksetzen, wenn der entsprechende Button geklickt wurde
    if "reset_filter" in request.form:
        abfluss_filter = None
        comparison_operator = "greater_equal"

    # Paginierungsparameter
    page = request.args.get("page", 1, type=int)
    entries_per_page = 20

    # Berechne den Offset basierend auf der Seitennummer
    offset = (page - 1) * entries_per_page

    # Datenbankabfrage mit Paginierung
    if abfluss_filter is not None:
        if comparison_operator == "exact":
            cursor.execute("SELECT * FROM reuss WHERE abfluss = ? ORDER BY id DESC LIMIT ? OFFSET ?", (abfluss_filter, entries_per_page, offset))
        elif comparison_operator == "greater_equal":
            cursor.execute("SELECT * FROM reuss WHERE abfluss >= ? ORDER BY id DESC LIMIT ? OFFSET ?", (abfluss_filter, entries_per_page, offset))
    else:
        cursor.execute("SELECT * FROM reuss ORDER BY id DESC LIMIT ? OFFSET ?", (entries_per_page, offset))

    daten = cursor.fetchall()
    
    # Zeitstempel in ein Datetime-Objekt umwandeln und für den Chart in Variable dates abspeichern
    dates = [datetime.strptime(row[1], "%d.%m.%Y %H:%M") for row in daten]
    
    # Abflussdaten für den Chart in Variable abflussData speichern
    abflussData = [row[2] for row in daten]

    # Berechne die Gesamtanzahl der Seiten für die Paginierung
    cursor.execute("SELECT COUNT(*) FROM reuss")
    total_entries = cursor.fetchone()[0]
    total_pages = (total_entries // entries_per_page) + (1 if total_entries % entries_per_page > 0 else 0)

    # HTML-Template rendern und Daten übergeben
    chart_image = generate_plot(dates, abflussData)
    connection.close()
    return render_template("index.html", daten=daten, abfluss_filter=abfluss_filter, comparison_operator=comparison_operator, total_pages=total_pages, current_page=page, chart_image=generate_plot(dates, abflussData))

if __name__ == "__main__":
    app.run(debug=True)
