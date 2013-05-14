function openPopup(name, url, width, height){

    var properties = [
            'width='+width,
            'height='+height,
            'location=false',
            'menubar=false',
            'resizable=false',
            'status=true',
            'toolbar=false',
            'scrollbars=yes'
        ],
        popup = window.open(url, name, properties.join(','));

    if(window.focus) {
        popup.focus();
    }

    return popup;
}

$('.survey-link').click(function(event) {
    var type = $(this).attr('data-survey');

    event.preventDefault();

    openPopup('hi', 'http://survey.oneandonly.im/' + type, screen.width / 2, screen.height / 5 * 4);
});