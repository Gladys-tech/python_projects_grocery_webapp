var productModal = $("#productModal");
$(function () {

    //JSON data by API call
    $.get(productListApiUrl, function (response) {
        if (response) {
            var table = '';
            $.each(response, function (index, product) {
                // var quantity = product.quantity || 0;
                // var lowStockClass = quantity <= 5 ? 'low-stock' : '';
                // Build table rows with product data
                table += '<tr data-id="' + product.product_id +
                    '" data-name="' + product.name +
                    '" data-unit="' + product.uom_id +
                    '" data-price="' + product.price_per_unit +
                    '" data-buying-price="' + (product.buying_price || 0) + '">' +
                    '" data-quantity="' + (product.quantity || 0) + '">' +
                    '<td>' + product.name + '</td>' +
                    '<td>' + product.uom_name + '</td>' +
                    '<td>' + product.price_per_unit + '</td>' +
                    '<td>' + (product.buying_price || 0) + '</td>' +
                    '<td>' + (product.quantity || 0) + '</td>' +
                    '<td><span class="btn btn-xs btn-danger delete-product">Delete</span> <span class="btn btn-xs btn-primary edit-product">Edit</span></td></tr>';

            });
            var lowStockItems = response.filter(p => (p.quantity || 0) <= 5);
            if (lowStockItems.length > 0) {
                alert("Warning: " + lowStockItems.length + " product(s) are low in stock!");
            }

            $("table").find('tbody').empty().html(table);
        }
    });
});

$(document).on("click", ".edit-product", function () {
    var tr = $(this).closest('tr');
    var id = tr.data('id');
    var name = tr.data('name');
    var unit = tr.data('unit');
    var price = tr.data('price');
    var buyingPrice = tr.data('buying-price') || 0;
    var quantity = tr.data('quantity') || 0;


    // Set values in modal form
    $("#productId").val(id);
    $("#name").val(name);
    $("#uoms").val(unit);
    $("#price").val(price);
    $("#buying_price").val(buyingPrice);
    $("#quantity").val(quantity);

    console.log("Editing product with ID:", id);
    console.log("Editing product with name:", name);
    console.log("Editing product with uom_id:", unit);
    console.log("Editing product with price:", price);
    console.log("Editing product with buying price:", buyingPrice);
    console.log("Editing product with quantity:", quantity);

    console.log(tr[0].outerHTML); // to see all data-* attributes directly


    // Change modal title
    productModal.find('.modal-title').text('Edit Product');
    productModal.modal('show');
});


// Save Product
$("#saveProduct").on("click", function () {
    // If we found id value in form then update product detail
    var data = $("#productForm").serializeArray();
    var requestPayload = {
        product_id: null,
        product_name: null,
        uom_id: null,
        price_per_unit: null,
        buying_price: null,
        quantity: null
    };
    for (var i = 0; i < data.length; ++i) {
        var element = data[i];
        switch (element.name) {
            case 'product_id':
                requestPayload.product_id = element.value;
                break;
            case 'name':
                requestPayload.product_name = element.value;
                break;
            case 'uoms':
                requestPayload.uom_id = element.value;
                break;
            case 'price':
                requestPayload.price_per_unit = element.value;
                break;
            case 'buying_price':
                requestPayload.buying_price = element.value;
                break;
            case 'quantity':
                requestPayload.quantity = element.value;
                break;
        }
    }
    // ✅ DEBUG LOGS
    console.log("Product ID from form:", requestPayload.product_id);
    console.log("Detected as edit:", requestPayload.product_id && requestPayload.product_id !== "0");

    // Decide API URL based on whether product_id is set
    var isEdit = requestPayload.product_id && requestPayload.product_id !== "0";
    var apiUrl = isEdit ? productEditApiUrl : productSaveApiUrl;
    var method = isEdit ? "PUT" : "POST";
    // ✅ LOG which API endpoint and method are used
    console.log("API Method:", method);
    console.log("API URL:", apiUrl);
    console.log("Payload:", requestPayload);

    callApi(method, apiUrl, {
        'data': JSON.stringify(requestPayload)
    });

});

$(document).on("click", ".delete-product", function () {
    var tr = $(this).closest('tr');
    var data = {
        product_id: tr.data('id')
    };
    var isDelete = confirm("Are you sure to delete " + tr.data('name') + " item?");
    if (isDelete) {
        callApi("POST", productDeleteApiUrl, data);
    }
});

productModal.on('hide.bs.modal', function () {
    $("#id").val('0');
    // $("#productId").val('0');
    $("#name, #unit, #price,  #buying_price, #quantity").val('');
    productModal.find('.modal-title').text('Add New Product');
});

productModal.on('show.bs.modal', function () {
    //JSON data by API call
    $.get(uomListApiUrl, function (response) {
        if (response) {
            var currentUnit = $("#uoms").val(); // Save current value
            var options = '<option value="">--Select--</option>';
            $.each(response, function (index, uom) {
                options += '<option value="' + uom.uom_id + '">' + uom.uom_name + '</option>';
            });
            $("#uoms").empty().html(options).val(currentUnit);
        }
    });
});