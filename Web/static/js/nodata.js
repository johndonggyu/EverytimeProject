window.onload = function(){
	if(document.location.pathname.split('/')[1] == 'major'){
		if( $('#word_cloud')[0].innerHTML.length < 30 ){
			$('#word_cloud')[0].innerHTML = "<img src='/static/img/nodata.png'>";
		}
		if( $('#n_word_cloud')[0].innerHTML.length < 30 ){
			$('#n_word_cloud')[0].innerHTML = "<img src='/static/img/nodata.png'>";
		}
	}else{
		if( $('#word_cloud')[0].innerHTML.length < 30 ){
			$('#word_cloud')[0].innerHTML = "<img src='/static/img/nodata.png'>";
		}
	}

}