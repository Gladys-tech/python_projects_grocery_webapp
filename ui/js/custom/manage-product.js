// var productModal = $("#productModal");
//     $(function () {

//         //JSON data by API call
//         $.get(productListApiUrl, function (response) {
//             if(response) {
//                 var table = '';
//                 $.each(response, function(index, product) {
//                     table += '<tr data-id="'+ product.product_id +'" data-name="'+ product.name +'" data-unit="'+ product.uom_id +'" data-price="'+ product.price_per_unit +'">' +
//                         '<td>'+ product.name +'</td>'+
//                         '<td>'+ product.uom_name +'</td>'+
//                         '<td>'+ product.price_per_unit +'</td>'+
//                         '<td><span class="btn btn-xs btn-danger delete-product">Delete</span> <span class="btn btn-xs btn-primary edit-product">Edit</span></td></tr>';
//                 });
//                 $("table").find('tbody').empty().html(table);
//             }
//         });
//     });

//     // Save Product
//     $("#saveProduct").on("click", function () {
//         // If we found id value in form then update product detail
//         var data = $("#productForm").serializeArray();
//         var requestPayload = {
//             product_name: null,
//             uom_id: null,
//             price_per_unit: null
//         };
//         for (var i=0;i<data.length;++i) {
//             var element = data[i];
//             switch(element.name) {
//                 case 'name':
//                     requestPayload.product_name = element.value;
//                     break;
//                 case 'uoms':
//                     requestPayload.uom_id = element.value;
//                     break;
//                 case 'price':
//                     requestPayload.price_per_unit = element.value;
//                     break;
//             }
//         }
//         callApi("POST", productSaveApiUrl, {
//             'data': JSON.stringify(requestPayload)
//         });
//     });

//     $(document).on("click", ".delete-product", function (){
//         var tr = $(this).closest('tr');
//         var data = {
//             product_id : tr.data('id')
//         };
//         var isDelete = confirm("Are you sure to delete "+ tr.data('name') +" item?");
//         if (isDelete) {
//             callApi("POST", productDeleteApiUrl, data);
//         }
//     });

//     productModal.on('hide.bs.modal', function(){
//         $("#id").val('0');
//         $("#name, #unit, #price").val('');
//         productModal.find('.modal-title').text('Add New Product');
//     });

//     productModal.on('show.bs.modal', function(){
//         //JSON data by API call
//         $.get(uomListApiUrl, function (response) {
//             if(response) {
//                 var options = '<option value="">--Select--</option>';
//                 $.each(response, function(index, uom) {
//                     options += '<option value="'+ uom.uom_id +'">'+ uom.uom_name +'</option>';
//                 });
//                 $("#uoms").empty().html(options);
//             }
//         });
//     });

var productModal = $("#productModal");

$(function () {
    // Fetch and display products
    $.get(productListApiUrl, function (response) {
        if (response) {
            var table = '';
            $.each(response, function (index, product) {
                table += `<tr data-id="${product.product_id}" data-name="${product.name}" data-unit="${product.uom_id}" data-price="${product.price_per_unit}">
                            <td>${product.name}</td>
                            <td>${product.uom_name}</td>
                            <td>${product.price_per_unit}</td>
                            <td>
                                <span class="btn btn-xs btn-danger delete-product">Delete</span>
                                <span class="btn btn-xs btn-primary edit-product" data-toggle="modal" data-target="#productModal">Edit</span>
                            </td>
                          </tr>`;
            });
            $("table").find('tbody').empty().html(table);
        }
    });
});

// 🎯 NEW: Handle Edit Button Click
$(document).on("click", ".edit-product", function () {
    const tr = $(this).closest("tr");

    const id = tr.data("id");
    const name = tr.data("name");
    const price = tr.data("price");
    const unit = tr.data("unit");

    $("#id").val(id);
    $("#name").val(name);
    $("#price").val(price);
    $("#uoms").val(unit);

    productModal.find(".modal-title").text("Edit Product");
});

// Save Product (Create or Update)
$("#saveProduct").on("click", function () {
    var data = $("#productForm").serializeArray();
    var requestPayload = {
        product_id: $("#id").val(), // will be 0 or real id
        product_name: null,
        uom_id: null,
        price_per_unit: null
    };

    for (var i = 0; i < data.length; ++i) {
        var element = data[i];
        switch (element.name) {
            case 'name':
                requestPayload.product_name = element.value;
                break;
            case 'uoms':
                requestPayload.uom_id = element.value;
                break;
            case 'price':
                requestPayload.price_per_unit = element.value;
                break;
        }
    }

    let isEdit = requestPayload.product_id && requestPayload.product_id !== "0";
    const url = isEdit ? productEditApiUrl : productSaveApiUrl;

    callApi("POST", url, {
        'data': JSON.stringify(requestPayload)
    });

    productModal.modal('hide');
});

// Handle delete (unchanged)
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

// Reset modal on hide
productModal.on('hide.bs.modal', function () {
    $("#id").val('0');
    $("#name, #unit, #price").val('');
    productModal.find('.modal-title').text('Add New Product');
});

// Load UOMs on modal show
productModal.on('show.bs.modal', function () {
    $.get(uomListApiUrl, function (response) {
        if (response) {
            var options = '<option value="">--Select--</option>';
            $.each(response, function (index, uom) {
                options += `<option value="${uom.uom_id}">${uom.uom_name}</option>`;
            });
            $("#uoms").html(options);
        }
    });
});
