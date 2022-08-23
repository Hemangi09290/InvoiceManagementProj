
var a = ['','One ','Two ','Three ','Four ', 'Five ','Six ','Seven ','Eight ','Nine ','Ten ','Eleven ','Twelve ','Thirteen ','Fourteen ','Fifteen ','Sixteen ','Seventeen ','Eighteen ','Nineteen '];
var b = ['', '', 'Twenty','Thirty','Forty','Fifty', 'Sixty','Seventy','Eighty','Ninety'];

function inWords (num) {
    if ((num = num.toString()).length > 9) return 'overflow';
    let n = ('000000000' + num).substr(-9).match(/^(\d{2})(\d{2})(\d{2})(\d{1})(\d{2})$/);
    if (!n) return; var str = '';
    str += (n[1] != 0) ? (a[Number(n[1])] || b[n[1][0]] + ' ' + a[n[1][1]]) + 'Crore ' : '';
    str += (n[2] != 0) ? (a[Number(n[2])] || b[n[2][0]] + ' ' + a[n[2][1]]) + 'Lakh ' : '';
    str += (n[3] != 0) ? (a[Number(n[3])] || b[n[3][0]] + ' ' + a[n[3][1]]) + 'Thousand ' : '';
    str += (n[4] != 0) ? (a[Number(n[4])] || b[n[4][0]] + ' ' + a[n[4][1]]) + 'Hundred ' : '';
    str += (n[5] != 0) ? ((str !== '') ? 'and ' : '') + (a[Number(n[5])] || b[n[5][0]] + ' ' + a[n[5][1]]) : '';
    return str;
}

//
// function calculate_totals() {
//     console.log("called");
//     let total_forms = $("#id_fixed_p-TOTAL_FORMS").val();
//     console.log(total_forms);
//     var i;
//     let qty = 0, amt = 0;
//     for (i = 0; i < total_forms; i++) {
//         let quantity = $("#id_form-"+i.toString()+"-quantity").val();
//         let unit_rate_val = $("#id_form-"+i.toString()+"-unit_rate").val();
//         let amount = $("#id_form-"+i.toString()+"-amount").val();
//         console.log(quantity, unit_rate_val, amount);
//         if (!isNaN(quantity)) {
//             qty = qty + parseInt(quantity);
//         }
//         if (!isNaN(amount)) {
//             amt = amt + parseFloat(amount);
//         }
//         if (!isNaN(unit_rate_val)) {
//             unit_rate = unit_rate + parseFloat(unit_rate_val);
//         }
//
//     }
//     if (qty) {
//         $("#total_hours").text(qty);
//     }
//
//     if (unit_rate) {
//         $("#total_unit_rate").text(unit_rate);
//     }
//
//     if (amt) {
//         $("#total_amount").val(amt);
//         $("#in_words").text(inWords(amt));
//     }
// }

function calculate_totals() {
    let total_forms = $("#id_form-TOTAL_FORMS").val();
    var i;
    let qty = 0, unit_rate = 0, amt = 0;
    for (i = 0; i < total_forms; i++) {
        let quantity = $("#id_form-"+i.toString()+"-quantity").val();
        let unit_rate_val = $("#id_form-"+i.toString()+"-unit_rate").val();
        let amount = $("#id_form-"+i.toString()+"-amount").val();
        console.log(quantity, unit_rate_val, amount)
        if (!isNaN(quantity)) {
            qty = qty + parseFloat(quantity);
        }
        if (!isNaN(amount)) {
            amt = amt + parseFloat(amount);
        }
        if (!isNaN(unit_rate_val)) {
            unit_rate = unit_rate + parseFloat(unit_rate_val);
        }

    }
    if (qty) {
        $("#total_hours").text(qty.toFixed(2));
    }

    if (unit_rate) {
        $("#total_unit_rate").text(unit_rate.toFixed(2));
    }

    if (amt) {
        if ($("#tax-row").is(':visible')){
            amt = amt + amt*parseFloat($("#id_cgst").val())/100;
            amt = amt + amt*parseFloat($("#id_sgst").val())/100;
            amt = amt + amt*parseFloat($("#id_igst").val())/100;
        }
        $("#total_amount").val(amt.toFixed(2));
        show_in_words(amt.toFixed(2), 'in_words');
    }
}


