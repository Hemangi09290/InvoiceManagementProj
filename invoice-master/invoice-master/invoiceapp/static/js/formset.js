$(document).ready(function() {

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function updateElementIndex(el, prefix, ndx) {
        var id_regex = new RegExp('(' + prefix + '-\\d+)');
        var replacement = prefix + '-' + ndx;
        if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
        if (el.id) el.id = el.id.replace(id_regex, replacement);
        if (el.name) el.name = el.name.replace(id_regex, replacement);
    }

    function cloneMore(selector, prefix, add_form_class, remove_form_class, element_class) {
        var newElement = $(selector).clone(true);
        var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
        newElement.find('input,select').not(':button').not('input[type=submit]').not(':reset').each(function() {
            var name = $(this).attr('name').replace('-' + (total - 1) + '-', '-' + total + '-');
            var id = 'id_' + name;
            $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
        });
        newElement.find('label').each(function () {
            var forValue = $(this).attr('for');
            if (forValue) {
                forValue = forValue.replace('-' + (total - 1) + '-', '-' + total + '-');
                $(this).attr({'for': forValue});
            }
        });
        total++;
        $('#id_' + prefix + '-TOTAL_FORMS').val(total);
        $(selector).after(newElement);
        var conditionRow = $('.'+element_class+':not(:last)');
        conditionRow.find('.btn.'+add_form_class)
            .removeClass('btn-success').addClass('btn-danger')
            .removeClass(add_form_class).addClass(remove_form_class)
            .html('<span class="glyphicon glyphicon-minus" aria-hidden="true">Remove </span>');
        return false;
    }

    function deleteForm(prefix, btn, element_class) {
        var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
        if (total > 1) {
            btn.closest('.'+element_class+'').remove();
            var forms = $('.'+element_class+'');
            $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
            for (var i = 0, formCount = forms.length; i < formCount; i++) {
                $(forms.get(i)).find(':input').each(function () {
                    updateElementIndex(this, prefix, i);
                });
            }
            return true;
        }
        else{
            alert("can not delete last particulars.")
        }
        return false;
    }

    $(document).on('click', '.add-form-row', function (e) {
        e.preventDefault();
        cloneMore('.duplicate-row:last', 'form', 'add-form-row',
            'remove-form-row', 'duplicate-row');
        return false;
    });
    $(document).on('click', '.add-fixed-form-row', function (e) {
        e.preventDefault();
        cloneMore('.fixed-duplicate-row:last', 'fixed_p', 'add-fixed-form-row',
            'remove-fixed-form-row', 'fixed-duplicate-row');
        return false;
    });
    $(document).on('click', '.remove-form-row', function (e) {
        e.preventDefault();
        let is_deleted = deleteForm('form', $(this), 'duplicate-row');
        if (is_deleted) {
            let id = $(this).closest('.duplicate-row').find('input[type=hidden][id$="-id"]').val();

            if (id !== "") {
                var csrftoken = $("[name=csrfmiddlewaretoken]").val();
                console.log(csrftoken);
                $.ajax({
                    url: "/particulars/" + id + "/delete",
                    type: "POST",
                    headers: {
                        "X-CSRFToken": csrftoken
                    },
                    success: function (response) {
                        console.log(response);
                    },

                });
            } else {
                console.log("nothing found");
            }
        }
        return false;
    });
    $(document).on('click', '.remove-fixed-form-row', function (e) {
        e.preventDefault();
        let is_deleted = deleteForm('fixed_p', $(this), 'fixed-duplicate-row');
        if (is_deleted) {
            let id = $(this).closest('.fixed-duplicate-row').find('input[type=hidden][id$="-id"]').val();

            if (id !== "") {
                var csrftoken = $("[name=csrfmiddlewaretoken]").val();
                console.log(csrftoken);
                $.ajax({
                    url: "/particulars/" + id + "/delete",
                    type: "POST",
                    headers: {
                        "X-CSRFToken": csrftoken
                    },
                    success: function (response) {
                        console.log(response);
                    },

                });
            } else {
                console.log("nothing found");
            }
        }
        return false;
    });
});
