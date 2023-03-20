
var quantities = document.getElementsByClassName('quantity_changed');

$(document).ready(function () {
    $('#cartitems_table').on('click', '.removeitem', function (e) {

        var product_id = $(this).data('remove_id');

        $.ajax({
            type: 'GET',
            url: '/remove-cart',
            dataType: 'json',
            data: {
                product_id: product_id,
               
            },
            success: function (data) {

                var table = $('#cartitems_table');
                table.find('tbody').empty();
                console.log('Table emptied')
                table.append(data.rendered.table_to_render);
                console.log('Table added.')
                
                document.getElementById('total_payment_subtotal').innerHTML = `$${data.data.total_payment.toFixed(2)}`
                
                document.getElementById('total_payment').innerHTML = `$${data.data.total_payment.toFixed(2)}`
                document.getElementById('cart_items_total').innerHTML = data.data.total_product_quantity;
            },

            error: function () { }

        })

    })


});



$('#cartitems_table').on('change', '.quantity_changed', function (e) {

        console.log('value changed')

        var newvalue = e.target.value
        var product_id = e.target.dataset.productid
        
        $.ajax({
            type: 'GET',
            url: '/update-cart',
            dataType: 'json',
            data: {
                new_quantity: newvalue,
                product_id: product_id,
            },
            success: function (data) {
                document.getElementById('cart_items_total').innerHTML = data.cart_items_total;

                e.target.parentElement.parentElement.parentElement.parentElement.children[2].innerHTML = `$${data.item_subtotal.toFixed(2)}`;

                document.getElementById('total_payment_subtotal').innerHTML = `$${data.total_payment.toFixed(2)}`
                document.getElementById('total_payment').innerHTML = `$${data.total_payment.toFixed(2)}`
                
            },
            error: function (data) { console.error(data.errors) }

        })

    })


let shop_detail_add_to_cart_btn = $('#shop_detail_add_to_cart');
console.log('aM SOMEWERE HERE.')
console.log(shop_detail_add_to_cart_btn)
shop_detail_add_to_cart_btn.on('click', function(e){
    console.log('I clicked this')
})


