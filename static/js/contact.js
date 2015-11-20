$('#happy-to-contact').click(function() {
    $(this).parents('.alert-box').hide();
    $.post("/communicate", {'contact': 'True'});
    return false;
});

$('#rather-not').click(function() {
    $(this).parents('.alert-box').hide();
    $.post("/communicate", {'contact': 'False'});
    return false;
});