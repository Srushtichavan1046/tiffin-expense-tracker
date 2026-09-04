from datetime import datetime

print("=" * 35)
print("       TIFFIN EXPENSE TRACKER")
print("=" * 35)

# Get today's date
today = datetime.now()

date = today.strftime("%d-%m-%Y")
day = today.strftime("%A")

print("\nDate :", date)
print("Day  :", day)

lunch_price = float(input("\nEnter lunch price: ₹"))
dinner_price = float(input("Enter dinner price: ₹"))

lunch = input("Did you take lunch? (yes/no): ").lower()
dinner = input("Did you take dinner? (yes/no): ").lower()

total = 0

if lunch == "yes":
    total = total + lunch_price

if dinner == "yes":
    total = total + dinner_price

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