window.isValidURL = (function() {// wrapped in self calling function to prevent global pollution

     //URL pattern based on rfc1738 and rfc3986
    var rg_pctEncoded = "%[0-9a-fA-F]{2}";
    var rg_protocol = "(http|https):\\/\\/";

    var rg_userinfo = "([a-zA-Z0-9$\\-_.+!*'(),;:&=]|" + rg_pctEncoded + ")+" + "@";

    var rg_decOctet = "(25[0-5]|2[0-4][0-9]|[0-1][0-9][0-9]|[1-9][0-9]|[0-9])"; // 0-255
    var rg_ipv4address = "(" + rg_decOctet + "(\\." + rg_decOctet + "){3}" + ")";
    var rg_hostname = "([a-zA-Z0-9\\-\\u00C0-\\u017F]+\\.)+([a-zA-Z]{2,})";
    var rg_port = "[0-9]+";

    var rg_hostport = "(" + rg_ipv4address + "|localhost|" + rg_hostname + ")(:" + rg_port + ")?";

    // chars sets
    // safe           = "$" | "-" | "_" | "." | "+"
    // extra          = "!" | "*" | "'" | "(" | ")" | ","
    // hsegment       = *[ alpha | digit | safe | extra | ";" | ":" | "@" | "&" | "=" | escape ]
    var rg_pchar = "a-zA-Z0-9$\\-_.+!*'(),;:@&=";
    var rg_segment = "([" + rg_pchar + "]|" + rg_pctEncoded + ")*";

    var rg_path = rg_segment + "(\\/" + rg_segment + ")*";
    var rg_query = "\\?" + "([" + rg_pchar + "/?]|" + rg_pctEncoded + ")*";
    var rg_fragment = "\\#" + "([" + rg_pchar + "/?]|" + rg_pctEncoded + ")*";

    var rgHttpUrl = new RegExp( 
        "^"
        + rg_protocol
        + "(" + rg_userinfo + ")?"
        + rg_hostport
        + "(\\/"
        + "(" + rg_path + ")?"
        + "(" + rg_query + ")?"
        + "(" + rg_fragment + ")?"
        + ")?"
        + "$"
    );

    // export public function
    return function (url) {
        if (rgHttpUrl.test(url)) {
            return true;
        } else {
            return false;
        }
    };
})();

// $('#id_url').change(function() {
//     if ($('#id_title').val() == '') {
//         // Only if there isn't a title already do we import one
//         var url = $(this).val();
//         $.post('/lookup', {url: url}, function(r) {
//             content = "";
//             if (r.images.length > 0) {
//                 content = "![](" + r.images[0].url + ")\n\n";
//             }
//             $('#id_title').val(r.title);
//             if ($('#id_description').val() == "") {
//                 $('#id_description').val(content + r.content);
//                 editor._setupTextareaSync();
//             }
//         });
//     }
// })

$('#submit-topic-step-1 form').submit(function() {
    var url = $(this).find('[name="url"]').val();
    if (!isValidURL(url)) {
        alert("The URL must be valid");
        return false;
    }

    $.post('/lookup', {url: url}, function(r) {
        // $('#title').val(r.title);
        // $('#description').val(content + r.content);
        // editor._setupTextareaSync();
        $('[name="url"]').val(url);
        $('[name="title"]').val(r.title);
        $('[name="description"]').val(r.content);

        if (r.images.length > 0) {
            $('[name="image"]').val(r.images[0].url);
            $('#submit-topic').find('img').attr('src', r.images[0].url);
            $('#topic-image').show();
        } else {
            $('[name="image"]').val("");
            $('#topic-image').hide();
        }

        $('#submit-topic-step-1').hide();
        $('#submit-topic').show();
    });
    return false;
});

$('#cancel-submit').click(function() {
    $('#submit-topic').hide();
    $('#submit-topic-step-1').show();
});