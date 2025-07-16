// $(function () {
//     //Json data by api call for order table
//     $.get(orderListApiUrl, function (response) {
//         if (response) {
//             var table = '';
//             var totalCost = 0;
//             $.each(response, function (index, order) {
//                 totalCost += parseFloat(order.total);
//                 table += '<tr>' +
//                     '<td>' + order.datetime + '</td>' +
//                     '<td>' + order.order_id + '</td>' +
//                     '<td>' + order.customer_name + '</td>' +
//                     '<td>' + order.total.toFixed(2) + ' Rs</td>' +
//                     '<td><a href="order-details.html?order_id=' + order.order_id + '" class="btn btn-sm btn-info">View</a></td>' +
//                     '</tr>';
//             });
//             table += '<tr><td colspan="3" style="text-align: end"><b>Total</b></td><td><b>' + totalCost.toFixed(2) + ' Rs</b></td></tr>';
//             $("table").find('tbody').empty().html(table);
//         }
//     });
// });


let allOrders = [];

function fetchAndRenderOrders() {
    $.get(orderListApiUrl, function (response) {
        if (response) {
            allOrders = response;
            renderTable(allOrders);
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
                <td>${order.total.toFixed(2)} Rs</td>
                <td><a href="order-details.html?order_id=${order.order_id}" class="btn btn-sm btn-info">View</a></td>
            </tr>
        `;
        tbody.append(row);
    });

    tbody.append(`
        <tr>
            <td colspan="3" style="text-align: end"><b>Total</b></td>
            <td><b>${totalCost.toFixed(2)} Rs</b></td>
            <td></td>
        </tr>
    `);
}

function filterTransactionsByDate(filter) {
    const today = new Date();
    const filtered = allOrders.filter(order => {
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

    renderTable(filtered);
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
