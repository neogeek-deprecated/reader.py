(function () {

    'use strict';

    var $html = $('html'),
        $feed = $('.feed'),
        config = null;

    function reset_config() {

        window.localStorage.setItem('config', JSON.stringify({'read': []}));

    }

    function return_unread_stories(stories) {

        return stories.filter(function (story) {
            return config.read.indexOf(story.hash) === -1;
        });

    }

    function mark_stories_as_read(stories) {

        window.localStorage.setItem('config', JSON.stringify({
            'read': config.read.concat(stories)
        }));

    }

    if (!window.localStorage.getItem('config')) {

        reset_config();

    }

    config = JSON.parse(window.localStorage.getItem('config'));

    $html.addClass('loading');

    setTimeout(function () {

        $.getJSON('/feed').done(function (data) {

            var template;

            $html.removeClass('loading');

            template = Handlebars.compile(data.template);

            $feed.html(template({
                stories: return_unread_stories(data.stories)
            }));

        }).fail(function () {

            $html.removeAttribute('loading');

            $feed.html('<p>Error processing request.</p>');

        });

    }, 10);

    $(document).on('click', 'a[href="#nav"]', function (e) {

        e.preventDefault();

        $('nav ul').toggle();

    }).on('click', 'a[href="#reload"]', function (e) {

        e.preventDefault();

        window.location.reload();

    }).on('click', 'a[href="#markallasread"]', function (e) {

        e.preventDefault();

        mark_stories_as_read($('.story').map(function () {
            return $(this).attr('data-hash');
        }).toArray());

        window.location.reload();

    });

}());
