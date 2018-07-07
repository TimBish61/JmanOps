
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
         data: $('#cst_move').serialize(),
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

//***********************These scripts do customer previous/next******************************************************************
// New click


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
    //move_post(frmPrimary, dir);
    move_post(frmPrimary, dir);

});

//ony used for test - ajax to write the form fields rather than just set values
function class_move_post(post_primary_key, dir) {
    //alert(post_primary_key);
    $.ajax({
        url: "customer_move/", // the endpoint
        type: "POST", // http method
        //        data: {
        //            form: $('#cst_move').serialize(), postpk: post_primary_key, postdir: dir
        //},
        data: { postpk: post_primary_key, postdir: dir }, // data sent with the POST request
        dataType: 'html',
        success: function (data) {
            //alert('here');
            $('#search').val('');
            //$('#cst_Code').val(json.oPost.Code);
            //$('#cst_id').val(json.oPost.id);


            //the_customer_post   
            //alert(data);
            $('#the_customer_post').html('')
            $('#the_customer_post').html(data)


            console.log("post move successful");
            $('#MySaveAlert').alert('close');
            if (json.oPost.id == 0) {
                $('#bCancel').prop("disabled", true);
                $('#bDelete').prop("disabled", true);
                $('#bContactAdd').prop("disabled", true);
                contact_post('');
            }
            else {
                $('#bCancel').prop("disabled", false);
                $('#bDelete').prop("disabled", false);
                $('#bContactAdd').prop("disabled", false);
                //add contact list
                contact_post(json.oPost.Code);
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

};


function move_post(post_primary_key, dir) {
    //alert(post_primary_key);
    $.ajax({
        url: "customer_move/", // the endpoint
        type: "POST", // http method
//        data: {
//            form: $('#cst_move').serialize(), postpk: post_primary_key, postdir: dir
//},
        data: { postpk: post_primary_key, postdir: dir }, // data sent with the POST request
        //dataType: 'html',
        success: function (json) {

            $('#search').val('');
            $('#cst_Code').val(json.oPost.Code);
            $('#cst_id').val(json.oPost.id);
            $('#post-id').val(json.oPost.id);
            $('#Customer_Display').val(json.oPost.Code + ': ' + json.oPost.Name);

            //alert($('#post-id').val());

            if (json.oPost.id == 0 | json.oPost.id == -1) {
                //alert('reset');
                $('#cst_move')[0].reset();
            }


            var jsonResult = json.oReturnCustomer;
            var oReturn = JSON.parse(jsonResult);
            //var myid = oReturn[0].pk
            var oFields = oReturn[0].fields
            var sUpdate

            try {
                for (var key in oFields) {
                    if (oFields.hasOwnProperty(key)) {
                        //alert(oFields[key]);

                        if (oFields[key] == null)
                            oFields[key] = ''

                        var value = oFields[key]

                            //.replace("\r\n", "\\r\\n")
                            //.replace(/\r\n/g, "&#13;")
                            //.replace("\\n", "\n")
                            .replace(/\r\n/g, "\\r\\n")
                            .replace(/\n/g, "\\n")
                            .replace(/&/g, "&")
                            .replace(/'/g, '"')
                            .replace(/%/g, "%")
                            .replace(/"/g, '"')
                            ;
                        if (key == 'Address') {
                            var numberOfLineBreaks = (value.match(/\n/g) || []).length;
                            if (numberOfLineBreaks > 0)
                                alert(value);
                            //alert('Number of breaks: ' + numberOfLineBreaks);
                        }
                        //alert(value);
                        // work with key and value                    
                        sUpdate = "$('#post-" + key + "').val('" + value + "')"
                        //alert(sUpdate);
                        eval(sUpdate);
                    }
                }
                
            }
            catch(err){}

            $('#MySaveAlert').alert('close');
            if (json.oPost.id == 0) {
                $('#bCancel').prop("disabled", true);
                $('#bDelete').prop("disabled", true);
                $('#bContactAdd').prop("disabled", true);
                //clear contact list
                contact_post('');
                //clear transactions
                trans_post('');
            }
            else {
                $('#bCancel').prop("disabled", false);
                $('#bDelete').prop("disabled", false);
                $('#bContactAdd').prop("disabled", false);
                //add contact list
                contact_post(json.oPost.Code);
                //load transactions
                trans_post(json.oPost.Code);
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

};



//***********************These scripts do contact list******************************************************************
//Ajax for contact list
function contact_post(code) {
    //alert(code)
    $.ajax({
        type: "POST",
        url: "contact-list",
        data: {
            'code': code
            //,'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val()
        },
        success: lstContactSuccess,
        //error: alert(data),
        dataType: 'html'


    })

}

function lstContactSuccess(data, textStatus, jqXHR) {
    $('#ContactList').html(data)
}
//***********************These scripts do transactions******************************************************************

$("#bTrans").on('click', function () {
    var post_primary_key = $('#post-Code').val();
    trans_post(post_primary_key);
});

// AJAX for transactions
function trans_post(post_primary_key) {
    //if (confirm('are you sure you want to move '+ dir +' this post? id=' + post_primary_key) == true) {
    $.ajax({
        url: "customer_trans/", // the endpoint
        type: "POST", // http method
        data: {
            postpk: post_primary_key,
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

//***********************These scripts do Existing Contact Edit Save******************************************************************


$('#modal').on('click', '#frmContactModalSave', function (e) {

    e.preventDefault();
    //alert("click");
    edit_savecontact();
    return false;
});



$('#modal').on('hidden.bs.modal', function () {
    $(this).removeData('bs.modal');
    $(':input', '#frmContactModal').val("");
});

$('#modal').on('shown.bs.modal', function (event) {
    var RecordCode = $('#post-Code').val();
    //alert(RecordCode);
    //var modal = $(this)
    //modal.RecordCode.val(RecordCode);
    //modal.find('.modal-body input').val(recipient)
    $("#RecordCode").val(RecordCode);
    $("#RecordType").val("Customer");
    //alert('Code: ' + $('#RecordCode').val() + ', Type: ' + $("#RecordType").val())
})

function edit_savecontact() {
    console.log("create contact post is working!") // sanity check

    $.ajax({
        url: "contact-save-edit/", // the endpoint
        type: "POST", // http method
        data: $('#frmContactModal').serialize(),
        //data: {
        //    'form': $('#frmContactModal').serialize()
        //    , 'id': $('#frmContactModal').get('con-id').val()
        //},

        // handle a successful response
        success: function (json) {
            //update with new id
            //alert("Record Saved - id: " + json.oPost.postpk + " Code: " + json.oPost.postCode)
            $('#post-id').val(json.oPost.postpk);
            $('#results').html("<div id='MySaveAlert' data-alert class='alert alert-success alert-dismissable'>Record Saved - id: " + json.oPost.postpk + " Name: " + json.oPost.Name + "<a href='#' class='close' data-dismiss='alert' aria-label='close'>&times;</a></div>");
            $("#modal").modal('hide');
            //add contact list
            contact_post(json.oPost.postCstCode);
        },

        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

//***********************These scripts do Contact Delete******************************************************************
$('#ContactList').on('click', '.delete', function (e) {

    e.preventDefault();
    id = $(this).attr('id');
    //alert($(this).attr('id'));
    //edit_savecontact();
    delete_contact_post(id);
    return false;
});

function delete_contact_post(id) {
    console.log("delete contact post is working! ") // sanity check
    //alert(id);
    if (confirm('Are you sure you want to remove Customer ?') == true) {
        $.ajax({
            url: "contact-delete/", // the endpoint
            type: "POST", // http method
            //data: { the_post: $('#post-text').val() }, // data sent with the post request
            data: { id: id }, // data sent with the post request

            // handle a successful response
            success: function (json) {
                //update with new id
                //alert("Record Saved - id: " + json.oPost.postpk + " Code: " + json.oPost.postCode)
                //add contact list
                contact_post(json.oPost.postCode);
                $('#results').html("<div data-alert class='alert alert-success alert-dismissable'>Record Deleted - id: " + json.oPost.postpk + " Code: " + json.oPost.postCode + "<a href='#' class='close' data-dismiss='alert' aria-label='close'>&times;</a></div>");
            },

            // handle a non-successful response
            error: function (xhr, errmsg, err) {
                $('#results').html("<div class='alert alert-success alert-dismissable'>Oops! We have encountered an error: " + errmsg +
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }
};


//***********************These scripts do New Contact Save******************************************************************
// AJAX for posting
$('#modal').on('click', '#frmNewContactModalSave', function (e) {
    //alert("click");
    e.preventDefault();
    //alert("click");
    create_contact_post();
    return false;
});

function create_contact_post() {
    console.log("create contact post is working!") // sanity check

    $.ajax({
        url: "contact-create/", // the endpoint
        type: "POST", // http method

        data: $('#frmNewContactModal').serialize(),

        // handle a successful response
        success: function (json) {

            contact_post(json.oPost.postCstCode);

            $('#post-id').val(json.oPost.postpk);
            $('#results').html("<div id='MySaveAlert' data-alert class='alert alert-success alert-dismissable'>Record Saved - id: " + json.oPost.postpk + " Name: " + json.oPost.Name + "<a href='#' class='close' data-dismiss='alert' aria-label='close'>&times;</a></div>");
            $("#modal").modal('hide');
        },

        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};


