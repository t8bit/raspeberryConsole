var CreateCircles=function(){
	howManyCircles = 10, circles = [];  
	for (var i = 0; i < howManyCircles; i++)   
		circles.push([Math.random() * width, Math.random() * height, Math.random() * 100, Math.random() / 2]);
	platforms = [];
	nrPlatforms=7;
}

var DrawCircles = function(){  
	for (var i = 0; i < howManyCircles; i++) {  
		context.fillStyle = 'rgba(255, 255, 255, ' + circles[i][3] + ')';  
		context.beginPath();  
		context.arc(circles[i][0], circles[i][1], circles[i][2], 0, Math.PI * 2, true);  
		context.closePath();  
		context.fill();  
	}  
};

var MoveCircles = function(deltaY){  
	for (var i = 0; i < howManyCircles; i++) {  
		if (circles[i][1] - circles[i][2] > height) {    
			circles[i][0] = Math.random() * width;  
			circles[i][2] = Math.random() * 100;  
			circles[i][1] = 0 - circles[i][2];  
			circles[i][3] = Math.random() / 2;  
		} else {   
			circles[i][1] += deltaY;  
		}	  
	}  
}; 
