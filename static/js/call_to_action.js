$('.call-to-action').click(function() {
    window.location = "/accounts/login?next=" + window.location.pathname;
});

if (!USER_AUTHENTICATED) {
    setTimeout(function() {
        $('.call-to-action').show();
    }, 180000);
}