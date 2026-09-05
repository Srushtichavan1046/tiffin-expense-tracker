from flask import Flask, render_template, request
from datetime import datetime
import json
import os


# ==========================================
# Flask App
# ==========================================

app = Flask(__name__)


# ==========================================
# File Locations
# ==========================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_FILE = os.path.join(BASE_DIR, "data.json")
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")


# ==========================================
# Home Page
# ==========================================

@app.route("/")
def home():

    # Load saved entries
    if os.path.exists(DATA_FILE):

        with open(DATA_FILE, "r") as file:
            data = json.load(file)

    else:

        data = []

    return render_template("index.html", entries=data)

# ==========================================
# Save Today's Entry
# ==========================================

@app.route("/save", methods=["POST"])
def save_entry():

    lunch = request.form.get("lunch")
    dinner = request.form.get("dinner")

    # Get today's date
    today = datetime.now()

    date = today.strftime("%d-%m-%Y")
    day = today.strftime("%A")

    # Load tiffin prices
    with open(SETTINGS_FILE, "r") as file:
        settings = json.load(file)

    lunch_price = settings["lunch_price"]
    dinner_price = settings["dinner_price"]

    # Calculate total
    total = 0

    if lunch == "yes":
        total = total + lunch_price

    if dinner == "yes":
        total = total + dinner_price

    # Create entry
    entry = {
        "date": date,
        "day": day,
        "lunch": lunch,
        "lunch_price": lunch_price if lunch == "yes" else 0,
        "dinner": dinner,
        "dinner_price": dinner_price if dinner == "yes" else 0,
        "total": total
    }

    # Load existing entries
    if os.path.exists(DATA_FILE):

        with open(DATA_FILE, "r") as file:
            data = json.load(file)

    else:

        data = []

    # Add new entry
    data.append(entry)

    # Save entry
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

    return render_template("index.html", entries=data)


# ==========================================
# Run Application
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)