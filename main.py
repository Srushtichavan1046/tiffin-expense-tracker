from datetime import datetime
import json
import os

print("=" * 35)
print("       TIFFIN EXPENSE TRACKER")
print("=" * 35)

# Get today's date
today = datetime.now()

date = today.strftime("%d-%m-%Y")
day = today.strftime("%A")

print("\nDate :", date)
print("Day  :", day)

# Get tiffin prices
lunch_price = float(input("\nEnter lunch price: ₹"))
dinner_price = float(input("Enter dinner price: ₹"))

# Ask whether lunch and dinner were taken
lunch = input("Did you take lunch? (yes/no): ").lower()
dinner = input("Did you take dinner? (yes/no): ").lower()

# Calculate total
total = 0

if lunch == "yes":
    total = total + lunch_price

if dinner == "yes":
    total = total + dinner_price

# Create today's entry
entry = {
    "date": date,
    "day": day,
    "lunch": lunch,
    "lunch_price": lunch_price if lunch == "yes" else 0,
    "dinner": dinner,
    "dinner_price": dinner_price if dinner == "yes" else 0,
    "total": total
}

# Check whether data.json already exists
if os.path.exists("data.json"):
    with open("data.json", "r") as file:
        data = json.load(file)
else:
    data = []

# Add today's entry
data.append(entry)

# Save data
with open("data.json", "w") as file:
    json.dump(data, file, indent=4)

# Display today's bill
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