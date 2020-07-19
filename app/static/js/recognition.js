$( document ).ready(function() {
    var button = document.getElementById('size');

	button.onclick = function() {
		var div = document.getElementById('sizedetails');
		if (div.style.display !== 'none') {
		div.style.display = 'none';
		}
		else {
		div.style.display = 'block';
		}
	};

	var button = document.getElementById('fragrance');

	button.onclick = function() {
		var div = document.getElementById('fragrancedetails');
		if (div.style.display !== 'none') {
		div.style.display = 'none';
		}
		else {
		div.style.display = 'block';
		}
	};

	var button = document.getElementById('time');

	button.onclick = function() {
		var div = document.getElementById('timedetails');
		if (div.style.display !== 'none') {
		div.style.display = 'none';
		}
		else {
		div.style.display = 'block';
		}
	};
})
