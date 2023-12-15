import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.hydrodaten.admin.ch/de/seen-und-fluesse/stationen-und-daten/2018"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
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

        with open("sandbox.csv", "w", newline="", encoding="utf-8") as csvfile:
            csvwriter = csv.writer(csvfile)

            for row in rows:
                cells = row.find_all(["th", "td"])
                data = [cell.get_text(strip=True) for cell in cells]
                csvwriter.writerow(data)

    else:
        print("Die Tabelle mit der Klasse 'table-carousel sensors-table columns-3' wurde nicht gefunden.")
else:
    print("Fehler beim Abrufen der Webseite.")