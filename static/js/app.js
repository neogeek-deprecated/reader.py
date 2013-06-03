'use strict';

if ('localStorage' in window) {

	if (!localStorage.getItem('config')) {
		localStorage.setItem('config', JSON.stringify({ deleted: [] }));
	}

	var config = JSON.parse(localStorage.getItem('config'));

}

$.getJSON('/feeds', function (data) {

	if (config) {

		for (var key in data.stories) {

			if (config.deleted.indexOf(data.stories[key]['hash']) != -1) {
				data.stories[key] = [];
			}

		}

	}

	var template = Handlebars.compile(data.template);

	$('.feed').html(template(data.stories));

});

$(document).on('click', 'a[href="#readlater"]', function (e) {

	e.preventDefault();

}).on('click', 'a[href="#delete"]', function (e) {

	e.preventDefault();

	if (confirm('Are you sure you want to delete this story?')) {

		var hash = this.parentNode.parentNode.getAttribute('data-hash');

		if (config) {

			if (config.deleted.indexOf(hash) == -1) {
				config.deleted.push(hash);
			}

			localStorage.setItem('config', JSON.stringify(config));

		}

		this.parentNode.parentNode.parentNode.removeChild(this.parentNode.parentNode);

	}

});