// Fetch and display all expenses
$(document).ready(function () {
    $.get(expenseListApiUrl, function (response) {
        var tbody = $('#expenseTable tbody');
        tbody.empty();
        $.each(response, function (index, expense) {
            var row = '<tr>' +
                '<td>' + expense.category + '</td>' +
                '<td>' + expense.description + '</td>' +
                '<td>' + expense.amount + '</td>' +
                '<td>' + expense.date + '</td>' +
                '</tr>';
            tbody.append(row);
        });
    });
});

// Save expense
$('#saveExpense').on('click', function () {
    var category = $('#expense_category').val();
    var description = $('#expense_description').val();
    var amount = parseFloat($('#expense_amount').val());

    if (!category || !description || isNaN(amount)) {
        alert('Please fill in all fields correctly.');
        return;
    }

    var expensePayload = {
        category: category,
        description: description,
        amount: amount
    };

    callApi("POST", expenseSaveApiUrl, JSON.stringify(expensePayload));
});
