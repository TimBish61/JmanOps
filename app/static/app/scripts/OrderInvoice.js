

$('#SODetail tbody').on('change', 'td', function () {
    event.stopImmediatePropagation();
    var post_primary_key = $(this).find("input[type='number']").attr('id');
    //var r = /\d+/;
    //var s = post_primary_key
    //alert(s.match(r));

    var sField = post_primary_key.split('-', 3)

    if (!(sField[2] == 'SOQty' || sField[2] == 'SOSalesPrice')) {
        return;
    }
    //alert('Field: ' + sField[2] + ' RowNo: ' + sField[1]);
    var sEval = "$('#" + post_primary_key + "').val()";
    //alert(sEval);
    var fValue = eval(sEval);
    //alert(fValue);

    if (sField[2] == 'SOQty' || sField[2] == 'SOSalesPrice') {
        //SOQty
        //SOSalesPrice
        //SONet
        //SOHomeNet
        var sQty = "$('#id_tosoheader-" + sField[1] + "-SOQty').val()";
        var sUnitPrice = "$('#id_tosoheader-" + sField[1] + "-SOSalesPrice').val()";
        var sNet = "$('#id_tosoheader-" + sField[1] + "-SOHomeNet').val()";
        var sHomeNet = "$('#id_tosoheader-" + sField[1] + "-SONet').val()";

        var fQty = eval(sQty);
        var fUnitPrice = eval(sUnitPrice);
        var fNet = fQty * fUnitPrice;
        //alert(fQty);
        //alert(fUnitPrice);
        //alert(fNet);
        var sSetNet = "$('#id_tosoheader-" + sField[1] + "-SONet').val("+fNet+")";
        //var sSetNet = "$('#id_tosoheader-" + sField[1] + "-SONet').val((" + sQty + ")*(" + sUnitPrice+"))";

        eval(sSetNet);

        //$("#tosoheader-""-SONet").val() = $("#SOQty").val() * $("#SOSalesPrice").val()
    }

    

});

$("#id_customer").on('change', function () {
    //alert("cust change ere");   
    event.stopImmediatePropagation();
    var cst_id = this.value;
    if (cst_id!='')
        setCurrencyCode(cst_id);
    else
        $('#id_SOExRate').val(1);

});

$("#id_SOCurrency").on('change', function () {
    //alert("curry change");   
    var curr_id = this.value;
    var curr_code = $("#id_SOCurrency option:selected").text()
    var res = curr_code.split(':');
    curr_code = res[0];


    if (curr_code == 'GBP')
        $('#id_SOExRate').val(1);
    else if (curr_code == ''){
        $('#id_SOExRate').val(1);
    }
    else
        setXRate(curr_code);


});

function setCurrencyCode(primary_key) {
    //alert(post_primary_key);
    $.ajax({
        url: "setcurrency/", // the endpoint
        type: "POST", // http method
        data: { postpk: primary_key }, // data sent with the POST request

        success: function (json) {

            $('#id_SOCurrency').val(json.oPost.CurrencyId);

            if (json.oPost.CurrencyId != '') {
                setXRate(json.oPost.CurrencyCode);
                
            }
            else {
                $("#id_SOCurrency").val(153)
                $('#id_SOExRate').val(1);
            }
            console.log("update successful");
            $('#results').html("<div data-alert class='alert alert-success alert-dismissable'>Currency set - id: " + json.oPost.postpk + " Code: " + json.oPost.postCode + "<a href='#' class='close' data-dismiss='alert' aria-label='close'>&times;</a></div>");


        },

        error: function (xhr, errmsg, err) {
            // Show an error
            $('#results').html("<div class='alert-box alert radius' data-alert>" +
                "Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            $('#search').val('');
        }
    });

};

function setXRate(currency_code) {
    //alert(post_primary_key);
    $.ajax({
        url: "setXRate/", // the endpoint
        type: "POST", // http method
        data: { currency_code: currency_code }, // data sent with the POST request

        success: function (json) {

            $('#id_SOExRate').val(json.oPost.ExRate);

            console.log("update successful");
            $('#results').html("<div data-alert class='alert alert-success alert-dismissable'>Ex Rate set - id: " + json.oPost.postpk + " Code: " + json.oPost.postCode + "<a href='#' class='close' data-dismiss='alert' aria-label='close'>&times;</a></div>");


        },

        error: function (xhr, errmsg, err) {
            // Show an error
            $('#results').html("<div class='alert-box alert radius' data-alert>" +
                "Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            $('#search').val('');
        }
    });

};

$("#SODetail tbody").on('focus','.LineText', function () {    
    event.stopImmediatePropagation();
    var post_primary_key = $(this).attr('id');
    this.rows = 5;
    this.cols = 50;

});



$("#SODetail tbody").on('blur', '.LineText', function () {
    event.stopImmediatePropagation();
    var post_primary_key = $(this).attr('id');
    this.rows = 1;
    this.cols = 30;

});