window.addEventListener('load', function(){init();}, false);

document.addEventListener('keydown', function(e){
	console.log(e.which);
	switch(e.which)
	{
		case 65:	
			right=0;
			player.moveLeft();
		break;
		case 68:  
			right=1;
			player.moveRight();
		break;
		case 72:
			player.murro(3);
		break;
		case 74:
			player.murro(4);
		break;
		case 75:
			player.murro(5);
		break;
		case 76:
			player.murro(6);
		break;
	}
}, false);
 

document.addEventListener('keyup', function(e){
	player.stop();
	left=0;
	right=0;
}, false);   
