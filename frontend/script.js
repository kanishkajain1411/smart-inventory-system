const API_URL = "http://98.84.159.185:5000/api";

// ================= Dashboard Cards =================

fetch(`${API_URL}/dashboard`)
    .then(res => res.json())
    .then(data => {

        document.getElementById("totalProducts").textContent = data.total_products;
        document.getElementById("totalCategories").textContent = data.total_categories;
        document.getElementById("lowStock").textContent = data.low_stock_products;
        document.getElementById("inventoryValue").textContent = "₹ " + data.total_inventory_value;

    })
    .catch(error => console.error(error));


// ================= Recent Products =================

fetch(`${API_URL}/dashboard/recent-products`)
    .then(res => res.json())
    .then(products => {

        const table = document.getElementById("recentProductsTable");

        table.innerHTML = "";

        products.forEach(product => {

            let colorClass = "";

            if (product.status === "Available") {
                colorClass = "available";
            }
            else if (product.status === "Low Stock") {
                colorClass = "low";
            }
            else {
                colorClass = "out";
            }

            table.innerHTML += `
                <tr>
                    <td>${product.name}</td>
                    <td>${product.category}</td>
                    <td>${product.quantity}</td>
                    <td class="${colorClass}">
                        ${product.status}
                    </td>
                </tr>
            `;

        });

    })
    .catch(error => console.error(error));