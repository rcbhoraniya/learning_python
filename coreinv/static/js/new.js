

function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}

//stores the total no of item forms
var total = 1;

function cloneMore(selector, prefix) {
    var newElement = $(selector).clone(true, true);
    var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
    newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
        var name = $(this).attr('name');
        console.log(name);
        if(name) {
            name = name.replace('-' + (total-1) + '-', '-' + total + '-');
                    console.log(name);

            var id = 'id_' + name;
            $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
        }
    });
    newElement.find('label').each(function() {
        var forValue = $(this).attr('for');
        if (forValue) {
        forValue = forValue.replace('-' + (total-1) + '-', '-' + total + '-');
        $(this).attr({'for': forValue});
        }
    });
    total++;
    console.log(total-1)
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
    $('#id_form-'+(total-1)+'-product').off('change');
    add_product(total-1);

    update_amounts($('.quantity:last'));

    return false;
}

function deleteForm(prefix, btn) {
    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());

    if (total > 1){
        btn.closest('.form-row').remove();
        var forms = $('.form-row');

        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (var i=0, formCount=forms.length; i<formCount; i++) {
            $(forms.get(i)).find(':input').each(function() {
                updateElementIndex(this, prefix, i);
            });
        }
        total--;
    } else {
        alert('Field cannot be deleted');
    }
    return false;
}

function update_invoice_totals() {

    // amount without gst
    sum_amt_without_gst = 0
    $('.amt_without_gst').each(function(){
        sum_amt_without_gst += parseFloat($(this).val());
    });
    $('#id_total_amt_without_gst').val(sum_amt_without_gst.toFixed(2));
        console.log(sum_amt_without_gst);

    // amount sgst
    sum_amt_sgst = 0
    $('.amt_sgst').each(function(){

        sum_amt_sgst += parseFloat($(this).val());

    });
    $('#id_total_amt_sgst').val(sum_amt_sgst.toFixed(2));

    // amount cgst
    sum_amt_cgst = 0
    $('.amt_cgst').each(function(){
        sum_amt_cgst += parseFloat($(this).val());
    });
    $('#id_total_amt_cgst').val(sum_amt_cgst.toFixed(2));

    // amount igst
    sum_amt_igst = 0
    $('.amt_igst').each(function(){
        sum_amt_igst += parseFloat($(this).val());
    });
    $('#id_total_amt_igst').val(sum_amt_igst.toFixed(2));

    sum_amt_with_gst = 0
    $('.amt_with_gst').each(function(){
        sum_amt_with_gst += parseFloat($(this).val());
    });
    $('#id_total_amt_with_gst').val(sum_amt_with_gst.toFixed(2));

}

function initialize_auto_calculation(){
    update_amounts($('.quantity'));
    $('.quantity').change(function (){
        update_amounts($(this));
    });
}


function update_amounts(element){
//updates the total price by multiplying 'price per item' and 'quantity'
//$(document).on('change', '.quantity', function(e){
//    element.preventDefault();
    //gets the values
//    var element = $(this);
//    console.log(element.parents);
    var product = element.parents('.form-row').find('.product').val();
    var rate_without_gst = element.parents('.form-row').find('.rate_without_gst').val();

    var quantity = element.parents('.form-row').find('.quantity').val();
    var gst_percentage = element.parents('.form-row').find('.gst_percentage').val();
    var profit_margin_percentage=element.parents('.form-row').find('.profit_margin_percentage').val();

    var purchase_price = rate_without_gst * gst_percentage/100 + parseFloat(rate_without_gst);


    var rate_with_gst = (purchase_price * profit_margin_percentage/100) + purchase_price;


    var amt_without_gst = rate_without_gst * quantity;

    var sgst;
    var cgst;
    var igst;
    if(product == ""){
        sgst = 0;
        cgst = 0;
        igst = 0;
        amt_without_gst = 0;
    }
    else {
        if($('#id_igstcheck').is(':checked')){
            sgst = 0;
            cgst = 0;
            igst = amt_without_gst * gst_percentage / 100;
        }
        else {
            sgst = amt_without_gst * gst_percentage / 200;
            cgst = amt_without_gst * gst_percentage / 200;
            igst = 0;

        }
    }
    var amt_with_gst = amt_without_gst + cgst + sgst + igst;

//    element.parent('.form-row').find('.rate_without_gst').val(rate_without_gst);
    element.parents('.form-row').find('.rate_with_gst').val(rate_with_gst.toFixed(2));
    element.parents('.form-row').find('.amt_without_gst').val(amt_without_gst.toFixed(2));
    element.parents('.form-row').find('.amt_sgst').val(sgst.toFixed(2));
    element.parents('.form-row').find('.amt_cgst').val(cgst.toFixed(2));
    element.parents('.form-row').find('.amt_igst').val(igst.toFixed(2));
    element.parents('.form-row').find('.amt_with_gst').val(amt_with_gst.toFixed(2));

    update_invoice_totals();

    return false;
//});
}

function add_invoice_rows() {
    $(document).on('click', '.add-form-row', function(e){
            e.preventDefault();
            cloneMore('.form-row:last', 'form');
            return false;
        });
}


function remove_invoice_rows(){
$(document).on('click', '.remove-form-row', function(e){
    e.preventDefault();
    deleteForm('form', $(this));
    return false;
});

}


$("#id_customer").on('change',function (e) {
        console.log('hi')
      var url = '/customerjson';  // get the url of the `load_cities` view
      var customerId = $(this).val();  // get the selected country ID from the HTML input
        console.log(customerId)
      $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'customerid': customerId       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
//        $("#id_name").val(data[0]['name']);
          $("#id_address").val(data[0]['address']);
            $("#id_city").val(data[0]['city']);
             $("#id_email").val(data[0]['email']);
              $("#id_phone").val(data[0]['phone']);
               $("#id_gstin").val(data[0]['gstin']);
            // replace the contents of the city input with the data that came from the server
            console.log(data)
        }
      });

    });


function add_product(i){
$('#id_form-'+i+'-product').on('change',function (e) {
console.log('#id_form-'+i+'-product')
e.preventDefault();
      var url = '/productjson';  // get the url of the `load_cities` view
      var productId = $(this).val();  // get the selected country ID from the HTML input
      $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'productid': productId       // add the country id to the GET parameters
        },
        success: function (data) {

<!--        $("#id_name").val(data[0]['name']);-->
          $('#id_form-'+i+'-hsn').val(data[0]['hsn']);
            $('#id_form-'+i+'-unit').val(data[0]['unit']);
             $('#id_form-'+i+'-rate_without_gst').val(data[0]['rate_without_gst']);
              $('#id_form-'+i+'-gst_percentage').val(data[0]['gst_percentage']);
            $('#id_form-'+i+'-profit_margin_percentage').val(data[0]['profit_margin_percentage']);
            // replace the contents of the city input with the data that came from the server

        }
      });

    });
}


$(document).ready(function() {

add_invoice_rows();
remove_invoice_rows();

const formRow = document.getElementsByClassName('form-row')

var total = parseInt($('#id_form-TOTAL_FORMS').val());
for(let i=0; i<total;i++){
formRow[i].setAttribute('id',`form-${i}`)
add_product(i);
}
    // Initialize auto calculation of amounts
    initialize_auto_calculation();

    // Initialize igst toggle
    $("#id_igstcheck").change(function() {
            $('.quantity').each(function(){
                update_amounts($( this ));
            });
    });

});
