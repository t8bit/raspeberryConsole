var position;
var width=$(window).width();
var nr_per_line=width/110;
var quantosjogos=3;
function init()
{
	position=0;
	//select first game
	$('.game').first().css('background-color','#87EDDF');
	$('.game').first().css('border','3px solid grey');
}

var deselect=function(){
	$('.game').eq(position).css('background-color','white');
	$('.game').eq(position).css('border','1px solid grey');
}
var select=function(){
	$('.game').eq(position).css('background-color','#87EDDF');
	$('.game').eq(position).css('border','3px solid grey');
}


$(document).keydown(function(e) {
	switch(e.which)
	{
		case 39:
		deselect();
		if(position<quantosjogos-1){position++;}
		select();
		break;
		
		case 37:
		deselect();
		if(position>0){position--;}
		select();
		break;
		
		case 40:
		deselect();
		if(position+nr_per_line<quantosjogos-1){position=position+nr_per_line;}
		select();
		break;
		
		case 38:
		deselect();
		if(position-nr_per_line>0){pposition=position-nr_per_line;}
		select();
		break;
		
		case 13:
		jogo=$('.game').eq(position).children().attr('href');
		$('#debug').load(jogo);
		break;
	}	

});