function show_in_words(amount, in_words_id){
    let selected_sub_unit_val = $("#currency_sub_unit").text();
    let selected_unit_val = $("#currency_unit").text();
    if (amount.includes('.')){
        let amount_in_words = "";
        let currency_prefix = amount.split('.')[0];
        amount_in_words = inWords(parseInt(currency_prefix)) +" "+ selected_unit_val;
        let currency_suffix = amount.split('.')[1];
        if (parseInt(currency_suffix)){
            amount_in_words = amount_in_words+" and "+ inWords(parseInt(currency_suffix)) +" "+selected_sub_unit_val;
        }

        $("#"+in_words_id).text(amount_in_words +" only.");
    } else {
        $("#"+in_words_id).text(inWords(parseInt(amount))+" only.");
    }
}

function update_calculations(total_hours, unit_rate, total_amount){

    total_hours = parseFloat(total_hours);
    unit_rate = parseFloat(unit_rate);
    let total_amt = parseFloat($("#total_amount").val())
    if (total_hours){
        let total_hrs = parseFloat($("#total_hours").text()) + parseFloat(total_hours);
        $("#total_hours").text(total_hrs.toFixed(2));
    }

    if (unit_rate){
        let total_rate = parseFloat($("#total_unit_rate").text()) + parseFloat(unit_rate);
        $("#total_unit_rate").text(total_rate.toFixed(2));
    }

    if (total_amount){
        total_amt = total_amt + total_amount;
        total_amt = total_amt.toFixed(2);
        $("#total_amount").val(total_amt);
    }
    if (total_amount)
    {
        show_in_words(total_amount.toFixed(2), 'in_words');
    }
}

function calculate_amount(id, value) {

    let total_amount = 0;

    let amount_ele = $("#" + id.replace("amount", "quantity"));
    let  unit_rate = $("#"+id.replace("amount", "unit_rate")).val();

    if (value &&  unit_rate && unit_rate !== 0) {
        total_amount = parseFloat(value) / parseFloat(unit_rate);
        amount_ele.val(total_amount.toFixed(2));
    }

    calculate_totals();
}
function calculate_total_amount(id, value) {
    let total_quantity = 0;
    let  amount = $("#"+id.replace("unit_rate", "amount")).val();
    let quantity_ele = $("#" + id.replace("unit_rate", "quantity"));

    if (value &&  amount) {
        total_quantity =  parseFloat(amount) / parseFloat(value) ;
        quantity_ele.val(total_quantity.toFixed(2));
    }
    calculate_totals();
}


function calculate_fixed_quantity(id, value){
        let total_forms = $("#id_fixed_p-TOTAL_FORMS").val();
        let qty = 0;
        for (i = 0; i < total_forms; i++) {
            let quantity = $("#id_fixed_p-" + i.toString() + "-quantity").val();
            if (!isNaN(quantity)) {
                qty = qty + parseFloat(quantity);
            }
        }
        if (!isNaN(qty)){
            $("#fixed_total_hours").val(qty.toFixed(2))
        }
}

function calculate_fixed_amount(id, value){
        let total_forms = $("#id_fixed_p-TOTAL_FORMS").val();
        let amt = 0;
        for (i = 0; i < total_forms; i++) {
            let amount = $("#id_fixed_p-" + i.toString() + "-amount").val();

            console.log(amount);
            if (!isNaN(amount)) {
                amt = amt + parseFloat(amount)  ;
            }
        }
        if (!isNaN(amt)){

            if ($("#fixed-tax-row").is(':visible')){
                amt = amt + amt*parseFloat($("#id_fixed_cgst").val())/100;
                amt = amt + amt*parseFloat($("#id_fixed_sgst").val())/100;
                amt = amt + amt*parseFloat($("#id_fixed_igst").val())/100;
        }
            $("#fixed_total_amount").val(amt.toFixed(2));
            show_in_words(amt.toFixed(2), 'fixed_in_words');
        }
}

function calculate_fixed_tax(){
    var amt = parseFloat($("#fixed_total_amount").val());
    if ($("#fixed-tax-row").is(':visible')){
                amt = amt + amt*parseFloat($("#id_fixed_cgst").val())/100;
                amt = amt + amt*parseFloat($("#id_fixed_sgst").val())/100;
                amt = amt + amt*parseFloat($("#id_fixed_igst").val())/100;
        }
    $("#fixed_total_amount").val(amt.toFixed(2));
    show_in_words(amt.toFixed(2), 'fixed_in_words');
}