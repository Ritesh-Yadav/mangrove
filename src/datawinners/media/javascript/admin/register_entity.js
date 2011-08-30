DW.viewModel = {};

$(document).ready(function() {
     $('#autogen').unbind('change').change(function(event) {
        if ($('#autogen').attr('checked') != true) {
            $('#short_name').attr('disabled', '');

        }
        else {
            $('#short_name').removeClass('error');
            $("#short_name").parent().find('label.error').hide();
            $('#short_name').val("");
            DW.viewModel.message.s('');
            $('#short_name').attr('disabled', 'disabled');
        }
    });
    $('#register_entity').unbind('click').click(function() {
        if ($('#question_form').valid()) {
            $(this).after("<span class='ajax_loader_small'></span>");
            DW.viewModel.message.l($('#id_location').val());
            if (DW.viewModel.message.s())
                DW.viewModel.message.s(DW.viewModel.message.s().toLowerCase());
            $.post($('#post_url').val(), {'format': 'json', 'data': JSON.stringify(ko.toJS(DW.viewModel), null, 1)},
                    function(response) {
                        var d = $.parseJSON(response);
                        $('#message').remove();
                        $(".ajax_loader_small").hide();
                        if (d.success) {
                            $('<div id="message" class="success-message-box">' + d.message + '</div>').insertBefore($('#question_form'));
                            DW.viewModel.message.n('');
                            DW.viewModel.message.s('');
                            DW.viewModel.message.t('');
                            DW.viewModel.message.l('');
                            DW.viewModel.message.d('');
                            DW.viewModel.message.m('');
                            DW.viewModel.message.g('');
                            $('#id_entity_type').val(0);
                        }
                        else {
                            $(".ajax_loader_small").hide();
                            $('<div id="message" class="error_message message-box">' + d.message + '</span>').insertBefore($('#question_form'));
                        }
                    }
            );
        }
    }
    );
    $.widget("custom.catcomplete", $.ui.autocomplete, {
        _renderMenu: function(ul, items) {
            var self = this,
                    currentCategory = "";
            $.each(items, function(index, item) {
                if (item.category != currentCategory) {
                    ul.append("<li class='ui-autocomplete-category'>" + item.category + "</li>");
                    currentCategory = item.category;
                }
                self._renderItem(ul, item);
            });
        }
    });

    $("#id_location").catcomplete({
        source: "/places"
    });

    DW.viewModel = {
        'message': {
            'n': ko.observable(),
            's': ko.observable(),
            't': ko.observable(),
            'l': ko.observable(),
            'd': ko.observable(),
            'm': ko.observable(),
            'g': ko.observable(),
            'form_code': 'reg'
        },
        'transport': 'web',
        'source': 'web',
        'destination': 'mangrove'
    };

    ko.applyBindings(DW.viewModel);

});

