from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client
from dotenv import dotenv_values
from pathlib import Path


# ==========================================
# FIND PROJECT ROOT AND .ENV FILE
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"


# ==========================================
# READ .ENV FILE
# ==========================================

config = dotenv_values(ENV_FILE)

SUPABASE_URL = config.get("SUPABASE_URL")
SUPABASE_KEY = config.get("SUPABASE_KEY")


# ==========================================
# CHECK SUPABASE CREDENTIALS
# ==========================================

print("ENV FILE:", ENV_FILE)
print("ENV EXISTS:", ENV_FILE.exists())
print("SUPABASE URL LOADED:", bool(SUPABASE_URL))
print("SUPABASE KEY LOADED:", bool(SUPABASE_KEY))


if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "SUPABASE_URL or SUPABASE_KEY is missing from .env file"
    )


# ==========================================
# CONNECT TO SUPABASE
# ==========================================

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# ==========================================
# CREATE FLASK APP
# ==========================================

app = Flask(__name__)

CORS(app)
# Home / Test Route
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Lunch Order Pool API is running!"
    })


# Get All Orders
@app.route("/orders", methods=["GET"])
def get_orders():
    response = (
        supabase
        .table("orders")
        .select("*")
        .order("id", desc=True)
        .execute()
    )

    return jsonify(response.data)


# Add New Order
@app.route("/orders", methods=["POST"])
def add_order():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request data is missing"}), 400

    name = data.get("name")
    food_item = data.get("food_item")
    quantity = data.get("quantity")
    price = data.get("price")

    if not name or not food_item or quantity is None or price is None:
        return jsonify({"error": "All fields are required"}), 400

    try:
        quantity = int(quantity)
        price = float(price)
    except (ValueError, TypeError):
        return jsonify({
            "error": "Quantity and price must be numbers"
        }), 400

    if quantity <= 0:
        return jsonify({
            "error": "Quantity must be greater than 0"
        }), 400

    if price < 0:
        return jsonify({
            "error": "Price cannot be negative"
        }), 400

    total = quantity * price

    order = {
        "name": name,
        "food_item": food_item,
        "quantity": quantity,
        "price": price,
        "total": total
    }

    response = (
        supabase
        .table("orders")
        .insert(order)
        .execute()
    )

    return jsonify({
        "message": "Order added successfully",
        "order": response.data
    }), 201


# Update Order
@app.route("/orders/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request data is missing"
        }), 400

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

    response = (
        supabase
        .table("orders")
        .update(updated_order)
        .eq("id", order_id)
        .execute()
    )

    if not response.data:
        return jsonify({
            "error": "Order not found"
        }), 404

    return jsonify({
        "message": "Order updated successfully",
        "order": response.data
    })


# Delete Order
@app.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    response = (
        supabase
        .table("orders")
        .delete()
        .eq("id", order_id)
        .execute()
    )

    if not response.data:
        return jsonify({
            "error": "Order not found"
        }), 404

    return jsonify({
        "message": "Order deleted successfully"
    })


# Get Summary
@app.route("/summary", methods=["GET"])
def get_summary():
    response = (
        supabase
        .table("orders")
        .select("total")
        .execute()
    )

    orders = response.data

    total_cost = sum(
        float(order["total"])
        for order in orders
    )

    return jsonify({
        "order_count": len(orders),
        "total_cost": total_cost
    })


# Start Flask Server
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )


# ==========================================
# HOME / TEST ROUTE
# ==========================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "Lunch Order Pool API is running!"
    })


# ==========================================
# GET ALL ORDERS
# ==========================================

# Get All Orders
@app.route("/orders", methods=["GET"])
def get_orders():
    response = (
        supabase
        .table("orders")
        .select("*")
        .execute()
    )

    return jsonify(response.data)


# ==========================================
# ADD NEW ORDER
# ==========================================

@app.route("/orders", methods=["POST"])
def add_order():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request data is missing"
        }), 400

    name = data.get("name")
    food_item = data.get("food_item")
    quantity = data.get("quantity")
    price = data.get("price")


    # Check required fields

    if (
        not name
        or not food_item
        or quantity is None
        or price is None
    ):

        return jsonify({
            "error": "All fields are required"
        }), 400


    # Convert quantity and price

    try:

        quantity = int(quantity)
        price = float(price)

    except (ValueError, TypeError):

        return jsonify({
            "error": "Quantity and price must be numbers"
        }), 400


    # Validate values

    if quantity <= 0:

        return jsonify({
            "error": "Quantity must be greater than 0"
        }), 400


    if price < 0:

        return jsonify({
            "error": "Price cannot be negative"
        }), 400


    # Calculate total

    total = quantity * price


    # Create order object

    order = {
        "name": name,
        "food_item": food_item,
        "quantity": quantity,
        "price": price,
        "total": total
    }


    # Insert order into Supabase

    response = (
        supabase
        .table("orders")
        .insert(order)
        .execute()
    )


    return jsonify({
        "message": "Order added successfully",
        "order": response.data
    }), 201


# ==========================================
# UPDATE ORDER
# ==========================================

@app.route("/orders/<int:order_id>", methods=["PUT"])
def update_order(order_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request data is missing"
        }), 400

    name = data.get("name")
    food_item = data.get("food_item")
    quantity = data.get("quantity")
    price = data.get("price")


    if (
        not name
        or not food_item
        or quantity is None
        or price is None
    ):

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


    response = (
        supabase
        .table("orders")
        .update(updated_order)
        .eq("id", order_id)
        .execute()
    )


    if not response.data:

        return jsonify({
            "error": "Order not found"
        }), 404


    return jsonify({
        "message": "Order updated successfully",
        "order": response.data
    })


# ==========================================
# DELETE ORDER
# ==========================================

@app.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):

    response = (
        supabase
        .table("orders")
        .delete()
        .eq("id", order_id)
        .execute()
    )


    if not response.data:

        return jsonify({
            "error": "Order not found"
        }), 404


    return jsonify({
        "message": "Order deleted successfully"
    })


# ==========================================
# GET SUMMARY
# ==========================================

@app.route("/summary", methods=["GET"])
def get_summary():

    response = (
        supabase
        .table("orders")
        .select("total")
        .execute()
    )


    orders = response.data


    total_cost = sum(
        float(order["total"])
        for order in orders
    )


    return jsonify({
        "order_count": len(orders),
        "total_cost": total_cost
    })


# ==========================================
# START FLASK SERVER
# ==========================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )