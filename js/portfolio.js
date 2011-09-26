$(function(){

    var init = function() {
        var $thumbs = $('#thumbs');

        $thumbs.height($($thumbs.children().get(0)).height());

        Galleria.loadTheme('js/galleria/themes/classic/galleria.classic.min.js');
    },

    bindEvents = function() {
        var clicks = 0,
            hist = new Hist();

        $('#side-nav a').click(function(event){
            var $target = $(event.target.hash),
                $thumbs = $('#thumbs');

            event.preventDefault();

            $thumbs.height($target.height());
            $thumbs.scrollTop($target.position().top + $thumbs.scrollTop());
        });

        $('#thumbs li a').click(function(event){
            var url = event.target.parentNode.href;

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
                        window.history.pushState('#cap', '', '#cap');
                    })
                    .bind(Galleria.FULLSCREEN_EXIT, function(e){
                        $exit.hide();
                        hist.goBack();
                        console.log(window.history.length);
                    })
                    .enterFullscreen();

                $exit.click(function(){
                    gal.exitFullscreen();
                });

                hist.setBack(function(){
                    gal.exitFullscreen();
                });

            });
        });

    };

    var Hist = function() {
        var self = this,
            onBack = function(){},
            goingBack = false;

        this.setBack = function(callback){
            self.onBack = callback;
            window.onpopstate = function(event){
                goingBack = true;
                self.onBack();
                goingBack = false;
            };
        };

        this.goBack = function() {
            if (!goingBack) {
                //window.history.back();
                //window.history.replaceState('#', '', '#');
            }
        };
            
    };

    bindEvents();
    init();

});
