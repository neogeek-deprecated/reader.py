(function () {

	'use strict';

	/*global window, document, confirm, $, Handlebars */

	var html = document.querySelector('html'),
		feed = document.querySelector('.feed'),
		config = null;

	function reset_all_config() {

		window.localStorage.setItem('config', JSON.stringify({ read: [] }));

	}

	function hide_read_stories(data) {

		var key;

		for (key in data.stories) {

			if (data.stories.hasOwnProperty(key)) {

				if (config.read.indexOf(data.stories[key].hash) !== -1) {
					data.stories[key] = [];
					data.count--;
				}

			}

		}

		return data;

	}

	function mark_story_as_read(hash) {

		if (config.read.indexOf(hash) === -1) {
			config.read.push(hash);
		}

		window.localStorage.setItem('config', JSON.stringify(config));

	}

	if (!window.localStorage.getItem('config')) {

		reset_all_config();

	}

	config = JSON.parse(window.localStorage.getItem('config'));

	html.setAttribute('class', 'loading');

	setTimeout(function () {

		$.getJSON('/feeds', function (data) {

			var template;

			html.removeAttribute('class');

			data = hide_read_stories(data);

			template = Handlebars.compile(data.template);

			feed.innerHTML = template(data);

		});

	}, 10);

	$(document).on('click', 'a[href="#nav"]', function (e) {

		e.preventDefault();

		$('.nav ul').toggle();

	}).on('click', 'a[href="#reload"]', function (e) {

		e.preventDefault();

		window.location.reload();

	}).on('click', 'a[href="#markallasread"]', function (e) {

		e.preventDefault();

		$('.story').each(function (key, value) {

			mark_story_as_read(value.getAttribute('data-hash'));

		});

		window.location.reload();

	}).on('click', 'a[href="#resetreadstories"]', function (e) {

		e.preventDefault();

		if (confirm('Reset read stories?')) {

			reset_all_config();

			window.location.reload();

		}

	});

}());