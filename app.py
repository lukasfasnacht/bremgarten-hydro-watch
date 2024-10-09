# Import various Python modules for the web server
from flask import Flask, render_template, request
import sqlite3
import matplotlib.pyplot as plt
plt.switch_backend("Agg")
from io import BytesIO
import base64
from datetime import datetime

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)