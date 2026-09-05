from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import json
import os


# ==========================================
# FLASK APP
# ==========================================

app = Flask(__name__)


# ==========================================
# FILE LOCATIONS
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_FILE = os.path.join(BASE_DIR, "data.json")
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")


# ==========================================
# DEFAULT PRICES
# ==========================================

DEFAULT_SETTINGS = {
    "lunch_price": 50,
    "dinner_price": 50
}


# ==========================================
# LOAD DATA
# ==========================================

def load_data():

    if not os.path.exists(DATA_FILE):
        return []

    try:

        with open(DATA_FILE, "r") as file:
            data = json.load(file)

            if isinstance(data, list):
                return data

            return []

    except (json.JSONDecodeError, FileNotFoundError):

        return []


# ==========================================
# SAVE DATA
# ==========================================

def save_data(data):

    with open(DATA_FILE, "w") as file:

        json.dump(
            data,
            file,
            indent=4
        )


# ==========================================
# LOAD SETTINGS
# ==========================================

def load_settings():

    if os.path.exists(SETTINGS_FILE):

        try:

            with open(SETTINGS_FILE, "r") as file:

                settings = json.load(file)

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


    # Create default settings

    settings = DEFAULT_SETTINGS.copy()

    with open(SETTINGS_FILE, "w") as file:

        json.dump(
            settings,
            file,
            indent=4
        )

    return settings


# ==========================================
# SAVE SETTINGS
# ==========================================

def save_settings(settings):

    with open(SETTINGS_FILE, "w") as file:

        json.dump(
            settings,
            file,
            indent=4
        )


# ==========================================
# HOME
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
    # Get form values
    # --------------------------------------

    selected_date = request.form.get("date")
    lunch = request.form.get("lunch")
    dinner = request.form.get("dinner")


    # --------------------------------------
    # Validate date
    # --------------------------------------

    if not selected_date:

        return "Please select a date before saving."


    # --------------------------------------
    # Validate meals
    # --------------------------------------

    if lunch not in ["yes", "no"]:

        return "Please select Lunch."


    if dinner not in ["yes", "no"]:

        return "Please select Dinner."


    # --------------------------------------
    # Convert date
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
    # Load current prices
    # --------------------------------------

    settings = load_settings()

    lunch_price = float(
        settings["lunch_price"]
    )

    dinner_price = float(
        settings["dinner_price"]
    )


    # --------------------------------------
    # Calculate prices
    # --------------------------------------

    actual_lunch_price = (
        lunch_price
        if lunch == "yes"
        else 0
    )

    actual_dinner_price = (
        dinner_price
        if dinner == "yes"
        else 0
    )


    total = (
        actual_lunch_price
        + actual_dinner_price
    )


    # --------------------------------------
    # Create entry
    # --------------------------------------

    entry = {

        "date": date,

        "day": day,

        "lunch": lunch,

        "lunch_price": actual_lunch_price,

        "dinner": dinner,

        "dinner_price": actual_dinner_price,

        "total": total
    }


    # --------------------------------------
    # Load existing entries
    # --------------------------------------

    data = load_data()


    # --------------------------------------
    # Update existing date
    # --------------------------------------

    updated = False

    for i, old_entry in enumerate(data):

        if old_entry.get("date") == date:

            data[i] = entry

            updated = True

            break


    # --------------------------------------
    # Add new date
    # --------------------------------------

    if not updated:

        data.append(entry)


    # --------------------------------------
    # Sort by date
    # --------------------------------------

    try:

        data.sort(
            key=lambda x: datetime.strptime(
                x["date"],
                "%d-%m-%Y"
            )
        )

    except (ValueError, KeyError):

        pass


    # --------------------------------------
    # Save
    # --------------------------------------

    save_data(data)


    return redirect(
        url_for("home")
    )


# ==========================================
# UPDATE TIFFIN PRICES
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
    # Validate prices
    # --------------------------------------

    if lunch_price < 0:

        return "Lunch price cannot be negative."


    if dinner_price < 0:

        return "Dinner price cannot be negative."


    # --------------------------------------
    # Save new settings
    # --------------------------------------

    settings = {

        "lunch_price": lunch_price,

        "dinner_price": dinner_price
    }

    save_settings(settings)


    # --------------------------------------
    # Update existing entries
    # --------------------------------------

    data = load_data()


    for entry in data:

        if entry.get("lunch") == "yes":

            entry["lunch_price"] = lunch_price

        else:

            entry["lunch_price"] = 0


        if entry.get("dinner") == "yes":

            entry["dinner_price"] = dinner_price

        else:

            entry["dinner_price"] = 0


        entry["total"] = (
            entry["lunch_price"]
            + entry["dinner_price"]
        )


    # --------------------------------------
    # Save updated entries
    # --------------------------------------

    save_data(data)


    return redirect(
        url_for("home")
    )


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )