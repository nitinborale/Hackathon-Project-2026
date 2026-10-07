let totalCost = 0;
let orderCount = 0;

let people = new Set();

function addOrder() {

    const name =
        document.getElementById("name")
        .value
        .trim();

    const foodSelect =
        document.getElementById("food");

    const food =
        foodSelect.value;

    const price =
        Number(
            foodSelect.options[
                foodSelect.selectedIndex
            ].dataset.price
        );

    const qty =
        Number(
            document.getElementById("qty").value
        );

    if (name === "" || qty <= 0) {
        alert("Please enter valid details");
        return;
    }

    const cost = price * qty;

    totalCost += cost;
    orderCount++;

    people.add(name);

    document.getElementById("peopleCount")
        .textContent = people.size;

    const li =
        document.createElement("li");

    li.innerHTML = `
        <span>
            <strong>${name}</strong>
            ordered
            <strong>${qty}</strong>
            ${food}
            - ₹${cost}
        </span>

        <button onclick="removeOrder(this, ${cost})">
            ❌
        </button>
    `;

    document
        .getElementById("orderList")
        .appendChild(li);

    document
        .getElementById("total")
        .textContent = totalCost;

    document
        .getElementById("orderCount")
        .textContent = orderCount;

    document.getElementById("name").value = "";
    document.getElementById("qty").value = "";
}

function removeOrder(button, cost) {

    button.parentElement.remove();

    totalCost -= cost;
    orderCount--;

    document.getElementById("total")
        .textContent = totalCost;

    document.getElementById("orderCount")
        .textContent = orderCount;
}