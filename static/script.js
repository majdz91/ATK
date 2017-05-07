function provideLink(filename, type){
	var ele = $('.infoContainer .ancher');
	ele.each(function(i, el){
		var data,url,blob;
		data = $(el).prev('.information').text();
		blob = new Blob(["\ufeff",data], {type: "text/plain"});
		url = window.URL.createObjectURL(blob);
		el.href = url;
		el.download = filename+'.'+type;
	})
};

$(document).ready(function(){
	provideLink('file', 'csv');
});