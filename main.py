from datetime import datetime
import json
import os


# ==========================================
# Load Settings
# ==========================================

def load_settings():

    if os.path.exists("settings.json"):

        with open("settings.json", "r") as file:
            settings = json.load(file)

    else:

        print("\nSet your tiffin prices")

        lunch_price = float(input("Enter lunch price: ₹"))
        dinner_price = float(input("Enter dinner price: ₹"))

        settings = {
            "lunch_price": lunch_price,
            "dinner_price": dinner_price
        }

        with open("settings.json", "w") as file:
            json.dump(settings, file, indent=4)

        print("\nPrices saved successfully!")

    return settings


# ==========================================
# Add Today's Entry
# ==========================================

def add_entry(settings):

    today = datetime.now()

    date = today.strftime("%d-%m-%Y")
    day = today.strftime("%A")

    lunch_price = settings["lunch_price"]
    dinner_price = settings["dinner_price"]

    print("\n------------------------------")
    print("       ADD TODAY'S ENTRY")
    print("------------------------------")

    print("Date :", date)
    print("Day  :", day)

    lunch = input("\nDid you take lunch? (yes/no): ").lower()
    dinner = input("Did you take dinner? (yes/no): ").lower()

    total = 0

    if lunch == "yes":
        total = total + lunch_price

    if dinner == "yes":
        total = total + dinner_price

    entry = {
        "date": date,
        "day": day,
        "lunch": lunch,
        "lunch_price": lunch_price if lunch == "yes" else 0,
        "dinner": dinner,
        "dinner_price": dinner_price if dinner == "yes" else 0,
        "total": total
    }

    # Load existing data
    if os.path.exists("data.json"):

        with open("data.json", "r") as file:
            data = json.load(file)

    else:

        data = []

    # Add entry
    data.append(entry)

    # Save entry
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

    print("\nEntry saved successfully!")
    print("Today's total: ₹", total)


# ==========================================
# View All Entries
# ==========================================

def view_entries():

    print("\n------------------------------")
    print("         ALL ENTRIES")
    print("------------------------------")

    if not os.path.exists("data.json"):

        print("No entries found.")

        return

    with open("data.json", "r") as file:
        data = json.load(file)

    if len(data) == 0:

        print("No entries found.")

        return

    for entry in data:

        print("\nDate   :", entry["date"])
        print("Day    :", entry["day"])

        if entry["lunch"] == "yes":
            print("Lunch  : ₹", entry["lunch_price"])
        else:
            print("Lunch  : Not Taken")

        if entry["dinner"] == "yes":
            print("Dinner : ₹", entry["dinner_price"])
        else:
            print("Dinner : Not Taken")

        print("Total  : ₹", entry["total"])
        print("------------------------------")


# ==========================================
# Change Tiffin Prices
# ==========================================

def change_prices(settings):

    print("\n------------------------------")
    print("       CHANGE TIFFIN PRICE")
    print("------------------------------")

    print("Current lunch price :", settings["lunch_price"])
    print("Current dinner price:", settings["dinner_price"])

    lunch_price = float(input("\nEnter new lunch price: ₹"))
    dinner_price = float(input("Enter new dinner price: ₹"))

    settings["lunch_price"] = lunch_price
    settings["dinner_price"] = dinner_price

    with open("settings.json", "w") as file:
        json.dump(settings, file, indent=4)

    print("\nPrices updated successfully!")


# ==========================================
# Main Program
# ==========================================

settings = load_settings()

while True:

    print("\n")
    print("=" * 35)
    print("       TIFFIN EXPENSE TRACKER")
    print("=" * 35)

    print("\n1. Add today's entry")
    print("2. View all entries")
    print("3. Change tiffin prices")
    print("4. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":

        add_entry(settings)

    elif choice == "2":

        view_entries()

    elif choice == "3":

        change_prices(settings)

    elif choice == "4":

        print("\nThank you for using Tiffin Expense Tracker!")
        break

    else:

        print("\nInvalid choice. Please try again.")