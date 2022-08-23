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

    function cloneMore(selector, prefix) {
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
        console.log(total);
    

        $('#id_' + prefix + '-TOTAL_FORMS').val(total);
        $(selector).after(newElement);
        var conditionRow = $('.duplicate-row:not(:last)');
        conditionRow.find('.btn.add-form-row')
            .removeClass('btn-primary').addClass('btn-danger')
            .removeClass('add-form-row').addClass('remove-form-row')
            .html('<span class="glyphicon glyphicon-minus" aria-hidden="true">Remove </span>');
        return false;
    }

    function deleteForm(prefix, btn) {
        var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
        if (total > 1) {
            btn.closest('.duplicate-row').remove();
            var forms = $('.duplicate-row');
            $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
            for (var i = 0, formCount = forms.length; i < formCount; i++) {
                $(forms.get(i)).find(':input').each(function () {
                    updateElementIndex(this, prefix, i);
                });
            }
            return true;
        }
        else{
            alert("can not delete last bank detail.")
        }
        return false;
    }




    $(document).on('click', '.add-form-row', function (e) {
        e.preventDefault();
        cloneMore('.duplicate-row:last', 'form');
        return false;
    });
    $(document).on('click', '.remove-form-row', function (e) {
        e.preventDefault();
        let is_deleted = deleteForm('form', $(this));
    if (is_deleted) {
        console.log($(this).closest('.duplicate-row').find('input[type=hidden][id$="-id"]'))

        let id = $(this).closest('.duplicate-row').find('input[type=hidden][id$="-id"]').val();

        if (id) {
            var csrftoken = $("[name=csrfmiddlewaretoken]").val();
            console.log(csrftoken);
            $.ajax({
                url: "/bank/" + id + "/delete",
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
