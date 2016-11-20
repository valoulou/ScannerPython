function addRowHandlers(laCellule) {

    request = $.ajax({
    	 url: 'script.php',
         data: {mid: laCellule.innerHTML},
         type: 'post',
         success: function(output) {
                      alert(output);
                  }
	});
}
