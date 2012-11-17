var player = new (function(){  
	this.image = new Image();  
	this.image.src = "images/sprite1.png";  
    this.width = 65;  
    this.height = 95;  
  
    this.X = 0;  
    this.Y = 0;  
    
	this.frames = 2;  
	this.actualFrame = 0;  
	this.interval = 0; 
	
	this.action=0;     
    
      
    this.setPosition = function(x, y){  
		this.X = x;  
		this.Y = y;  
	}
	 
	this.moveLeft = function(){  
		this.X=this.X-5;
		this.action=1;
		this.image.src = "images/sprite2.png"; 
	}  
  
	this.moveRight = function(){  
		this.X=this.X+5;
		this.action=1;
		this.image.src = "images/sprite1.png"; 
	}
	
	this.murro = function(a){
		this.action=a;
	}
	
	this.stop = function(){
		this.action=0;
	}
	
	
	this.draw = function(){  
        try {
            context.drawImage(this.image,0+(this.actualFrame*56),this.action*80,56,90,this.X,(height-this.Y)-82,56,90);    
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
