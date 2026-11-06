from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Temporary storage for orders
orders = []

# Restaurant menu
menu = [
    {"id": 1, "name": "Chicken Burger", "price": 45, "requires_preparation": True},
    {"id": 2, "name": "Fries", "price": 20, "requires_preparation": True},
    {"id": 3, "name": "Chicken Wings", "price": 50, "requires_preparation": True},
    {"id": 4, "name": "Soft Drink", "price": 15, "requires_preparation": False},
]


@app.route("/")
def home():

    pending_orders = sum(1 for order in orders if order["status"] == "Received")

    preparing_orders = sum(1 for order in orders if order["status"] == "Preparing")

    ready_orders = sum(1 for order in orders if order["status"] == "Ready")

    completed_sales = sum(
        order["price"] for order in orders if order["status"] == "Completed"
    )

    return render_template(
        "index.html",
        orders=orders,
        menu=menu,
        pending_orders=pending_orders,
        preparing_orders=preparing_orders,
        ready_orders=ready_orders,
        completed_sales=completed_sales,
    )


@app.route("/create-order", methods=["POST"])
def create_order():

    customer_name = request.form["customer_name"]
    item_id = int(request.form["item"])

    selected_item = next(item for item in menu if item["id"] == item_id)

    order = {
        "id": len(orders) + 1,
        "customer": customer_name,
        "item": selected_item["name"],
        "price": selected_item["price"],
        "status": "Received" if selected_item["requires_preparation"] else "Ready",
    }

    orders.append(order)

    return redirect("/")


@app.route("/update-status/<int:order_id>", methods=["POST"])
def update_status(order_id):

    for order in orders:

        if order["id"] == order_id:

            current_status = order["status"]

            status_transitions = {
                "Received": "Preparing",
                "Preparing": "Ready",
                "Ready": "Completed",
            }

            if current_status in status_transitions:
                order["status"] = status_transitions[current_status]

            break

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
