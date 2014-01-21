jQuery('#submitSequence').click(function(){
    bla=  $('#sequenceInput').val(); 
    alert(bla);
	jQuery.ajax({
		type: 'POST',
		url: 'cgi-bin/annotate_from_web.py',
		bla: 
        data: { upload: bla},
		beforeSend:function(){
		    alert("start");			// this is where we append a loading image
// 			jQuery('#ajax-panel').html('<div class="loading"><img src="http://www.kyleschaeffer.com/wp-content/uploads/2010/04/loading.gif" alt="Loading..." /></div>');
		},
		success:function(data){
			// successful request; do something with the data
			alert(data);
			// jQuery('#ajax-panel').empty();
// 			jQuery(data).find('item').each(function(i){
// 				jQuery('#ajax-panel').append('<h4>' + jQuery(this).find('title').text() + '</h4><p>' + jQuery(this).find('link').text() + '</p>');
// 			});
		},
		error:function(){
			// failed request; give feedback to user
// 			jQuery('#ajax-panel').html('<p class="error"><strong>Oops!</strong> Try that again in a few moments.</p>');
		}
	});
});
