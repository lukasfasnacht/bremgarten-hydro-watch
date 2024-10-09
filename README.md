<a name="readme-top"></a>

[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/lukasfasnacht/GLIN">
    <img src="static/favicon.svg" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Semester Project GLIN HS23</h3>

  <p align="center">
    This GitHub repository serves as documentation for the semester project in the module "Fundamentals of Information Systems." This README provides a comprehensive description of the work, including project objectives, technologies used, architecture, functionalities, and use cases. Additionally, instructions for installation and usage of the information system are provided.
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

<!-- Table of Contents -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About the Project</a>
      <ul>
        <li><a href="#idea-and-problem-statement">Idea and Problem Statement</a></li>
        <li><a href="#solution">Solution</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#known-bugs">Known Bugs</a></li>
    <li><a href="#resources">Resources</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## About the Project

[![Product Name Screen Shot][product-screenshot]](http://glin.lukasfasnacht.io)

As part of the "Fundamentals of Information Systems" module, the task was to create a simple information system in the form of a web-based database. The implementation of this task was left to the discretion of the students. During the project, there was the opportunity to set up Webex meetings with the instructor, Ingmar Baetge. Additional support was provided in the form of video tutorials created by Ingmar Baetge.

### Idea and Problem Statement

Given the existing knowledge in computer science and software development, it was decided to deliver a more extensive project to keep the task challenging and educational. The idea was to download hydrological data from the admin.ch [website](https://www.hydrodaten.admin.ch/de/seen-und-fluesse/stationen-und-daten/2018), analyze it, and then display it independently. The data should be downloaded every 30 minutes. The focus was specifically on determining whether it would be possible to surf on the Reuss River based on the flow rate. As background information, the Reuss offers a standing wave at a specific spot that can be surfed [example](https://www.youtube.com/watch?v=wut1fKHDnqQ), similar to the Eisbach in Munich. To make surfing possible, there must be a minimum flow rate of 180 m³ per second. Therefore, the information system was designed to download the data every 30 minutes, categorize the flow rate, process the data, and additionally display a chart of the recent flow rates.

### Solution

The idea was implemented as follows:

**Data Collection**<br>
To have data available for visualization, it first needed to be collected. Similar to a weather forecast, collecting only past data is not sufficient; live data is required. To achieve this, a Python script was created that uses [BeautifulSoup](https://pypi.org/project/beautifulsoup4/), a Python library for web scraping, to access the website www.hydrodaten.admin.ch/de/seen-und-fluesse/stationen-und-daten/2018 every 30 minutes, scrape a defined table from the website, and save it into a local CSV file.
```python
  if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")

        # Find table element with the desired class
        table = soup.find("table", class_="table-carousel sensors-table columns-3")

        if table:
            # The table element was found
            # Save table to CSV
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
```
Clean the CSV file by retaining only the second row and saving it to a new CSV file `clean_data`.
```python
# Edit raw_data CSV file, remove all rows except the second row, and save it to a new CSV file clean_data
    
    # Create a list to store the selected row
    selected_row = None

    # Open the raw_data CSV file
    with open("raw_data.csv", "r", newline="") as csv_in:
        reader = csv.reader(csv_in)
        
        # Iterate through each row and select the second row
        for index, row in enumerate(reader, start=1):
            if index == 2:
                selected_row = row
                break

    # Write the selected row to the new CSV file clean_data
    with open("clean_data.csv", "w", newline="") as csv_out:
        writer = csv.writer(csv_out)
        writer.writerow(selected_row)
        
    # Remove 'Last Measurement' from the data
    selected_row = None

    with open("clean_data.csv", "r", newline="") as csv_in:
        reader = csv.reader(csv_in)
        
        # Iterate through each row and select the first row
        for index, row in enumerate(reader, start=1):
            if index == 1:
                # Remove 'Last Measurement'
                row[0] = row[0].replace("Letzter Messwert", "")
                selected_row = row
                break

    # Write the selected row to the CSV file
    with open("clean_data.csv", "w", newline="") as csv_out:
        writer = csv.writer(csv_out)
        writer.writerow(selected_row)
```
Connect to a local database, write the cleaned CSV data to the database, and close the connection.
```python
# Read the CSV file to store it in the database
    with open("clean_data.csv", "r", newline="", encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile)
        data = list(csvreader)

    # Connect to SQLite database
    connection = sqlite3.connect("hydrodata.db")
    cursor = connection.cursor()

    # Create a table if it does not exist
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
```
One challenge was that many websites have blockers to prevent web scraping scripts. Therefore, during the initial request, BeautifulSoup had to provide enough information in the HTML request headers so that the government website would believe an actual user, rather than a bot (or script), was accessing it.
```python
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer": "https://hydrodaten.admin.ch" 
    }
```

**Database**<br>
An SQLite database was chosen for this project for several reasons:
<ul>
  <li>Server-less Database: SQLite is a server-less database, which means that no additional database server is required.</li>
  <li>Cross-Platform: SQLite works on Windows, macOS, and Linux. The goal was to ultimately run the information system on a Debian server via AWS, so it was important to use a database that works on all platforms.</li>
  <li>Popularity: SQLite is highly popular and one of the most widely used database systems. This means there are many resources and documentation available, and it is likely that someone has already solved the same problem.</li>
</ul>

**Web Server**<br>
To display the data as an HTML page, Flask was used. With the help of Flask and the Python library [SQLite](), a connection to the database was established, and data was retrieved, sorted, and passed to the HTML page for display. Additionally, functions were implemented to allow users to search for flow rates that are equal to or greater than a specified value. The data is displayed in sets of 20, and users can navigate through the pages using pagination. The data is displayed in descending date order.
```python
# Function to display the website
@app.route("/", methods=["GET", "POST"])
def display():
    
    # Connect to SQLite database
    connection = sqlite3.connect("hydrodata.db")
    cursor = connection.cursor()

    # Retrieve filter value and comparison operator
    flow_filter = request.form.get("flow_filter")
    # Default operator: greater or equal
    comparison_operator = request.form.get("comparison_operator", "greater_equal")  

    # Reset filter if the corresponding button is clicked
    if "reset_filter" in request.form:
        flow_filter = None
        comparison_operator = "greater_equal"

    # Pagination parameters
    page = request.args.get("page", 1, type=int)
    entries_per_page = 20

    # Calculate offset based on page number
    offset = (page - 1) * entries_per_page

    # Database query with pagination
    if flow_filter is not None:
        if comparison_operator == "exact":
            cursor.execute("SELECT * FROM reuss WHERE flow_rate = ? ORDER BY id DESC LIMIT ? OFFSET ?", (flow_filter, entries_per_page, offset))
        elif comparison_operator == "greater_equal":
            cursor.execute("SELECT * FROM reuss WHERE flow_rate >= ? ORDER BY id DESC LIMIT ? OFFSET ?", (flow_filter, entries_per_page, offset))
    else:
        cursor.execute("SELECT * FROM reuss ORDER BY id DESC LIMIT ? OFFSET ?", (entries_per_page, offset))

    data = cursor.fetchall()
    
    # Convert timestamp to a datetime object and store in the variable 'dates' for the chart
    dates = [datetime.strptime(row[1], "%d.%m.%Y %H:%M") for row in data]
    
    # Store flow data for the chart in variable 'flow_data'
    flow_data = [row[2] for row in data]

    # Calculate total number of pages for pagination
    cursor.execute("SELECT COUNT(*) FROM reuss")
    total_entries = cursor.fetchone()[0]
    total_pages = (total_entries // entries_per_page) + (1 if total_entries % entries_per_page > 0 else 0)

    # Render HTML template and pass data
    chart_image = generate_plot(dates, flow_data)
    connection.close()
    return render_template("index.html", data=data, flow_filter=flow_filter, comparison_operator=comparison_operator, total_pages=total_pages, current_page=page, chart_image=generate_plot(dates, flow_data))
```
To create the chart, the [Matplotlib](https://matplotlib.org/) library was used. With the help of the libraries [BytesIO](https://wiki.python.org/moin/BytesIO) and [Base64](https://docs.python.org/3/library/base64.html), the created chart was saved as an image file and passed to the HTML file.
```python
# Function to generate the chart with Matplotlib
def generate_plot(dates, flow_data):
    
    # Define size, x/y axis, title, date format of the x-axis
    plt.figure(figsize=(10, 6))
    plt.plot(dates, flow_data, marker="o", linestyle="-", color="blue")
    plt.xlabel("")
    plt.ylabel("Flow rate in m³/s")
    plt.title("Flow data of the displayed measurements")
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%d.%m.%Y %H:%M"))
    plt.gcf().autofmt_xdate()

    # Save the chart in a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format="png")
    image_stream.seek(0)

    # Base64 encoding for display in HTML
    encoded_image = base64.b64encode(image_stream.read()).decode("utf-8")

    # Return chart as an image
    return f"data:image/png;base64,{encoded_image}"
```

**Website**<br>
The website was created using standard HTML. Styling was achieved using [Tailwind](https://tailwindcss.com/), and additional specific styling was added through a local CSS file.
Upon landing on the website, users are greeted with a short message indicating the current surf situation. This was implemented using a simple IF function that compares the latest flow rate.
```html
<!-- Welcome Text. Displays a short message indicating whether surfing is currently possible. The message changes based on the flow rate. -->
    <div class="flex items-center justify-center text-3xl font-bold">
        {% if data %}
            {% set last_flow_rate = data[0][2] %}
            {% if last_flow_rate >= 400 %}
                <p>Pls help me, I'm under the water. Check in again in a few days, too much water.</p>
            {% elif last_flow_rate >= 350 %}
                <p>Bring that life jacket. It's really high...</p>
            {% elif last_flow_rate >= 280 %}
                <p>Better be patient. It's going to be crowded...</p>
            {% elif last_flow_rate >= 180 %}
                <p>Call in sick! It's surfable!</p>
            {% else %}
                <p>Go back to work! It's flat...</p>
            {% endif %}
        {% endif %}
    </div>
```
In addition to the welcome message, the flow rate is highlighted if it reaches a surfable or even a dangerous level. This was done using an IF function that compares the flow rate and assigns a specific CSS class accordingly.
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
To ensure the user understands what each color represents, a legend is also provided.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

The following sections explain how to run the web application locally.

### Prerequisites

The following software and libraries are required to run the web application:
* Python: <br>
  Available from the [Python Homepage](https://www.python.org/downloads/)<br>
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

1. Clone this repository
   ```sh
   git clone https://github.com/lukasfasnacht/GLIN
   ```
2. There is already a small dataset in the database; to start with an empty database, run the following command. Otherwise, proceed to step 3.
   ```sh
   rm -r hydrodata.db
   ```
3. Run webcrawl.py in the background, optionally with log output to monitor the script
   ```sh
   python3 webcrawl.py > output.log 2>&1 &
   ```
4. Start the web application
   ```sh
   python3 flaskapp.py
   ```
5. Done, open http://127.0.0.1:5000/ in your browser

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Known Bugs

### Filter Function and Pagination
When using the filter function to search for a value, only the first 20 values are displayed due to the pagination parameters. When navigating to a new page, the filter effect is not applied on the new page. This occurs because, in the basic structure, the pagination function works independently of the filter function.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Resources

The following resources were used to support this project:

* Ingmar Beatge and the lecture materials for GLIN
* [Stackoverflow](https://stackoverflow.com/)
* [Github Copilot](https://github.com/features/copilot)
* [Flask Documentation](https://flask.palletsprojects.com/en/3.0.x/)
* [Matplotlib Documentation](https://matplotlib.org/stable/users/index)
* [Tailwind Documentation](https://v2.tailwindcss.com/docs)
* [Tailwind Tutorial](https://www.youtube.com/watch?v=pfaSUYaSgRo)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

Distributed under the MIT License. For more information, see `LICENSE.txt`.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact

Lukas Fasnacht - lukas.fasnacht@gmail.com

Project Link: [https://github.com/lukasfasnacht/GLIN](https://github.com/lukasfasnacht/GLIN)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Links and Images -->
[license-shield]: https://img.shields.io/github/license/lukasfasnacht/GLIN.svg?style=for-the-badge
[license-url]: https://github.com/lukasfasnacht/GLIN/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/lukas-fasnacht-593a67156/
[product-screenshot]: img/product-screenshot.png