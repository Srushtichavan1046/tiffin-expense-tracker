from datetime import datetime
import json
import os

print("=" * 35)
print("       TIFFIN EXPENSE TRACKER")
print("=" * 35)

# -------------------------------
# Load tiffin prices
# -------------------------------

if os.path.exists("settings.json"):
    with open("settings.json", "r") as file:
        settings = json.load(file)

    lunch_price = settings["lunch_price"]
    dinner_price = settings["dinner_price"]

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


# -------------------------------
# Get today's date
# -------------------------------

today = datetime.now()

date = today.strftime("%d-%m-%Y")
day = today.strftime("%A")

print("\nDate :", date)
print("Day  :", day)

print("\nLunch price :", lunch_price)
print("Dinner price:", dinner_price)


# -------------------------------
# Ask about lunch and dinner
# -------------------------------

lunch = input("\nDid you take lunch? (yes/no): ").lower()
dinner = input("Did you take dinner? (yes/no): ").lower()


# -------------------------------
# Calculate total
# -------------------------------

total = 0

if lunch == "yes":
    total = total + lunch_price

if dinner == "yes":
    total = total + dinner_price


# -------------------------------
# Create today's entry
# -------------------------------

entry = {
    "date": date,
    "day": day,
    "lunch": lunch,
    "lunch_price": lunch_price if lunch == "yes" else 0,
    "dinner": dinner,
    "dinner_price": dinner_price if dinner == "yes" else 0,
    "total": total
}


# -------------------------------
# Load existing entries
# -------------------------------

if os.path.exists("data.json"):
    with open("data.json", "r") as file:
        data = json.load(file)
else:
    data = []


# -------------------------------
# Save today's entry
# -------------------------------

data.append(entry)

with open("data.json", "w") as file:
    json.dump(data, file, indent=4)


# -------------------------------
# Display today's bill
# -------------------------------

print("\n------ Today's Bill ------")

if lunch == "yes":
    print("Lunch  : ₹", lunch_price)
else:
    print("Lunch  : Not Taken")

if dinner == "yes":
    print("Dinner : ₹", dinner_price)
else:
    print("Dinner : Not Taken")

print("--------------------------")
print("Date   :", date)
print("Day    :", day)
print("Total  : ₹", total)

print("\nEntry saved successfully!")