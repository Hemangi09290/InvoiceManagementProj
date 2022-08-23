
 

// $(document).ready(function(){
//   $("#company_basic").click(function(){
//     //alert("Documnet Selector")   
//  	var company_name = $("#cname").val();
//  	var company_website = $("#cwebsite").val();
//  	var company_initial = $("#cinitial").val();

//  	var company_phone_no = $("#comp_phone_no").val();
//  	// var company_email = $( "#comp_email" ).val();
//  	// var company_country = $( "#comp_country" ).val();
//  	// var company_state = $( "#comp_state" ).val();
//  	// var company_city = $( "#comp_city" ).val();
//  	// var company_zip = $( "#comp_zip" ).val();
//  	// var company_street = $( "#comp_street" ).val();


//      console.log(company_name)
//      console.log(company_website)
//      console.log(company_initial)

// 	 console.log(company_phone_no)
// 	 // console.log(company_email)
// 	 // console.log(company_country)
// 	 // console.log(company_state)
// 	 // console.log(company_city)
// 	 // console.log(company_zip)
// 	 // console.log(company_street)
// 	});

// // Company Aditional====================================

//   $("#company_aditional").click(function(){
//   var company_pan = $("#company_pan").val();
//   var company_gstn = $("#company_gstn").val();
//   var company_iec = $("#company_iec").val();
//   var company_lutbond = $("#company_lutbond").text();
//   var company_terms = $("#company_terms").text();
//   var company_declaration = $("#company_declaration").text();

// 	console.log(company_pan)
// 	console.log(company_gstn)
// 	console.log(company_iec)
// 	console.log(company_lutbond)
// 	console.log(company_terms)
// 	console.log(company_declaration)
//   });

//  $("#company_bank").click(function(){
//   var comp_account_number = $("#comp_account_number").val();
//   var comp_account_type = $("#comp_account_type").val();
//   var comp_ifsc_code = $("#comp_ifsc_code").val();
//   var comp_bank_ad_code = $("#comp_bank_ad_code").val();
 
// 	console.log(comp_account_number)
// 	console.log(comp_account_type)
// 	console.log(company_iec)
// 	console.log(comp_bank_ad_code)

//   });

// });





//    //onblur function
// function nameValidate(input) {
//     console.log("**********  Name Validation called :" , this.value )
//     if (input.value.length < 1) {
//       //red border
//         input.style.borderColor = "red";
//         document.getElementById('name').innerHTML = 'Name must be filled out';
//     }

//     else {
//       //green border
//         input.style.borderColor = "#2ecc71";
//         document.getElementById('name').innerHTML = '';
//     }
//      return true;

// 	}

// function websiteValidate(input) {
//     console.log("********** Website Validation called :" , this.value )
//     if (input.value.length < 1) {
//       //red border
//         input.style.borderColor = "red";
//     }
//     else {
//       //green border
//         input.style.borderColor = "#2ecc71";
//     }
// }


//Delete confirmation  
//Delete compnay

function confirm_popup(id){
	
if (confirm('Are you sure want to deactivate company ? ')) {

 var csrftoken = $("[name=csrfmiddlewaretoken]").val();
                console.log(csrftoken);
        $.ajax({
            url: "/company/" + id + "/cancel",
            type: "POST",
            headers: {
                "X-CSRFToken": csrftoken
            },
            success: function (response) {
                console.log(response);
                // let total_forms = $("#id_address-TOTAL_FORMS").val()
                // if (total_forms <= 1) {
                //     location.reload();
                // }
            }

});
} else {
//alert('Why did you press cancel? You should have confirmed');
}
}


//Delete Client

function confirm_client(id) {

    if (confirm('Are you sure want to deactivate client ? ', id)) {

        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        console.log(csrftoken);
        $.ajax({
            url: "/client/" + id + "/cancel",
            type: "POST",
            headers: {
                "X-CSRFToken": csrftoken
            },
            success: function (response) {
                console.log(response);
                // let total_forms = $("#id_address-TOTAL_FORMS").val()
                // if (total_forms <= 1) {
                //     location.reload();
                // }
            }

        });
    } else {
//alert('Why did you press cancel? You should have confirmed');
    }
}



function confirm_invoice(id) {

    if (confirm('Are you sure want to deactivate invoice ? ', id)) {

        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        console.log(csrftoken);
        $.ajax({
            url: "/invoice/" + id + "/cancel",
            type: "POST",
            headers: {
                "X-CSRFToken": csrftoken
            },
            success: function (response) {
                console.log(response);
                // let total_forms = $("#id_address-TOTAL_FORMS").val()
                // if (total_forms <= 1) {
                //     location.reload();
                // }
            }

        });
    } else {
//alert('Why did you press cancel? You should have confirmed');
    }
}



function get_ifsc_detail(id, value){
    var address = id.replace("ifsc_code", "bank_address");
    var name = id.replace("ifsc_code", "name");
    var branch_code = id.replace("ifsc_code", "branch_code");
    if(value){

        $.ajax({
            url: "https://ifsc.razorpay.com/" + value,
            type: "GET",
            error: function(){
            $("#" + id).val("");
            $("#" + name).val("");
            $("#" + address).val("");
            $("#"+branch_code).val("");
            alert("IFSC detail not found");
            },
            success: function(response) {
            $("#" + name).val(response.BANK);
            $("#" + address).val(response.ADDRESS);
            $("#"+branch_code).val(response.BANKCODE);
            },
        });
    } else {
    $("#" + name).val("");
    $("#" + address).val("");
    $("#"+branch_code).val("");
    }
}

function get_address(id){
    var input = document.getElementById(id);
    var autocomplete = new google.maps.places.Autocomplete(input);
    google.maps.event.addListener(autocomplete, 'place_changed', function () {
    var place = autocomplete.getPlace();

});
}

function download_pdf(){
console.log("inside the function");
var pdf = new jsPDF('p', 'px', 'A4');
 pdf.addHTML($('#invoicepdf')[0], function () {
      pdf.setFillColor(255, 255, 255, 0);

     pdf.save('Test.pdf');
 });
}

function printDiv()
{
    document.getElementById("page-break").style.pageBreakBefore = "always";
    var restorepage = $('body').html();
    var printcontent = $('#invoicepdf').clone();
    $('body').empty().html(printcontent);
    window.print();
    $('body').html(restorepage);


}


function update_payment_status(id, payment_status) {
    var payment_status_inv = {
      Pending: "Paid",
      Paid: "Pending"
    };
    if (confirm('Are you sure, Do you want to update payment status from '+payment_status+' to '+payment_status_inv[payment_status]+'? ', id)) {

        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        console.log(csrftoken);
        $.ajax({
            url: "/invoice/" + id + "/update-status",
            type: "POST",
            async: false,
            cache: false,
            timeout: 30000,
            headers: {
                "X-CSRFToken": csrftoken
            },
            dataType:"json",
            data: {
                'payment_status': payment_status
            },
            success: function (response) {
                console.log(response);
            },
            error: function (error) {
                alert("no success");
            }

        });
    } else {

    }
}

function reset_filters(){
    $("#id_created_at_0").val("");
    $("#id_created_at_1").val("");
    $("#id_payment_status").val("");
    $("#id_project").val("")
    $("#id_client").val("");
}