
let allOrders = [];
let filteredOrders = [];

function fetchAndRenderOrders() {
    $.get(orderListApiUrl, function (response) {
        if (response) {
            allOrders = response.sort((a, b) => new Date(b.datetime) - new Date(a.datetime));
            // renderTable(allOrders);
            filteredOrders = [...allOrders]; // default to all
            renderTable(filteredOrders);
        }
    });
}

function renderTable(data) {
    const tbody = $("#orderTableBody");
    tbody.empty();

    let totalCost = 0;

    data.forEach(order => {
        totalCost += parseFloat(order.total);
        const row = `
            <tr>
                <td>${order.datetime}</td>
                <td>${order.order_id}</td>
                <td>${order.customer_name}</td>
                <td>${order.total.toFixed(2)} Ugx</td>
                <td><a href="order-details.html?order_id=${order.order_id}" class="btn btn-sm btn-info">View</a></td>
            </tr>
        `;
        tbody.append(row);
    });

    // Show total ABOVE the table
    $("#transactionTotal").html(`
        <div class="alert alert-primary mb-3" style="text-align: end">
            <b>Total Transactions : ${totalCost.toFixed(2)} Ugx</b>
        </div>
    `);
}

function filterTransactionsByDate(filter) {
    const today = new Date();
    // const filtered = allOrders.filter(order => {
    filteredOrders = allOrders.filter(order => {
        const orderDate = new Date(order.datetime);

        switch (filter) {
            case 'Today':
                return isSameDay(orderDate, today);
            case 'Yesterday':
                const yesterday = new Date();
                yesterday.setDate(today.getDate() - 1);
                return isSameDay(orderDate, yesterday);
            case 'ThisWeek':
                const startOfWeek = new Date(today);
                startOfWeek.setDate(today.getDate() - today.getDay()); // Sunday
                startOfWeek.setHours(0, 0, 0, 0);
                return orderDate >= startOfWeek;
            case 'ThisMonth':
                return orderDate.getMonth() === today.getMonth() &&
                    orderDate.getFullYear() === today.getFullYear();
            default:
                return true; // All
        }
    });

    // renderTable(filtered);
    renderTable(filteredOrders);
}

function isSameDay(d1, d2) {
    return d1.getDate() === d2.getDate() &&
        d1.getMonth() === d2.getMonth() &&
        d1.getFullYear() === d2.getFullYear();
}

// On document ready
$(function () {
    fetchAndRenderOrders();

    // Handle date filter change
    $('#dateFilter').on('change', function () {
        const selected = $(this).val();
        filterTransactionsByDate(selected);
    });
});

async function getOrderDetails(orderId) {
    try {
        const res = await fetch(`http://localhost:5000/getOrderDetails/${orderId}`);
        const data = await res.json();
        return data;
    } catch (err) {
        console.error("Error fetching order details:", err);
        return [];
    }
}

async function exportOrdersCombined(format) {
    let combinedData = [];
    for (let order of filteredOrders) {
        const details = await getOrderDetails(order.order_id);
        details.forEach(item => {
            combinedData.push({
                "Order Date": order.datetime,
                "Order Number": order.order_id,
                "Cashiers Name": order.customer_name,
                "Product": item.product_name,
                "Unit Price": item.price_per_unit.toFixed(2),
                "Quantity": item.quantity,
                "Total Price": parseFloat(item.total_price).toFixed(2)
            });
        });
    }
    console.log("Combined Data:", combinedData);
    if (!combinedData.length) {
        alert("No data to export!");
        return;
    }
    if (format === "csv") exportCSV(combinedData, "orders_combined.csv");
    else if (format === "excel") exportExcel(combinedData, "orders_combined.xlsx");
    else if (format === "pdf") exportPDF(combinedData, "orders_combined.pdf");
}

// --- Helpers ---
function exportCSV(data, filename) {
    const keys = Object.keys(data[0]);
    const csv = [
        keys.join(","),
        ...data.map(row => keys.map(k => row[k]).join(","))
    ].join("\n");

    const blob = new Blob([csv], { type: "text/csv" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
}

function exportExcel(data, filename) {
    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.json_to_sheet(data);
    XLSX.utils.book_append_sheet(wb, ws, "Orders");
    XLSX.writeFile(wb, filename);
}

function exportPDF(data, filename) {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    doc.autoTable({
        head: [Object.keys(data[0])],
        body: data.map(d => Object.values(d))
    });
    doc.save(filename);
}

// --- Button Handlers ---
$("#exportOrdersCsv").on("click", async () => await exportOrdersCombined("csv"));
$("#exportOrdersExcel").on("click", async () => await exportOrdersCombined("excel"));
$("#exportOrdersPdf").on("click", async () => await exportOrdersCombined("pdf"));


function goBack() {
    window.location.href = "index.html";
}
