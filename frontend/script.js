const API_URL = "http://127.0.0.1:5000";

async function loadOrders() {
    try {
        const response = await fetch(`${API_URL}/orders`);

        if (!response.ok) {
            throw new Error("Failed to load orders");
        }

        const orders = await response.json();

        const orderList = document.getElementById("orderList");
        orderList.innerHTML = "";

        orders.forEach(order => {
            displayOrder(order);
        });

        updateSummary();

    } catch (error) {
        console.error("Error loading orders:", error);
        alert("Could not connect to the backend.");
    }
}


async function addOrder() {
    const name = document.getElementById("name").value.trim();

    const foodSelect = document.getElementById("food");
    const food = foodSelect.value;

    const price = Number(
        foodSelect.options[foodSelect.selectedIndex].dataset.price
    );

    const qty = Number(document.getElementById("qty").value);

    if (name === "" || qty <= 0) {
        alert("Please enter valid details");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/orders`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: name,
                food_item: food,
                quantity: qty,
                price: price
            })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.error || "Failed to add order");
            return;
        }

        displayOrder(data.order[0]);

        document.getElementById("name").value = "";
        document.getElementById("qty").value = "";

        updateSummary();

    } catch (error) {
        console.error("Error:", error);
        alert("Could not connect to the backend.");
    }
}


function displayOrder(order) {
    const orderList = document.getElementById("orderList");

    const li = document.createElement("li");

    li.dataset.id = order.id;

    li.innerHTML = `
        <span>
            <strong>${order.name}</strong>
            ordered
            <strong>${order.quantity}</strong>
            ${order.food_item}
            - ₹${Number(order.total).toFixed(2)}
        </span>

        <button onclick="removeOrder(${order.id}, this)">
            Remove
        </button>
    `;

    orderList.appendChild(li);
}


async function removeOrder(orderId, button) {
    try {
        const response = await fetch(
            `${API_URL}/orders/${orderId}`,
            {
                method: "DELETE"
            }
        );

        const data = await response.json();

        if (!response.ok) {
            alert(data.error || "Failed to delete order");
            return;
        }

        button.parentElement.remove();

        updateSummary();

    } catch (error) {
        console.error("Error:", error);
        alert("Could not connect to backend.");
    }
}


async function updateSummary() {
    try {
        const response = await fetch(`${API_URL}/summary`);

        if (!response.ok) {
            throw new Error("Failed to get summary");
        }

        const data = await response.json();

        document.getElementById("total").textContent =
            `₹${Number(data.total_cost).toFixed(2)}`;

        document.getElementById("orderCount").textContent =
            data.order_count;

        updatePeopleCount();

    } catch (error) {
        console.error("Summary error:", error);
    }
}


function updatePeopleCount() {
    const names = new Set();

    const orders = document.querySelectorAll("#orderList li");

    orders.forEach(order => {
        const strong = order.querySelector("strong");

        if (strong) {
            names.add(strong.textContent);
        }
    });

    document.getElementById("peopleCount").textContent = names.size;
}


window.addEventListener("DOMContentLoaded", () => {
    loadOrders();
});