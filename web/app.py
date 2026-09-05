from flask import Flask, render_template, request, redirect, url_for
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
# Default Settings
# ==========================================

DEFAULT_SETTINGS = {
    "lunch_price": 50,
    "dinner_price": 50
}


# ==========================================
# Helper: Load Data
# ==========================================

def load_data():

    if os.path.exists(DATA_FILE):

        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)

        except (json.JSONDecodeError, FileNotFoundError):
            return []

    return []


# ==========================================
# Helper: Load Settings
# ==========================================

def load_settings():

    if os.path.exists(SETTINGS_FILE):

        try:
            with open(SETTINGS_FILE, "r") as file:
                settings = json.load(file)

                # Make sure both prices exist
                settings.setdefault(
                    "lunch_price",
                    DEFAULT_SETTINGS["lunch_price"]
                )

                settings.setdefault(
                    "dinner_price",
                    DEFAULT_SETTINGS["dinner_price"]
                )

                return settings

        except (json.JSONDecodeError, FileNotFoundError):
            pass

    # Create default settings file
    with open(SETTINGS_FILE, "w") as file:
        json.dump(DEFAULT_SETTINGS, file, indent=4)

    return DEFAULT_SETTINGS.copy()


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    data = load_data()
    settings = load_settings()

    return render_template(
        "index.html",
        entries=data,
        settings=settings
    )


# ==========================================
# SAVE / UPDATE ENTRY
# ==========================================

@app.route("/save", methods=["POST"])
def save_entry():

    # --------------------------------------
    # Get Form Data
    # --------------------------------------

    selected_date = request.form.get("date")
    lunch = request.form.get("lunch")
    dinner = request.form.get("dinner")


    # --------------------------------------
    # Check Date
    # --------------------------------------

    if not selected_date:
        return "Please select a date before saving."


    # --------------------------------------
    # Check Meals
    # --------------------------------------

    if not lunch or not dinner:
        return "Please select Lunch and Dinner."


    # --------------------------------------
    # Convert Date
    # --------------------------------------

    try:

        date_object = datetime.strptime(
            selected_date,
            "%Y-%m-%d"
        )

    except ValueError:

        return "Invalid date."


    date = date_object.strftime("%d-%m-%Y")
    day = date_object.strftime("%A")


    # --------------------------------------
    # Load Prices
    # --------------------------------------

    settings = load_settings()

    lunch_price = float(settings["lunch_price"])
    dinner_price = float(settings["dinner_price"])


    # --------------------------------------
    # Calculate Total
    # --------------------------------------

    total = 0

    if lunch == "yes":
        total += lunch_price

    if dinner == "yes":
        total += dinner_price


    # --------------------------------------
    # Create Entry
    # --------------------------------------

    entry = {

        "date": date,

        "day": day,

        "lunch": lunch,

        "lunch_price":
            lunch_price if lunch == "yes" else 0,

        "dinner": dinner,

        "dinner_price":
            dinner_price if dinner == "yes" else 0,

        "total": total
    }


    # --------------------------------------
    # Load Existing Data
    # --------------------------------------

    data = load_data()


    # --------------------------------------
    # Check If Date Already Exists
    # --------------------------------------

    updated = False

    for i in range(len(data)):

        if data[i]["date"] == date:

            data[i] = entry

            updated = True

            break


    # --------------------------------------
    # Add New Entry
    # --------------------------------------

    if not updated:

        data.append(entry)


    # --------------------------------------
    # Sort Entries By Date
    # --------------------------------------

    data.sort(
        key=lambda x:
        datetime.strptime(
            x["date"],
            "%d-%m-%Y"
        )
    )


    # --------------------------------------
    # Save Data
    # --------------------------------------

    with open(DATA_FILE, "w") as file:

        json.dump(
            data,
            file,
            indent=4
        )


    # --------------------------------------
    # Return To Home
    # --------------------------------------

    return redirect(url_for("home"))


# ==========================================
# UPDATE PRICES
# ==========================================

@app.route("/update-settings", methods=["POST"])
def update_settings():

    try:

        lunch_price = float(
            request.form.get("lunch_price")
        )

        dinner_price = float(
            request.form.get("dinner_price")
        )

    except (TypeError, ValueError):

        return "Please enter valid prices."


    # --------------------------------------
    # Prevent Negative Prices
    # --------------------------------------

    if lunch_price < 0 or dinner_price < 0:

        return "Price cannot be negative."


    # --------------------------------------
    # Save New Settings
    # --------------------------------------

    settings = {

        "lunch_price": lunch_price,

        "dinner_price": dinner_price
    }


    with open(SETTINGS_FILE, "w") as file:

        json.dump(
            settings,
            file,
            indent=4
        )


    return redirect(url_for("home"))


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )