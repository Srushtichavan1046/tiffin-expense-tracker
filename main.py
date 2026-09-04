print("=" * 35)
print("       TIFFIN EXPENSE TRACKER")
print("=" * 35)

lunch_price = float(input("Enter lunch price: ₹"))
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
print("Total  : ₹", total)