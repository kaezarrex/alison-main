$(function(){

    var init = function() {
        var $thumbs = $('#thumbs');

        $thumbs.height($($thumbs.children().get(0)).height());

        Galleria.loadTheme('js/galleria/themes/classic/galleria.classic.min.js');
    },

    bindEvents = function() {
        var clicks = 0;

        $('#side-nav a').click(function(event){
            var $target = $(event.target.hash),
                $thumbs = $('#thumbs');

            event.preventDefault();

            $thumbs.height($target.height());
            $thumbs.scrollTop($target.position().top + $thumbs.scrollTop());
        });

        $('#thumbs li a').click(function(event){
            var url = $(this)[0].href;

            event.preventDefault();

            $.get(url, function(data) {
                var $images = $(data).find('#project img'),
                    $exit = $('.exit-button'),
                    prefix = /.+\//.exec(url)[0],
                    data = [];

                $images.each(function(){
                    data.push({
                        image: prefix + $(this).attr('src')
                    });
                });

                $('#galleria').galleria({
                    dataSource: data
                });

                gal = Galleria.get(clicks++)
                    .bind(Galleria.FULLSCREEN_ENTER, function(e){
                        $exit.show();
                    })
                    .bind(Galleria.FULLSCREEN_EXIT, function(e){
                        $exit.hide();
                    })
                    .enterFullscreen();

                $exit.click(function(){
                    gal.exitFullscreen();
                });

            });
        });

    };

    bindEvents();
    init();

});
