// Fetch and render Sales Chart
fetch('/api/sales-data/')
.then(response => response.json())
.then(data => {
    const ctx = document.getElementById('salesChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Revenue',
                data: data.values,
                backgroundColor: 'rgba(75, 192, 192, 0.6)'
            }]
        },
        options: { responsive: true, plugins: { legend: { position: 'top' } } }
    });

    // Set KPI cards
    const totalRevenue = data.values.reduce((a, b) => a + b, 0);
    document.getElementById('totalRevenue').textContent = `₹${totalRevenue.toFixed(2)}`;
    document.getElementById('totalOrders').textContent = data.labels.length;
    document.getElementById('topProduct').textContent = data.labels[data.values.indexOf(Math.max(...data.values))];
});

// Fetch and render Inventory Chart
fetch('/api/inventory-data/')
.then(response => response.json())
.then(data => {
    const ctx = document.getElementById('inventoryChart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Stock Levels',
                data: data.values,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(75, 192, 192, 0.6)'
                ]
            }]
        },
        options: { responsive: true }
    });

    // Low stock KPI
    const lowStockCount = data.values.filter(v => v < 10).length;
    document.getElementById('lowStock').textContent = lowStockCount;
});
