from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Get Supabase details
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Connect to Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Create Flask app
app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "message": "Lunch Order Pool API is running!"
    })


@app.route("/orders", methods=["GET"])
def get_orders():
    response = supabase.table("orders").select("*").order(
        "id", desc=True
    ).execute()

    return jsonify(response.data)


@app.route("/orders", methods=["POST"])
def add_order():
    data = request.get_json()

    name = data.get("name")
    food_item = data.get("food_item")
    quantity = data.get("quantity")
    price = data.get("price")

    if not name or not food_item or quantity is None or price is None:
        return jsonify({
            "error": "All fields are required"
        }), 400

    try:
        quantity = int(quantity)
        price = float(price)
    except (ValueError, TypeError):
        return jsonify({
            "error": "Quantity and price must be numbers"
        }), 400

    if quantity <= 0 or price < 0:
        return jsonify({
            "error": "Invalid quantity or price"
        }), 400

    total = quantity * price

    order = {
        "name": name,
        "food_item": food_item,
        "quantity": quantity,
        "price": price,
        "total": total
    }

    response = supabase.table("orders").insert(order).execute()

    return jsonify({
        "message": "Order added successfully",
        "order": response.data
    }), 201

@app.route("/orders/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    data = request.get_json()

    name = data.get("name")
    food_item = data.get("food_item")
    quantity = data.get("quantity")
    price = data.get("price")

    if not name or not food_item or quantity is None or price is None:
        return jsonify({
            "error": "All fields are required"
        }), 400

    try:
        quantity = int(quantity)
        price = float(price)
    except (ValueError, TypeError):
        return jsonify({
            "error": "Quantity and price must be numbers"
        }), 400

    if quantity <= 0 or price < 0:
        return jsonify({
            "error": "Invalid quantity or price"
        }), 400

    total = quantity * price

    updated_order = {
        "name": name,
        "food_item": food_item,
        "quantity": quantity,
        "price": price,
        "total": total
    }

    response = supabase.table("orders").update(
        updated_order
    ).eq("id", order_id).execute()

    if not response.data:
        return jsonify({
            "error": "Order not found"
        }), 404

    return jsonify({
        "message": "Order updated successfully",
        "order": response.data
    })
@app.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    response = supabase.table("orders").delete().eq(
        "id", order_id
    ).execute()

    if not response.data:
        return jsonify({
            "error": "Order not found"
        }), 404

    return jsonify({
        "message": "Order deleted successfully"
    })


@app.route("/summary", methods=["GET"])
def get_summary():
    response = supabase.table("orders").select(
        "total"
    ).execute()

    orders = response.data

    total_cost = sum(float(order["total"]) for order in orders)

    return jsonify({
        "order_count": len(orders),
        "total_cost": total_cost
    })


if __name__ == "__main__":
    app.run(debug=True)