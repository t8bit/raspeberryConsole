var igame,gloop,howManyCircles,width,height,context,platforms;
window.addEventListener('load', function(){init();}, false);

var init = function(){
	igame=document.querySelector('#igame');
	context=igame.getContext('2d');
	width=document.documentElement.clientWidth; 
	height=document.documentElement.clientHeight; 
	igame.width=width;
	igame.height=height;
	
	howManyCircles = 10, circles = [];  
	for (var i = 0; i < howManyCircles; i++)   
		circles.push([Math.random() * width, Math.random() * height, Math.random() * 100, Math.random() / 2]);
	platforms = [];
	nrPlatforms=7;
	
	console.log();	
	GameLoop(); 
}

var clear = function(){
	context.fillStyle = '#d0e7f9';  
	context.beginPath();  
	context.rect(0, 0, width, height);
	context.closePath(); 
	context.fill();  
}  

var grass=function()
{
	image = new Image();  
	image.src = "grass.png"; 
	
	for(var i=0;i<width;i=i+130){
		context.drawImage(image,i,height-129);
	}
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
 
var player = new (function(){  
	this.image = new Image();  
	this.image.src = "sprite1.png";  
    this.width = 65;  
    this.height = 95;  
  
    this.X = 0;  
    this.Y = 0;  
    
	this.frames = 2;  
	this.actualFrame = 0;  
	this.interval = 0; 
	
	this.isJumping = false;  
	this.isFalling = false;
	
	this.jumpSpeed = 0;  
	this.fallSpeed = 0;
	
	this.action=0;     
    
      
    this.setPosition = function(x, y){  
		this.X = x;  
		this.Y = y;  
	}
	
	this.jump = function() {  
		if (!this.isJumping && !this.isFalling) {  
			this.fallSpeed = 0;  
			this.isJumping = true;  
			this.jumpSpeed = 17;    
		}  
	}  
  
	this.checkJump = function() {
		this.action=160;    
		this.Y=this.Y+this.jumpSpeed;  
		if(left==1){this.X=this.X-5;}
		else if(right==1){this.X=this.X+5;}
		this.jumpSpeed--;  
		if (this.jumpSpeed == 0) {  
			this.isJumping = false;  
			this.isFalling = true;  
			this.fallSpeed = 1;  
		}  
	}  
  
	this.checkFall = function(){  
		if (this.Y > 0 ) {
			this.Y=this.Y-this.fallSpeed;
			if(left==1){this.X=this.X-5;}
			else if(right==1){this.X=this.X+5;}  
			this.fallSpeed++;  
		} else {  
			this.fallStop();  
		}  
	}  
	
	this.stop=function(){
		this.action=0;
	}
	
	this.moveLeft = function(){  
		if (this.X > 0) {    
			this.X=this.X-5;
			if (!this.isJumping && !this.isFalling) {  
				this.image.src='sprite2.png';
				this.action=80;
			}  
		}  
	}  
  
	this.moveRight = function(){  
		if (this.X + this.width < width) {   
			this.X=this.X+5;
			if (!this.isJumping && !this.isFalling) {  
				this.image.src='sprite1.png';
				this.action=80;
			}  
		}  
	}
	
	this.fallStop = function(){
		this.action=0;    
		this.isFalling = false;  
		this.fallSpeed = 0;  
	}  
	
	this.moveUp = function(){  
			this.setPosition(this.X, this.Y+5);  
	}  
  
	this.moveDown = function(){     
			this.setPosition(this.X, this.Y-5);  
	}    
	
	this.draw = function(){  
        try {
            context.drawImage(this.image,0+(this.actualFrame*56),this.action,56,90,this.X,(height-this.Y)-82,56,90);    
        } catch (e) {};  
  
		if (this.interval == 4 ) {  
			if (this.actualFrame == this.frames) {  
				this.actualFrame = 0;  
            } else {  
                this.actualFrame++;  
            }  
            this.interval = 0;  
		}  
	this.interval++;   
    }  
})();    

var Platform = function(x, y,text,type){    
	this.image = new Image();  
	this.image.src = "log.png";
	this.text=text;
	this.type=type;
	this.onCollide = function(){  
		player.fallStop();  
	};  
	
	
	
	this.x = ~~x;  
	this.y = y;  	
	this.draw = function(){  
		context.drawImage(this.image,this.x,height-this.y);
	};    
	return this;  
};



player.setPosition(~~((width-player.width)/2),  ~~((height - player.height)/2));  
var left,right;
document.addEventListener('keydown', function(e){
	switch(e.which)
	{
		case 37:
			if (!this.isJumping && !this.isFalling) {  
				left=1;
				player.moveLeft();
			}
		break;
		case 39:
			if (!this.isJumping && !this.isFalling) {  
				right=1;
				player.moveRight();
			}
		break;
		case 38:
			player.jump();
		break;
	}
}, false);

var platformWidth=80;
var platformHeight=50;

var checkCollision = function(){
	for(i=0;i<platforms.length;i++){
		if(((player.X-25) < platforms[i].x + platformWidth)&&((player.X-25) + player.width > platforms[i].x)&&((player.Y-30) + player.height > platforms[i].y)&&((player.Y-30) + player.height < platforms[i].y + platformHeight)) { 	
			platforms[i].onCollide();
		}
	}
}  

document.addEventListener('keyup', function(e){
	player.stop();
	left=0;
	right=0;
}, false);   

var GameLoop = function(){  
	clear();
	MoveCircles(5);  
	DrawCircles();
	grass();
	if (player.isJumping) player.checkJump();  
	if (player.isFalling) player.checkFall();
	for(i=0;i<platforms.length;i++)
	{	
		platforms[i].draw();
	}
	checkCollision(); 
	player.draw();
	gLoop = setTimeout(GameLoop, 1000 / 30);  
}  

  
