$('#id_url').change(function() {
    if ($('#id_title').val() == '') {
        // Only if there isn't a title already do we import one
        var url = $(this).val();
        $.post('/lookup', {url: url}, function(r) {
            $('#id_title').val(r.title);
            if ($('#id_description').val() == "") {
                // $('#id_description').val(r.content);
                // editor._setupTextareaSync();
            }
        });
    }
})