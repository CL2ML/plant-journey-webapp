$( document ).ready(function() {
    
    var buttons = document.querySelectorAll("[id='size']");
    
    for(var i = 0; i < buttons.length; i++) 
    // var button = document.getElementById('size');

        

        buttons[i].onclick = function() {          
            var details = document.querySelectorAll("[id='sizedetails']");
            
            for(var i = 0; i < details.length; i++) 
            
                if (details[i].style.display !== 'none') {
                    details[i].style.display = 'none';
                }
                else {
                    details[i].style.display = 'block';
                }
	};
});
