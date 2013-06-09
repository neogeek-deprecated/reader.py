'use strict';

function reset_all_config () {

	localStorage.setItem('config', JSON.stringify({ read: [] }));

}

function hide_read_stories (data) {

	for (var key in data.stories) {

		if (config.read.indexOf(data.stories[key]['hash']) != -1) {
			data.stories[key] = [];
			data.count--;
		}

	}

	return data;

}

function mark_story_as_read (hash) {

	if (config.read.indexOf(hash) == -1) {
		config.read.push(hash);
	}

	localStorage.setItem('config', JSON.stringify(config));

}

if (!localStorage.getItem('config')) {

	reset_all_config();

}

var html = document.querySelector('html'),
	feed = document.querySelector('.feed'),
	config = JSON.parse(localStorage.getItem('config'));

html.setAttribute('class', 'loading');

setTimeout(function () {

	$.getJSON('/feeds', function (data) {

		html.removeAttribute('class');

		data = hide_read_stories(data);

		var template = Handlebars.compile(data.template);

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

}).on('click', 'a[href="#markasread"]', function (e) {

	e.preventDefault();

	mark_story_as_read(this.parentNode.parentNode.getAttribute('data-hash'));

	var ul = this.parentNode.parentNode.parentNode;

	ul.removeChild(this.parentNode.parentNode);

	if (!ul.getElementsByTagName('li').length) {

		feed.innerHTML = '<p>No new stories.</p>';

	}

});