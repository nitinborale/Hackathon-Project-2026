# AI Lunch Buddy
# Recommends lunch combinations based on group size,
# budget and food preference.

MENU = [
    {"name": "Veg Burger", "price": 120, "type": "veg"},
    {"name": "Veg Pizza", "price": 180, "type": "veg"},
    {"name": "Paneer Wrap", "price": 150, "type": "veg"},
    {"name": "Chicken Burger", "price": 160, "type": "non-veg"},
    {"name": "Chicken Pizza", "price": 220, "type": "non-veg"},
    {"name": "French Fries", "price": 80, "type": "veg"},
    {"name": "Coke", "price": 50, "type": "veg"},
]


def recommend_lunch(group_size, budget, preference):
    preference = preference.lower()

    if preference not in ["veg", "non-veg"]:
        return "Please choose either veg or non-veg."

    suitable_items = [
        item for item in MENU
        if item["type"] == preference
    ]

    # Find an item that fits the budget per person
    budget_per_person = budget / group_size

    suitable_items = [
        item for item in suitable_items
        if item["price"] <= budget_per_person
    ]

    if not suitable_items:
        return "No suitable lunch found within your budget."

    # Choose the most expensive suitable item
    recommendation = max(
        suitable_items,
        key=lambda item: item["price"]
    )

    total = recommendation["price"] * group_size
    remaining = budget - total

    return {
        "recommendation": recommendation["name"],
        "price_per_person": recommendation["price"],
        "group_size": group_size,
        "total_cost": total,
        "remaining_budget": remaining
    }


# Test the AI Lunch Buddy
if __name__ == "__main__":
    result = recommend_lunch(
        group_size=5,
        budget=1000,
        preference="veg"
    )

    print("\n🤖 AI LUNCH BUDDY")
    print("-------------------------")

    if isinstance(result, dict):
        print("🍽️ Recommendation:", result["recommendation"])
        print("👥 People:", result["group_size"])
        print("💰 Price per person: ₹", result["price_per_person"])
        print("💵 Total: ₹", result["total_cost"])
        print("🪙 Remaining budget: ₹", result["remaining_budget"])
    else:
        print(result)