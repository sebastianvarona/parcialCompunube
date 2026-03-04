function getOrders() {
    fetch('http://192.168.1.81:5004/api/orders', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);

        // Get table body
        var orderListBody = document.querySelector('#order-list tbody');
        orderListBody.innerHTML = ''; // Clear previous data

        // Loop through orders and populate table rows
        data.forEach(order => {
            var row = document.createElement('tr');

            // ID
            var idCell = document.createElement('td');
            idCell.textContent = order.id;
            row.appendChild(idCell);

            // User Name
            var userNameCell = document.createElement('td');
            userNameCell.textContent = order.user_name;
            row.appendChild(userNameCell);

            // User Email
            var userEmailCell = document.createElement('td');
            userEmailCell.textContent = order.user_email;
            row.appendChild(userEmailCell);

            // Total
            var totalCell = document.createElement('td');
            totalCell.textContent = '$' + order.total.toFixed(2);
            row.appendChild(totalCell);

            // Created At
            var createdAtCell = document.createElement('td');
            createdAtCell.textContent = new Date(order.created_at).toLocaleString();
            row.appendChild(createdAtCell);

            // Items
            var itemsCell = document.createElement('td');
            var itemsText = order.items.map(item =>
                `${item.product_name} (x${item.quantity}) - $${item.price}`
            ).join(', ');
            itemsCell.textContent = itemsText;
            row.appendChild(itemsCell);

            orderListBody.appendChild(row);
        });
    })
    .catch(error => console.error('Error:', error));
}
