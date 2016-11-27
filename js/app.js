var renderer = PIXI.autoDetectRenderer(500,800, {transparent: false, resolution: 0.5, antialias:false});


document.body.appendChild(renderer.view);

renderer.view.style.position = "absolute";
renderer.view.style.display = "block";
renderer.backgroundColor = 0x000000;
renderer.autoResize = true;
// PIXI.SCALE_MODES.DEFAULT = PIXI.SCALE_MODES.NEAREST;


var stage = new PIXI.Container();


renderer.resize(500, 800);
stage.scale.set(0.5,0.5);

class SnowEmitter {
	constructor(amount, color){
		this.amount=amount;
		var emitter = new PIXI.particles.ParticleContainer(300, {
		    scale: true,
		    position: true,
		    rotation: true,
		    uvs: true,
		    alpha: true
		});
		var that=this;
		var count=0;
		var timer = setInterval(function() {
			if(count<amount){
				var graphics=new PIXI.Sprite(PIXI.loader.resources["images/snow_flake_01.png"].texture);
				graphics.position.x = that.getRandomInt(0,1000);
				graphics.position.y = -10;
				graphics.scale.set(Math.random()+0.5);
				var tween = TweenMax.to(graphics.position, that.getRandomInt(9,12), {y:700, repeat:-1, repeatDelay:0.5, ease:Linear.easeNone, onRepeat:that.randomX});
				var randomWave = "+="+(that.getRandomInt(10,15)).toString();
				var tween2 = TweenMax.to(graphics.position, that.getRandomInt(2,3), {x:randomWave, repeat:-1, repeatDelay:0.1, yoyo:true, ease:Linear.easeNone});
				emitter.addChild(graphics);
				count++;
			} else {
				clearInterval(timer);
			}
		}, 100);

		stage.addChild(emitter);

	}

	start(){

	}

	randomX(){

	}

	getRandomInt(min, max) {
		min = Math.ceil(min);
		max = Math.floor(max);
		return Math.floor(Math.random() * (max - min + 1)) + min;
	}
}


class RainEmitter {
	constructor(amount){
		this.amount=amount;
		var emitter = new PIXI.particles.ParticleContainer(300, {
		    scale: true,
		    position: true,
		    rotation: true,
		    uvs: true,
		    alpha: true
		});
		var that=this;
		var count=0;
		var timer = setInterval(function() {
			if(count<amount){
				var graphics=new PIXI.Sprite(PIXI.loader.resources["images/rain_drop_01.png"].texture);
				graphics.position.x = that.getRandomInt(0,1000);
				graphics.position.y = -10;
				graphics.scale.set(that.getRandomFloat(0.5, 1));
				var tween = TweenMax.to(graphics.position, that.getRandomFloat(0.5, 1), {y:700, repeat:-1, repeatDelay:0.5, ease:Linear.easeNone});
				emitter.addChild(graphics);
				count++;
			} else {
				clearInterval(timer);
			}
		}, 100);

		stage.addChild(emitter);

	}

	getRandomFloat(min, max) {
		return Math.random() * (max - min) + min;
	}

	getRandomInt(min, max) {
		min = Math.ceil(min);
		max = Math.floor(max);
		return Math.floor(Math.random() * (max - min + 1)) + min;
	}
}

loadBitmaps();

function loadBitmaps(){
	PIXI.loader
	.add("images/hill_01.png")
	.add("images/hill_02.png")
	.add("images/mountain_01.png")
	.add("images/sky_01.png")
	.add("images/snow_flake_01.png")
	.add("images/rain_drop_01.png")
	.load(setup);
}

function setup(){
	var color_red = 0xe74c3c;
	var color_white = 0xffffff;

	var hill01=new PIXI.Sprite(PIXI.loader.resources["images/hill_01.png"].texture);
	var hill02=new PIXI.Sprite(PIXI.loader.resources["images/hill_02.png"].texture);
	var mountain01=new PIXI.Sprite(PIXI.loader.resources["images/mountain_01.png"].texture);
	var sky01=new PIXI.Sprite(PIXI.loader.resources["images/sky_01.png"].texture);
	stage.addChild(sky01);
	stage.addChild(mountain01);
	stage.addChild(hill02);
	// var emitter=new SnowEmitter(150, color_white);
	var emitter=new RainEmitter(150);
	stage.addChild(hill01);
	
	animationLoop();
}


animationLoop();

function animationLoop(){
	//Loop this function 60 times per second
	requestAnimationFrame(animationLoop);

	//Render the stage
	renderer.render(stage);
}
