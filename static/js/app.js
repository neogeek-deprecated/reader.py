$.getJSON('/feed', function (data) {

	$('.feed').html(Mustache.render('<ul>{{#data}} <li class="story" data-origin="{{origin}}"><span class="icon"></span><a href="{{link}}" target="_blank">{{title}}</a> <i class="site">{{site}}</i></li> {{/data}}</ul>', data));

});