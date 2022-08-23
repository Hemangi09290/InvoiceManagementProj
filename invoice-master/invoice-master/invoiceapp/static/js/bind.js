$(document).ready(function() {

    function isEmpty(obj) {
  return Object.keys(obj).length === 0;
}

$("#id_client").on("change", function (e) {
    console.log("changed");
    let client_value = e.target.value;
    $.ajax({
            url: "/client-address/"+ client_value +"?type=client",
            type: "GET",
            success: function(response) {
                console.log(response);
                response = JSON.parse(response);
                var $el = $("#id_to_address");
                $el.empty(); // remove old options
                $.each(response.address, function (value, key) {
                    $el.append($("<option></option>")
                        .attr("value", value).text(key));
                });
                $("#id_agreement_date").val(response.agreement_date);
                $("#id_project_type").val(response.project_type);
                show_hide_particulars_panel("", response.project_type);
            },

        });
});
$("#id_company").on("change", function (e) {
    console.log("changed");
    let client_value = e.target.value;
    $.ajax({
            url: "/client-address/"+ client_value +"?type=company",
            type: "GET",
            success: function(response) {
                console.log(response);
                response = JSON.parse(response)
                var $el = $("#id_from_address");
                $el.empty(); // remove old options
                $.each(response.address, function (value, key) {
                    $el.append($("<option></option>")
                        .attr("value", value).text(key));
                });

                var $elc = $("#id_company_bank");
                $elc.empty(); // remove old options
                $.each(response.bank, function (value, key) {
                    $elc.append($("<option></option>")
                        .attr("value", value).text(key));
                });
            },

        });
});


let client_value = $("#id_company :selected").val();
if(client_value) {
    $.ajax({
        url: "/client-address/" + client_value + "?type=company",
        type: "GET",
        success: function (response) {
            console.log(response);
            response = JSON.parse(response)
            var $el = $("#id_from_address");
            $el.empty(); // remove old options
            $.each(response.address, function (value, key) {
                $el.append($("<option></option>")
                    .attr("value", value).text(key));
            });

            var $elc = $("#id_company_bank");
            $elc.empty(); // remove old options
            $.each(response.bank, function (value, key) {
                $elc.append($("<option></option>")
                    .attr("value", value).text(key));
            });
        },
    });
}

});


function show_hide_particulars_panel(id, value){
    $.fn.dataTable.ext.errMode = 'none';
    let selected_currency = $("#id_currency :selected").text();
    if (value=="fixed price"){
        $('#project_table_fixed').show();
        $('#project_table').hide();

        $('#project_table_fixed').DataTable({
                "searching": false,
                "bLengthChange": false,
                "fixedHeader": true,
                "paging": false,
                "bDestroy": false
            });
        $('#project_table_info').hide();
        $('#project_table_fixed_info').hide();

        if(selected_currency == 'INR'){
            $("#fixed-tax-row").show();
            $("#id_sgst").val(0);
            $("#id_cgst").val(0);
            $("#id_igst").val(0);
            $("#id_fixed_sgst").val(0);
            $("#id_fixed_cgst").val(0);
            $("#id_fixed_igst").val(0);
            $("#tax-row").hide();
        }else{
           $("#id_sgst").val(0);
            $("#id_cgst").val(0);
            $("#id_igst").val(0);
            $("#id_fixed_sgst").val(0);
            $("#id_fixed_cgst").val(0);
            $("#id_fixed_igst").val(0);
            $("#fixed-tax-row").hide();
            $("#tax-row").hide();
        }

    }else{
        $('#project_table_fixed').hide();
        $('#project_table').show();
        $('#project_table_info').hide();
        $('#project_table_fixed_info').hide();
        $('#project_table').DataTable({
                "searching": false,
                "bLengthChange": false,
                "fixedHeader": true,
                "paging": false,
                "bDestroy": false
            });
        if(selected_currency == 'INR'){
            $("#fixed-tax-row").hide();
            $("#id_sgst").val(0);
            $("#id_cgst").val(0);
            $("#id_igst").val(0);
            $("#id_fixed_sgst").val(0);
            $("#id_fixed_cgst").val(0);
            $("#id_fixed_igst").val(0);
            $("#tax-row").show();
        }else{
            $("#id_sgst").val(0);
            $("#id_cgst").val(0);
            $("#id_igst").val(0);
            $("#id_fixed_sgst").val(0);
            $("#id_fixed_cgst").val(0);
            $("#id_fixed_igst").val(0);
            $("#fixed-tax-row").hide();
            $("#tax-row").hide();
        }

    }
}

function update_currency(id, value){
    let selected_ele = $("#"+id+" :selected");
    let selected_val = selected_ele.text();
    let selected_id = selected_ele.val();
    if (selected_id){
        $.ajax({
            url: "/currency/"+ selected_id,
            type: "GET",
            async: false,
            success: function(response) {
                response = JSON.parse(response);
                $("#currency_sub_unit").text(response.sub_unit);
                $("#currency_unit").text(response.currency_unit);
            },
        });
    }
    let selected_Project_type_val = $("#id_project_type  :selected").val();
    $("#id_currency_type").text(selected_val);
    $("#id_fixed_currency_type").text(selected_val);
    if (selected_val === 'INR'){
        $("#id_exchange_rate").val(1);
        $("#div_exchange_rate").hide();
        if (selected_Project_type_val !== "hourly"){
            $("#fixed-tax-row").show();
            $("#id_sgst").val(0);
            $("#id_cgst").val(0);
            $("#id_igst").val(0);
            $("#id_fixed_sgst").val(0);
            $("#id_fixed_cgst").val(0);
            $("#id_fixed_igst").val(0);
            $("#tax-row").hide();

        }else{
            $("#fixed-tax-row").hide();
            $("#id_sgst").val(0);
            $("#id_cgst").val(0);
            $("#id_igst").val(0);
            $("#id_fixed_sgst").val(0);
            $("#id_fixed_cgst").val(0);
            $("#id_fixed_igst").val(0);
            $("#tax-row").show();
        }

    }else{
        $("#div_exchange_rate").show();
        $("#id_sgst").val(0);
        $("#id_cgst").val(0);
        $("#id_igst").val(0);
        $("#id_fixed_sgst").val(0);
        $("#id_fixed_cgst").val(0);
        $("#id_fixed_igst").val(0);
        $("#fixed-tax-row").hide();
        $("#tax-row").hide();
    }
    let total_amount = $("#total_amount").val();
    let in_words_id = 'in_words';
    if (selected_Project_type_val !== "hourly"){
        in_words_id  = 'fixed_in_words';
        total_amount = $("#fixed_total_amount").val();
    }
    show_in_words(total_amount, in_words_id);
}