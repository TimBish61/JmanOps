
//***********************These scripts do customert Save******************************************************************

// Submit post on submit
$('#cst_move').on('submit', function (event) {
    //alert('here');
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    //alert('going to post next!')
    var btn = event.target.submited;
    if (btn == 'Delete') {
        delete_cust_post();
    }
    else if (btn == 'Cancel') {
        move_post(-1, 'equals');
    }
    else {
        create_cust_post();
    }
});


// AJAX for posting
function create_cust_post() {
    console.log("create customer post is working!") // sanity check
    $.ajax({
        url: "create_custpost/", // the endpoint
        type: "POST", // http method
        //data: { the_post: $('#post-text').val() }, // data sent with the post request
        data: { Code: $('#post-Code').val(), Name: $('#post-Name').val(), Address: $('#post-Address').val(), PostCode: $('#post-PostCode').val(), id: $('#post-id').val() }, // data sent with the post request

        // handle a successful response
        success: function (json) {
            //update with new id
            //alert("Record Saved - id: " + json.oPost.postpk + " Code: " + json.oPost.postCode)
            $('#post-id').val(json.oPost.postpk);
            $('#results').html("<div id='MySaveAlert' data-alert class='alert alert-success alert-dismissable'>Record Saved - id: " + json.oPost.postpk + " Code: " + json.oPost.postCode + "<a href='#' class='close' data-dismiss='alert' aria-label='close'>&times;</a></div>");
        },

        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};



//***********************These scripts do customer previous/next******************************************************************

// Prev click
$("#Move").on('click', 'a[id^=prev-post-]', function () {
    var post_primary_key = $(this).attr('id').split('-')[2];
    var dir = 'prev';
    var frmPrimary = $('#post-id').val();
    console.log(post_primary_key) // sanity check
    move_post(frmPrimary, dir);
});

// Next click
$("#Move").on('click', 'a[id^=next-post-]', function () {
    var post_primary_key = $(this).attr('id').split('-')[2];
    var dir = 'next';
    var frmPrimary = $('#post-id').val();
    console.log(post_primary_key) // sanity check
    move_post(frmPrimary, dir);

});






// AJAX for moving
function move_post(post_primary_key, dir) {
    //if (confirm('are you sure you want to move '+ dir +' this post? id=' + post_primary_key) == true) {
    $.ajax({
        url: "customer_move/", // the endpoint
        type: "POST", // http method
        data: { postpk: post_primary_key, postdir: dir }, // data sent with the POST request
        //data: { the_customer_post: $('#post-Code').val() }, // data sent with the post request

        success: function (json) {
            $('#search').val('');
            $('#post-Code').val(json.oPost.Code);
            $('#post-Name').val(json.oPost.Name);
            $('#post-Address').val(json.oPost.Address);
            $('#post-PostCode').val(json.oPost.PostCode);
            $('#post-id').val(json.oPost.id);
            console.log("post move successful");
            $('#MySaveAlert').alert('close');
            if (json.oPost.id == 0) {
                $('#bCancel').prop("disabled", true);
                $('#bDelete').prop("disabled", true);
            }
            else {
                $('#bCancel').prop("disabled", false);
                $('#bDelete').prop("disabled", false);
            }
        },

        error: function (xhr, errmsg, err) {
            // Show an error
            $('#results').html("<div class='alert-box alert radius' data-alert>" +
                "Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            $('#search').val('');
        }
    });
    //} else {
    //    return false;
    //}
    //finally close alert
    //$(this).parent().alert('alert alert-success alert-dismissable');

};




// AJAX for posting
function delete_cust_post() {
    console.log("delete customer post is working! ") // sanity check
    if (confirm('Are you sure you want to remove Customer ?') == true) {
        $.ajax({
            url: "delete_customer/", // the endpoint
            type: "POST", // http method
            //data: { the_post: $('#post-text').val() }, // data sent with the post request
            data: { Code: $('#post-Code').val(), Name: $('#post-Name').val(), Address: $('#post-Address').val(), PostCode: $('#post-PostCode').val(), id: $('#post-id').val() }, // data sent with the post request

            // handle a successful response
            success: function (json) {
                //update with new id
                //alert("Record Saved - id: " + json.oPost.postpk + " Code: " + json.oPost.postCode)
                $('#post-Code').val('');
                $('#post-Name').val('');
                $('#post-Address').val('');
                $('#post-PostCode').val('');
                $('#post-id').val(0);
                $('#results').html("<div data-alert class='alert alert-success alert-dismissable'>Record Deleted - id: " + json.oPost.postpk + " Code: " + json.oPost.postCode + "<a href='#' class='close' data-dismiss='alert' aria-label='close'>&times;</a></div>");
            },

            // handle a non-successful response
            error: function (xhr, errmsg, err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }
};
//***********************These scripts do transactions******************************************************************
// trans click

$("#bTrans").on('click', function () {
    var post_primary_key = $('#post-Code').val();
    var dir = '';
    trans_post(post_primary_key, dir);
});

// AJAX for transactions
function trans_post(post_primary_key, dir) {
    //if (confirm('are you sure you want to move '+ dir +' this post? id=' + post_primary_key) == true) {
    $.ajax({
        url: "customer_trans/", // the endpoint
        type: "POST", // http method
        data: {
            postpk: post_primary_key, postdir: dir,
            'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val()
        }, // data sent with the POST request
        //data: { the_customer_post: $('#post-Code').val() }, // data sent with the post request

        success: function (json) {
            //$('#Trans').html("<table><tr><th>Test</th></tr></table>")
            $('#Trans').html(json)
        },

        error: function (xhr, errmsg, err) {
            // Show an error
            $('#results').html("<div class='alert-box alert radius' data-alert>" +
                "Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            $('#search').val('');
        }
    });
    //} else {
    //    return false;
    //}
    //finally close alert
    //$(this).parent().alert('alert alert-success alert-dismissable');

};


//***********************These scripts do search******************************************************************
//search_results - this is the list click
$("#search_results").on('click', 'a[id^=equals-post-]', function () {
    var dir = 'equals';
    var post_primary_key = $(this).attr('id').split('-')[2];
    console.log(post_primary_key) // sanity check
    move_post(post_primary_key, dir);

});

//search_results
$("#search_results").on('click', 'a[id^=cst-lookup-]', function () {
    var dir = 'equals';
    var post_primary_key = $(this).attr('id').split('-')[2];
    var post_text = this.text
    console.log(post_primary_key) // sanity check
    $('#cstLookup').val(post_primary_key);
    $('#cstName').val(post_text);

});

$('#search').keyup(function () {

    $.ajax({
        type: "POST",
        url: "/search/",
        data: {
            'search_text': $('#search').val(),
            'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val()
        },
        success: searchSuccess,
        dataType: 'html'


    })

})

//btnSearch
$("#btnSearch").on('click', function () {

    $.ajax({
        type: "POST",
        url: "/search/",
        data: {
            'search_text': $('#search').val(),
            'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val()
        },
        success: btnsearchSuccess,
        dataType: 'html'


    })

});

//btnSearch
$("#btnCstLookup").on('click', function () {

    $.ajax({
        type: "POST",
        url: "/lookup/",
        data: {
            'search_text': $('#cstLookup').val(),
            'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val()
        },
        success: btnsearchSuccess,
        dataType: 'html'


    })

});

function searchSuccess(data, textStatus, jqXHR) {
    $('#search_results').html(data)
    $(".dropdown-toggle").dropdown('toggle');
}

function btnsearchSuccess(data, textStatus, jqXHR) {
    $('#search_results').html(data)

}


//****************SEcurity Token Stuff***************************************************************************

$(function () {


    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});