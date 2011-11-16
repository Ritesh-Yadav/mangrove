$(document).ready(function() {
    $("#add_subject_type").accordion({collapsible: true,autoHeight:false, active:2});

    $("#add_new_subject_type").live("click", function() {
        $("#type_message").html('');
        $("#type_message").removeClass("message-box");
        $("#add_subject_type_content").removeClass("none");
        $("#id_entity_type_text").val("");
    });

    function should_append(options, new_type) {
        var i =0;
        for (i; i < options.length; i=i+1) {
            if (new_type == options[i].value){
                return false;
            }
        }
        return true;
    }
    
    $("#add_type").live("click", function() {
        $("#type_message").html("<span class='ajax_loader_small'></span>");
        var new_type = $("#id_entity_type_text").val().toLowerCase();
        var default_form_model = $("#use-default-form").attr("checked");
        $.post("/entity/type/create/", { entity_type_regex: new_type, default_form_model: default_form_model},
                function(response) {
                    var data = JSON.parse(response);
                    if (data.success) {
                        if(default_form_model) {
                            var options = $("#id_entity_type").attr('options');
                            if (should_append(options, new_type)) {
                                $("#id_entity_type").prepend($('<option></option>').val(new_type).html(new_type));
                            }
                            $('#id_entity_type').val(0);
                            $('#id_entity_type').trigger('change');
                            $("#add_subject_type").accordion({collapsible: true,autoHeight:false, active:2});
                            $("#type_message").html('');
                            $("#type_message").removeClass("message-box");
                            $("#id_entity_type_text").val("");
                        } else {
                            window.location.replace('/entity/registration/' + new_type);
                        }
                    }
                    else {
                        $("#type_message").html(data.message);
                        $("#type_message").addClass("message-box");
                    }
            });
    });

});
