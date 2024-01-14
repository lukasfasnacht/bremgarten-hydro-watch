<a name="readme-top"></a>

[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/lukasfasnacht/GLIN">
    <img src="static/favicon.svg" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Semesterprojekt GLIN HS23 - Gruppe Sauvignon Blanc</h3>

  <p align="center">
    Dieses GitHub-Repository dient als Dokumentation für unser Semesterprojekt im Modul "Grundlagen von Informationssystemen". Das Projekt wurde von Lukas Fasnacht, Osaze Osa, Noa Roth, Cyrill Schmid und Men Zimmermann entwickelt. In dieser README finden Sie eine umfassende Beschreibung unserer Arbeit, einschließlich Projektziele, der verwendeten Technologien, Architektur, Funktionalitäten und Anwendungsfälle. Darüber hinaus bieten wir Anleitungen zur Installation und Nutzung unseres Informationssystems.
    <br />
    <a href="https://github.com/lukasfasnacht/GLIN/blob/master/README.md"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="http://glin.lukasfasnacht.io/">View Website</a>
    ·
    <a href="https://github.com/lukasfasnacht/GLIN/issues">Report Bug</a>
    ·
    <a href="https://github.com/lukasfasnacht/GLIN/issues">Request Feature</a>
  </p>
</div>



<!-- Inhaltsverzeichnis  -->
<details>
  <summary>Inhaltsverzeichnis</summary>
  <ol>
    <li>
      <a href="#über-das-projekt">Über das Projekt</a>
      <ul>
        <li><a href="#idee-und-problemstellung">Idee und Problemstellung</a></li>
        <li><a href="#lösung">Lösung</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#voraussetzungen">Voraussetzungen</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#bekannte-bugs">Bekannte Bugs</a></li>
    <li><a href="#ressourcen">Ressourcen</a></li>
    <li><a href="#lizenz">Lizenz</a></li>
    <li><a href="#kontakt">Kontakt</a></li>
  </ol>
</details>


## Über das Projekt

[![Product Name Screen Shot][product-screenshot]](http://glin.lukasfasnacht.io)

Im Rahmen des Moduls "Grundlagen von Informationssysteme" wurde die Aufgabe erlegt ein einfaches Informationssystem in Form einer im Web dargestellten Datenbank zu erstellen. Wie diese Aufgabe umgesetzt wird, war uns, den Studierenden, überlassen. Während des Projektes gab es die Möglichkeiten Webex Meetings, mit unserem Dozent Ingmar Baetge, aufzusetzen. Sonstige Unterstützung folgte in Form von Video Tutorials, erstellt von Ingmar Baetge. 

### Idee und Problemstellung

Da einge unserer Gruppe bereits seit einigen Jahren im Feld der Informatik arbeiten, haben wir uns dazu entschieden eine etwas umfangreicheres Projekt zu liefern. Damit es auch spannend bleibt und ein Lerneffekt entsteht. Die Idee war es Hydrodaten der admin.ch [Website](https://www.hydrodaten.admin.ch/de/seen-und-fluesse/stationen-und-daten/2018) herunterzuladen, auszuwerten und dann selbst darzustellen. Das Herunterladen der Daten sollte alle 30min erfolgen. Das Interesse galt dabei rein an den Daten, welche als Indikation dienten, ob es möglich ist im Fluss Reuss zu surfen. Als kurze Hintergrundinformation; die Reuss bietet an einer spezifischen stelle die Möglichkeit auf einer stehenden Welle zu surfen [Beispiel](https://www.youtube.com/watch?v=wut1fKHDnqQ), ähnlich wie z.B. der Eisbach in München. Das dies jedoch möglich ist, braucht es genügend Abfluss. Abfluss bedeutet wie viel Wasser (in m³) pro Sekunde durch die Messstation fliesst. Bei dem Fall der Flusswelle in Bremgarten braucht es mindestens einen Abfluss von 180m³. 
Unsere Informatonssytem sollte also nun alle 30min Daten herunterladen, den Abflusswert einordnen, Daten aufbereiten und zusätzlich noch ein Chart der letzten Abflusswerte darzustellen.

### Lösung

Die Idee haben wir wie folgt umgesetzt:

**Datenerhebung**<br>
Um überhaupt Daten für die Darstellung zu haben, mussten diese zuerst gesammelt werden. Gleich wie bei einem Wetterbericht, bringt es nichts vergangene Daten zu erheben, sondern braucht es vorzu live Daten. Um dies umzusetzen wurde ein Python Script erstellt, welches mittels [BeautifulSoup](https://pypi.org/project/beautifulsoup4/), eine Python Library zum Crawlen von Websiten, alle 30min die Website www.hydrodaten.admin.ch/de/seen-und-fluesse/stationen-und-daten/2018 aufruft, eine definierte Tabelle der Website in eine lokale CSV Datei schreibt
```python
  if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")

        # Suchen table-Element mit der gesuchten Klasse
        table = soup.find("table", class_="table-carousel sensors-table columns-3")

        if table:
            # Das table-Element wurde gefunden
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
``````
die CSV Datei bereinigt
```python
# CSV Datei raw_data bearbeiten, alle Zeilen bis auf die 2e löschen und in neue CSV Datei clean_data speichern
    
    # Erstelle Liste zum Speichern der ausgewählten Zeile
    selected_row = None

    # CSV Datei raw_data öffnen
    with open("raw_data.csv", "r", newline="") as csv_in:
        reader = csv.reader(csv_in)
        
        # Iteriere durch jede Zeile und wähle die zweite Zeile aus
        for index, row in enumerate(reader, start=1):
            if index == 2:
                selected_row = row
                break

    # Schreibe die ausgewählte Zeile in die neue CSV-Datei clean_data
    with open("clean_data.csv", "w", newline="") as csv_out:
        writer = csv.writer(csv_out)
        writer.writerow(selected_row)
        
    # Letzter Messwert aus dem Datum löschen
    # Erstelle Liste zum Speichern der ausgewählten Zeile
    selected_row = None

    with open("clean_data.csv", "r", newline="") as csv_in:
        reader = csv.reader(csv_in)
        
        # Iteriere durch jede Zeile und wähle die erste Zeile aus
        for index, row in enumerate(reader, start=1):
            if index == 1:
                # Löscht Letzter Messwert
                row[0] = row[0].replace("Letzter Messwert", "")
                selected_row = row
                break

    # Schreibe die ausgewählte Zeile in die CSV-Datei
    with open("clean_data.csv", "w", newline="") as csv_out:
        writer = csv.writer(csv_out)
        writer.writerow(selected_row)
``````
sich mit einer lokalen Datenbank verbindet, die Daten der bereinigten CSV Datei in die Datenbank schreibt und die Verbindung zu Datenbank wieder schliesst.
```python
# CSV-Datei lesen um in DB zu speichern
    with open("clean_data.csv", "r", newline="", encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile)
        daten = list(csvreader)

    # SQLite-Datenbank verbinden
    connection = sqlite3.connect("hydrodata.db")
    cursor = connection.cursor()

    # Tabelle erstellen falls noch nicht vorhanden
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reuss (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            abfluss INTEGER,
            wasserstand REAL,
            temperatur REAL
        )
    """)

    # Daten in die Datenbank einfügen ohne Primärschlüssel
    for datensatz in daten:
        cursor.execute("INSERT INTO reuss (timestamp, abfluss, wasserstand, temperatur) VALUES (?, ?, ?, ?)", datensatz)

    # Änderungen speichern
    connection.commit()

    # Verbindung schließen
    connection.close()
```
Die Schwierigkeit hierbei war es das inzwischen viele Website einen Blocker für solche Crawl Scripts integriert haben. Es mussten also bei dem intialen Aufruf der Website, BeautifulSoup genug Daten im HTML Request Header mitgeben werden, damit die Website des Bundes das Gefühl hat hier möchte ein echter User auf die Website zugreifen und nicht irgendein Roboter (oder in diesem Fall Script).
```python
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer": "https://hydrodaten.admin.ch" 
    }
```

**Datenbank**<br>
Für dieses Projekt wurde auf eine eine SQLite Datenbank gesetzt, dies hat mehrere Gründe:
<ul>
  <li>Server-les Datenbank: SQLite ist eine Server-less Datenbank, das heisst es wird zusätzlich zur Datenbank keinen Datenbankserver benötigt.</li>
  <li>Plattformunabhängig: SQLite läuft auf Windows, MacOS, sowie Linux. Das Ziel war es das Informationssystem schlussendlich auf einem Debian Server über aws laufen zu lassen, deshalb war es wichtig eine Datenbank zu haben, welche auf allen Plattformen funktionert.</li>
  <li>Beliebtheit. SQLite erfreut sich einer hohen Beliebtheit und ist eine der meist verbreiteten Datenbanksystemen. Dies hat zum Vorteil das viele Ressourcen und Dokumentationen bereit stehen und die Chance das jemand das gleiche Problem wie man selbst hatte ist gross.</li>
</ul>

**Webserver**<br>
Um das Ganze nun als HTML Seite darzustellen, wurde Flask verwendet. Mithilfe von Flask und der Python  Bibliothek [SQLite]() wurde eine Verbindung zur Datenbank aufgestellt, sowie wurden die Daten abgerufen, sortiert und der HTML Seite zur Darstellung weitergegeben. Zusätzlich wurden die Funktionen Suchen, bei dem der User entweder gleich oder grösser gleich nach einem selbst eingegeben Abflusswert suchen kann. Die Daten werden jeweils in 20er Pakete dargestellt und der User kann mittels Seitenanzahl in den verschiedenen Seiten navigieren. Die Daten werden nach dem Filter "Datum absteigend" angezeigt. 
```python
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

    # HTML-Template rendern und Daten hergeben
    chart_image = generate_plot(dates, abflussData)
    connection.close()
    return render_template("index.html", daten=daten, abfluss_filter=abfluss_filter, comparison_operator=comparison_operator, total_pages=total_pages, current_page=page, chart_image=generate_plot(dates, abflussData))
```
Um das Chart zu erstellen wurde die Bibliothek [Matplotlib](https://matplotlib.org/) verwendet. Mithilfe denn Bibliotheken [BytesIO](https://wiki.python.org/moin/BytesIO) und [Base64](https://docs.python.org/3/library/base64.html) wurde der erstellte Chart in eine Bild Datei gespeichert und der HTML Datei weitergegeben.
```python
# Funktion für Generieren des Charts mit Matplot
def generate_plot(dates, abflussData):
    
    # Definition Grösse,x/y-Achse, Titel, Datumsformat x-Achse
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
```

**Website**<br>
Die Website wurde standardmässig mitfhilfe von HTML erstellt. Das Styling wurde mithilfe von [Tailwind](https://tailwindcss.com/) erreicht, zusätzliches spezifisches Styling wurde durch eine lokale CSS Datei erweitert. 
Wenn man auf der Website landet ist das erste was man sieht ein kurzen Text, welcher indiziert wie die momentane Surf-Situation ist. Diese wurde mit einer einfachen IF-Funktion erstellt, indem der letzte Abfluss Wert verglichen wird.
```html
<!-- Welcome Text. Zeigt in einer kurzen Message an, ob es momentan möglich ist zu surfen oder nicht. Jenachdem wie der Abflusswert ist, wird die Nachricht angepasst -->
    <div class="flex items-center justify-center text-3xl font-bold">
        {% if daten %}
            {% set last_abfluss = daten[0][2] %}
            {% if last_abfluss >= 400 %}
                <p>Pls help me, I"m under the water. Check in again in a few days, too much water.</p>
            {% elif last_abfluss >= 350 %}
                <p>Bring that life jacket. Its fucking huge...</p>
            {% elif last_abfluss >= 280 %}
                <p>Better be patient. Its gonna be crowded...</p>
            {% elif last_abfluss >= 180 %}
                <p>Call in sick! Its surfable!</p>
            {% else %}
                <p>Go back to work! It's flat...</p>
            {% endif %}
        {% endif %}
    </div>
```
Zusätzlich zu der Willkommens-Nachricht, wird der Abflusswert eingefärbt, wenn der Abflusswert einen "surfbaren" Wert erreicht oder sogar ein gefährliches Niveau erreicht. Dies wurde wieder mit einer IF-Funktion erstellt, indem der Abfluss Wert verglichen wird und jenachdem eine spezifische CSS Klasse zuweist.
```html
<td class="{% if row[2]|int >= 450 %}firebrick-cell{% elif row[2]|int >= 400 %}coral-cell{% elif row[2]|int >= 350 %}darkgreen-cell{% elif row[2]|int >= 250 %}forestgreen-cell{% elif row[2]|int >= 180 %}mediumseagreen-cell{% elif row[2]|int >= 0 %}white-cell{% else %}{{ "" }}{% endif %} px-8 pb-1">{{ row[2] }} m³/s</td>
```
```css
.white-cell {
  background-color: white;
}
.darkgreen-cell {
  background-color: darkgreen;
}
.mediumseagreen-cell {
  background-color: mediumseagreen;
}
.forestgreen-cell {
  background-color: forestgreen;
}
.coral-cell {
  background-color: coral;
}
.firebrick-cell {
  background-color: firebrick;
}
```
Damit der User auch weiss, welche Farbe was zu bedeuten hat gibt es zusätzlich eine Legende. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

In den nächsten zwei Kapitel wird erklärt wie man die Webapplikation bei sich selbst lokal laufen lassen kann.

### Voraussetzungen

Folgende Software und Bibliotheken sind notwendig für das Betreiben der Webapplikation:
* Python: <br>
  Über die [Python-Homepage](https://www.python.org/downloads/)<br>
  Homebrew:
    ```sh
    brew install python
    ```
* requests
  ```sh
  pip3 install requests
  ```
* schedule
  ```sh
  pip3 install schedule
  ```
* BeautifulSoup
  ```sh
  pip3 install beautifulsoup4
  ```
* Flask
  ```sh
  pip3 install Flask
  ```
* Matplotlib
  ```sh
  pip3 install matplotlib
  ```

### Installation

1. Klone dieses Repo
   ```sh
   git clone https://github.com/lukasfasnacht/GLIN
   ```
2. Es befindet sich bereits ein kleinder Datensatz in der Datenbank, falls mit einer leeren Datenbank gestartet werden möchte sollte dieser Schritt ausgeführt werden. Ansonsten kann direkt mit 3. weitergemacht werden
   ```sh
   rm -r hydrodata.db
   ```
3. Führe webcrawl.py im Hintergrund aus, optional mit Log output um das Skript zu überwachen
   ```sh
   python3 webcrawl.py > output.log 2>&1 &
   ```
4. Starte die Webapplikation
   ```sh
   python3 flaskapp.py
   ```
5. Done, öffne http://127.0.0.1:5000/ in deinem Browser

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Bekannte Bugs

### Filter Funktion und Pagnierung
Wenn man mitels der Filterfunktion einen Wert sucht, werden einem durch die Pagnierungsparameter nur die ersten 20 Values angezeigt. Wenn man nun mittels der Pagnierungs Navigation die Seite wechselt, wird auf der neuen Seite der Filtereffekt nicht angewendet. Dies hat zu Grunde das in der Grundstruktur die Pagnierungsfunktion unabhänig von der Filterfunktion funktioniert. Der Fehler wurde leider erst zu spät im Testing durch Cyrill Schmid entdeckt. Das Feature ist im nächsten Release geplant. 

## Ressourcen

Folgende Ressourcen dienten zur Unterstützung dieses Projektes

* Ingmar Beatge und die Vorlesungsunterlagen zu GLIN
* [Stackoverflow](https://stackoverflow.com/)
* [Github-Copilot](https://github.com/features/copilot)
* [Flask-Dokumentation](https://flask.palletsprojects.com/en/3.0.x/)
* [Matplotlib-Dokumentation](https://matplotlib.org/stable/users/index)
* [Tailwind-Dokumentation](https://v2.tailwindcss.com/docs)
* [Tailwind-Tutorial](https://www.youtube.com/watch?v=pfaSUYaSgRo)



<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Lizenz

Vertrieben unter der MIT-Lizenz. Weitere Informationen finden Sie in `LICENSE.txt`.


<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Kontakt

Lukas Fasnacht  - lukas.fasnacht@gmail.com

Projekt Link: [https://github.com/lukasfasnacht/GLIN](https://github.com/lukasfasnacht/GLIN)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- Links  und Bilder -->
[license-shield]: https://img.shields.io/github/license/lukasfasnacht/GLIN.svg?style=for-the-badge
[license-url]: https://github.com/lukasfasnacht/GLIN/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/lukas-fasnacht-593a67156/
[product-screenshot]: img/product-screenshot.png
