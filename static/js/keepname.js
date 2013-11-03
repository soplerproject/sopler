// Update comments with username
                (function() {
			var comment = document.querySelector('#comment');
			var username = document.querySelector('#username');
			
			function supportsLocalStorage() {
				return typeof(Storage)!== 'undefined';
			}
			if (!supportsLocalStorage()) {
				comment.value = 'No HTML5 localStorage support, soz.';
				username.value = comment.value;
			} else {
				try {
					setInterval(function() {
						localStorage.setItem('autosave', comment.value);
						localStorage.setItem('autosave', username.value);
					}, 1000);
				} catch (e) {
					if (e == QUOTA_EXCEEDED_ERR) {
						alert('Quota exceeded!');
					}
				}
				if (localStorage.getItem('autosave')) {
					comment.value = localStorage.getItem('autosave');
					username.value = comment.value;
				}
			}
		})();
		
		$('#username').change(function() {
		$('#comment').val($(this).val());
		});

		var x = document.document.querySelector('#comment');
		for(i = 0; i < x.length; i++) {
		  x[i].value = $('#username').val();
		}
