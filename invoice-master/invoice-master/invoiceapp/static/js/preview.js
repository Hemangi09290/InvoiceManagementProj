$(document).ready(function() {

    function check_empty_value(value){
        if (value == null || value == ""){
            return ""
        }
        return value;
    }

    function get_particulars(prefix="form") {
      let total_forms = $("#id_"+prefix+"-TOTAL_FORMS").val();
      console.log(total_forms);
      var i;
      let resources = "", quantities = "<br>", unit_rates = "<br>", amounts = "<br>";

      for (i = 0; i < total_forms; i++) {
          let unit_rate_val = "", resource = "";
          if (prefix === "form") {
               resource = $("#id_" + prefix + "-" + i.toString() + "-resource_type :selected").text();
               unit_rate_val = $("#id_" + prefix + "-" + i.toString() + "-unit_rate").val();
          }else{
              resource = $("#id_" + prefix + "-" + i.toString() + "-project_particulars_name").val();
              unit_rate_val = "";
          }
          let quantity = $("#id_"+prefix+"-" + i.toString() + "-quantity").val();

          let amount = $("#id_"+prefix+"-" + i.toString() + "-amount").val();
          quantities = quantities + "<br>" + quantity;
          unit_rates = unit_rates + "<br>" + unit_rate_val;
          amounts = amounts + "<br>" + amount;
          resources = resources + "<br>" + resource;
      }
      return {
          quantities, amounts, unit_rates, resources
      }
  }

function preview_invoice() {
    let id_company = $("#id_company :selected").val();
    let id_company_bank = $("#id_company_bank :selected").val();
    let id_from_address = $("#id_from_address :selected").val();
    let id_client = $("#id_client :selected").val();
    let id_to_address = $("#id_to_address :selected").val();
    let text_currency = $("#id_currency :selected").text();

    let project_type = $("#id_project_type :selected").val();
    let prefix = "", in_words= "", total_amount = 0;
    var cgst_amt = 0, sgst_amt = 0, cgst_val = 0, sgst_val = 0, igst_amt=0, igst_val=0;
    if (project_type === "hourly") {
        in_words = $("#in_words").text();
        total_amount = $("#total_amount").val();
        if (text_currency==="INR"){
            cgst_amt =  total_amount*parseFloat($("#id_cgst").val())/100;
            sgst_amt =  total_amount*parseFloat($("#id_sgst").val())/100;
            igst_amt =  total_amount*parseFloat($("#id_igst").val())/100;
            cgst_val =  $("#id_cgst").val();
            sgst_val =  $("#id_sgst").val();
            igst_val =  $("#id_igst").val();
        }
        prefix = "form";
    }else{
        in_words = $("#fixed_in_words").text();
        total_amount = $("#fixed_total_amount").val();
        if (text_currency==="INR"){
            cgst_amt =  total_amount*parseFloat($("#id_fixed_cgst").val())/100;
            sgst_amt =  total_amount*parseFloat($("#id_fixed_sgst").val())/100;
            igst_amt =  total_amount*parseFloat($("#id_fixed_igst").val())/100;
            cgst_val =  $("#id_fixed_cgst").val();
            sgst_val =  $("#id_fixed_sgst").val();
            igst_val =  $("#id_fixed_igst").val();
        }
        prefix = "fixed_p";
        $("#qty_heading").html("Qty as per <br>Project Work");
    }
    let exchange_rate = $("#id_exchange_rate").val();
    let total_inr = 0;
    if ((!isNaN(total_amount) && (!isNaN(exchange_rate)))) {
        total_inr = parseFloat(total_amount) * parseFloat(exchange_rate);
    }
    let url = "/invoice-preview?company=" + id_company + "&client=" + id_client + "&from_address=" + id_from_address + "&to_address=" + id_to_address + "&bank_id=" + id_company_bank
    $.ajax({
        url: url,
        type: "GET",
        success: function (response) {
            console.log(response);

            var response_json = JSON.parse(response);
            $("#id_company_name").text(response_json.company_name);
            $("#id_company_address").html(response_json.company_address);
            $("#id_footer_ph_no").text(response_json.company_phone_number);
            $("#id_company_website").text(response_json.company_website);

            $("#id_footer_company_name").text(response_json.company_name);
            $("#id_footer_company_address").html(response_json.company_address);
            $("#id_company_phone_no").text("PH - " + response_json.company_phone_number);
            $("#id_footer_website").text(response_json.company_website);

            $("#id_invoice_additional").html(response_json.company_additional);
            $("#id_invoice_bank_ad").text(response_json.company_bank);
            $("#id_invoice_bank_name").text(response_json.bank_name);
            $("#id_invoice_bank_addr").text(response_json.bank_address);
            $("#id_invoice_bank_acc").text(response_json.company_bank_acc);
            $("#id_invoice_ifsc").text(response_json.company_bank_ifsc);

            $("#id_client_name").text(response_json.client_name);
            $("#id_client_address").html(response_json.client_address);
            $("#id_invoice_project").html(response_json.project_name);
            $("#id_invoice_eefc").html(response_json.company_bank_eefc);
            $("#id_bank_ad_code").html(response_json.bank_ad_code);
            $("#id_terms_condition_inv").html(response_json.terms_condition);
            $("#id_inv_lut_bond").html(response_json.lut_bond);
            $("#id_inv_self_declaration").html(response_json.self_declaration);
            $("#id_inv_company_cin").html(response_json.company_cin);

        },
    });
    $("#total_in_words").html(check_empty_value(in_words));
    $("#invoice_total_amount").html(check_empty_value(total_amount));

    $("#invoice_currency").html(check_empty_value(text_currency));

    $("#invoice_currency_inr").text(check_empty_value(total_inr));
    let particulars = get_particulars(check_empty_value(prefix));
    if (text_currency==="INR"){
            if(cgst_val && cgst_val != 0){
                particulars.amounts = particulars.amounts+"<br>"+cgst_amt.toFixed(2);
                particulars.resources = particulars.resources+"<br> CGST "+cgst_val+"%";
            }
            if(sgst_val && sgst_val != 0){
                particulars.amounts = particulars.amounts+"<br>"+sgst_amt.toFixed(2);
                particulars.resources = particulars.resources+"<br> SGST "+sgst_val+"%";
            }
            if(igst_val && igst_val != 0){
                particulars.amounts = particulars.amounts+"<br>"+igst_amt.toFixed(2);
                particulars.resources = particulars.resources+"<br> IGST "+igst_val+"%";
            }

        }
    else{
        exchange_rate = check_empty_value(exchange_rate);
        text_currency = check_empty_value(text_currency);
        $("#invoice_exchange_rate").text("Per "+text_currency+" @ Rs. "+ exchange_rate);
    }
    $("#id_invoice_p_qty").html(check_empty_value(particulars.quantities));
    $("#id_invoice_p_rate").html(check_empty_value(particulars.unit_rates));
    $("#id_invoice_p_amount").html(check_empty_value(particulars.amounts));
    $("#id_invoice_p_items").html(check_empty_value(particulars.resources));

}


function preview_invoice_temp2() {
    let id_company = $("#id_company :selected").val();
    let id_company_bank = $("#id_company_bank :selected").val();
    let id_from_address = $("#id_from_address :selected").val();
    let id_client = $("#id_client :selected").val();
    let id_to_address = $("#id_to_address :selected").val();
    let text_currency = $("#id_currency :selected").text();

    let project_type = $("#id_project_type :selected").val();
    let prefix = "", in_words= "", total_amount = 0;
    var cgst_amt = 0, sgst_amt = 0, cgst_val = 0, sgst_val = 0, igst_amt=0, igst_val=0;
    if (project_type === "hourly") {
        in_words = $("#in_words").text();
        total_amount = $("#total_amount").val();
        if (text_currency==="INR"){
            cgst_amt =  total_amount*parseFloat($("#id_cgst").val())/100;
            sgst_amt =  total_amount*parseFloat($("#id_sgst").val())/100;
            igst_amt =  total_amount*parseFloat($("#id_igst").val())/100;
            cgst_val =  $("#id_cgst").val();
            sgst_val =  $("#id_sgst").val();
            igst_val =  $("#id_igst").val();
        }
        prefix = "form";
    }else{
        in_words = $("#fixed_in_words").text();
        total_amount = $("#fixed_total_amount").val();
        if (text_currency==="INR"){
            cgst_amt =  total_amount*parseFloat($("#id_fixed_cgst").val())/100;
            sgst_amt =  total_amount*parseFloat($("#id_fixed_sgst").val())/100;
            igst_amt =  total_amount*parseFloat($("#id_fixed_igst").val())/100;
            cgst_val =  $("#id_fixed_cgst").val();
            sgst_val =  $("#id_fixed_sgst").val();
            igst_val =  $("#id_fixed_igst").val();
        }
        prefix = "fixed_p";
        $("#qty_heading").html("Qty as per <br>Project Work");
    }
    let exchange_rate = $("#id_exchange_rate").val();
    let total_inr = 0;
    if ((!isNaN(total_amount) && (!isNaN(exchange_rate)))) {
        total_inr = parseFloat(total_amount) * parseFloat(exchange_rate);
    }
    let url = "/invoice-preview?company=" + id_company + "&client=" + id_client + "&from_address=" + id_from_address + "&to_address=" + id_to_address + "&bank_id=" + id_company_bank

    $.ajax({
        url: url,
        type: "GET",
        success: function (response) {
            console.log(response);

            var response_json = JSON.parse(response);

            //temp2
            $(".temp2 #id_company_name_temp2").text(response_json.company_name);
            $(".temp2 #id_company_address_temp2").html(response_json.company_address);
            $(".temp2 #id_footer_ph_no_temp2").text(response_json.company_phone_number);
            $(".temp2 #id_company_website_temp2").text(response_json.company_website);
            $(".temp2 #id_company_gstn_temp2").text(response_json.company_gstn);
            $(".temp2 #id_company_pan_no_temp2").text(response_json.company_pan_no);
            $(".temp2 #id_client_name_temp2").text(response_json.client_name);
            $(".temp2 #id_client_address_temp2").text(response_json.client_address);
            $(".temp2 #id_company_zip_code_temp2").text(response_json.company_zip_code);
            $(".temp2 #id_client_address_zip_temp2").text(response_json.client_address_zip);
            $(".temp2 #id_company_phone_no_temp2").text("PH - " + response_json.company_phone_number);
            $(".temp2 #id_inv_company_cin_temp2").html(response_json.company_cin);
            $(".temp2 #id_invoice_ifsc_temp2").text(response_json.company_bank_ifsc);
            $(".temp2 #id_invoice_bank_name_temp2").text(response_json.bank_name);
            $(".temp2 #id_invoice_bank_addr_temp2").text(response_json.bank_address);
            $(".temp2 #id_invoice_bank_acc_temp2").text(response_json.company_bank_acc);
        },
    });

    $(".temp2 #total_in_words_temp2").html(check_empty_value(in_words));
    $(".temp2 #invoice_total_amount_temp2").html(check_empty_value(total_amount));
    $(".temp2 #invoice_currency_temp2").html(check_empty_value(text_currency));
    $(".temp2 #invoice_currency_inr_temp2").text(check_empty_value(total_inr));

    let particulars = get_particulars(check_empty_value(prefix));
    if (text_currency==="INR"){
            if(cgst_val && cgst_val != 0){
                particulars.amounts = particulars.amounts+"<br>"+cgst_amt.toFixed(2);
                particulars.resources = particulars.resources+"<br> CGST "+cgst_val+"%";
            }
            if(sgst_val && sgst_val != 0){
                particulars.amounts = particulars.amounts+"<br>"+sgst_amt.toFixed(2);
                particulars.resources = particulars.resources+"<br> SGST "+sgst_val+"%";
            }
            if(igst_val && igst_val != 0){
                particulars.amounts = particulars.amounts+"<br>"+igst_amt.toFixed(2);
                particulars.resources = particulars.resources+"<br> IGST "+igst_val+"%";
            }

        }
    else{
        exchange_rate = check_empty_value(exchange_rate);
        text_currency = check_empty_value(text_currency);
        $("#invoice_exchange_rate").text("Per "+text_currency+" @ Rs. "+ exchange_rate);
    }
    $(".temp2 #id_invoice_p_qty").html(check_empty_value(particulars.quantities));
    $(".temp2 #id_invoice_p_rate").html(check_empty_value(particulars.unit_rates));
    $(".temp2 #id_invoice_p_amount").html(check_empty_value(particulars.amounts));
    $(".temp2 #id_invoice_p_amount").html(check_empty_value(particulars.amounts));
    $(".temp2 #invoice_total_amount").html(check_empty_value(particulars.amounts));
    $(".temp2 #id_invoice_p_items").html(check_empty_value(particulars.resources));

}


$("#id_template").change(function(){
   let val = $("#id_template :selected").val();
   alert(val);
});

$("#preview-invoice").click(function () {
    preview_invoice_temp2();
});

$("#nav-preview-tab").click(function () {
    preview_invoice_temp2();
});

});