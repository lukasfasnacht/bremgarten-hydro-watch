# Import various Python modules for crawling data from https://www.hydrodaten.admin.ch/de/seen-und-fluesse/stationen-und-daten/2018
import csv
import requests
import schedule
import time
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

# Function to crawl the website and save the data in a CSV file, clean CSV data, and store it in a database
def crawl_and_save():
    url = "https://www.hydrodaten.admin.ch/de/seen-und-fluesse/stationen-und-daten/2018"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer": "https://hydrodaten.admin.ch" 
    }
    response = requests.get(url, headers=headers)
    
    # Check if the website can be accessed successfully, otherwise print an error message
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")

        # Find the table element with the defined class
        table = soup.find("table", class_="table-carousel sensors-table columns-4")

        if table:
            # The table element was found
            # Save the table to CSV
            rows = table.find_all("tr")

            with open("raw_data.csv", "w", newline="", encoding="utf-8") as csvfile:
                csvwriter = csv.writer(csvfile)

                for row in rows:
                    cells = row.find_all(["th", "td"])
                    data = [cell.get_text(strip=True) for cell in cells]
                    csvwriter.writerow(data)

        else:
            print("The table was not found.")
    else:
        print("Error retrieving the webpage.")
    
    
    # Step 1: Select the second row from raw_data.csv (Last measurement)
    selected_row = None

    with open("raw_data.csv", "r", newline="") as csv_in:
        reader = csv.reader(csv_in)
        
        # Iterate through each row and select the second row
        for index, row in enumerate(reader, start=1):
            if index == 2:
                selected_row = row
                break

    # Step 2: Modify the selected row (remove 'Last measurement' and the last column)
    if selected_row:
        # Remove "Last measurement" from the first value
        selected_row[0] = selected_row[0].replace("Letzter Messwert", "").strip()
        
        # Keep only the first 4 columns (remove the last column)
        selected_row = selected_row[:4]

    # Step 3: Write the cleaned row into clean_data.csv
    with open("clean_data.csv", "w", newline="") as csv_out:
        writer = csv.writer(csv_out)
        writer.writerow(selected_row)
    
    # Read CSV file to store in the database
    with open("clean_data.csv", "r", newline="", encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile)
        data = list(csvreader)

    # Connect to SQLite database
    connection = sqlite3.connect("hydrodata.db")
    cursor = connection.cursor()

    # Create table if it does not already exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reuss (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            flow_rate INTEGER,
            water_level REAL,
            temperature REAL
        )
    """)

    # Insert data into the database without primary key
    for record in data:
        cursor.execute("INSERT INTO reuss (timestamp, flow_rate, water_level, temperature) VALUES (?, ?, ?, ?)", record)

    # Save changes
    connection.commit()

    # Close connection
    connection.close()
    
    print("Data inserted into the database")

# Scheduler to run every 30 minutes
schedule.every(30).minutes.do(crawl_and_save)

# Infinite loop to keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)