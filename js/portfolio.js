$(function(){

    var init = function() {
        var $thumbs = $('#thumbs');

        $thumbs.height($($thumbs.children().get(0)).height());
    },

    bindEvents = function() {

        $('#side-nav a').click(function(event){
            var $target = $(event.target.hash),
                $thumbs = $('#thumbs');

            event.preventDefault();

            $thumbs.height($target.height());
            $thumbs.scrollTop($target.position().top + $thumbs.scrollTop());

            //$thumbs.animate({
            //    height: $target.height(),
            //    scrollTop: $target.position().top + $thumbs.scrollTop()
            //}, 500);
        });

    };

    bindEvents();
    init();

});
