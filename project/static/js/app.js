onload=function(){

	var renderer = PIXI.autoDetectRenderer(1000,500, {transparent: false, resolution: 0.5, antialias:false});

	document.getElementById("canvasContainer").appendChild(renderer.view);

	renderer.view.style.position = "absolute";
	renderer.view.style.display = "block";
	renderer.backgroundColor = 0xAED200;
	renderer.autoResize = true;
	// PIXI.SCALE_MODES.DEFAULT = PIXI.SCALE_MODES.NEAREST;

	var stage = new PIXI.Container();
	renderer.resize(window.innerWidth, window.innerHeight);
	let scaleWidth = window.innerWidth/2000;
	let scaleHeight = window.innerHeight/1600;
	if (window.innerHeight>window.innerWidth){
		scaleWidth = scaleHeight;
	} 
	if (window.innerWidth>window.innerHeight){
		scaleHeight = scaleWidth;
	}
	stage.scale.set(scaleWidth, scaleHeight);
	window.addEventListener("resize", function(event){
		renderer.resize(window.innerWidth, window.innerHeight);
		let scaleWidth = window.innerWidth/2000;
		let scaleHeight = window.innerHeight/1600;
		if (window.innerHeight>window.innerWidth){
			scaleWidth = scaleHeight;
		} 
		if (window.innerWidth>window.innerHeight){
			scaleHeight = scaleWidth;
		}
		stage.scale.set(scaleWidth, scaleHeight);
	});

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

			var count=0;
			var timer = setInterval(function() {
				if(count<amount){
					var graphics=new PIXI.Sprite.fromImage("/static/images/snow_flake_01.png");
					graphics.position.x = this.getRandomInt(0,2000);
					graphics.position.y = -10;
					graphics.scale.set(Math.random()+0.5);
					var tween = TweenMax.to(graphics.position, this.getRandomInt(5,8), {y:700, repeat:-1, repeatDelay:0.5, ease:Linear.easeNone, onRepeat:this.randomX});
					var randomWave = "+="+(this.getRandomInt(10,25)).toString();
					var tween2 = TweenMax.to(graphics.position, this.getRandomInt(1,3), {x:randomWave, repeat:-1, repeatDelay:0.1, yoyo:true, ease:Linear.easeNone});
					emitter.addChild(graphics);
					count++;
				} else {
					clearInterval(timer);
				}
			}.bind(this), 100);

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
			var emitter = new PIXI.particles.ParticleContainer(1000, {
			    scale: true,
			    position: true,
			    rotation: true,
			    uvs: true,
			    alpha: true
			});

			var count=0;
			var timer = setInterval(function() {
				if(count<amount){
					var graphics=new PIXI.Sprite.fromImage("/static/images/rain_drop_02.png");
					graphics.position.x = this.getRandomInt(0,2000);
					graphics.position.y = -10;
					graphics.scale.set(this.getRandomFloat(0.5, 1));
					var tween = TweenMax.to(graphics.position, this.getRandomFloat(0.5, 1), {y:700, repeat:-1, repeatDelay:0.5, ease:Linear.easeNone});
					emitter.addChild(graphics);
					count++;
				} else {
					clearInterval(timer);
				}
			}.bind(this), 10);

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


	var imgsNightPaths={
		hill1: "/static/images/night/hill_01.png",
		hill2: "/static/images/night/hill_02.png",
		mountain: "/static/images/night/mountain_01.png",
		sky: "/static/images/night/sky_01.png"
	};

	var imgsDayPaths={
		hill1: "/static/images/day/hill_01.png",
		hill2: "/static/images/day/hill_02.png",
		mountain: "/static/images/day/mountain_01.png",
		sky: "/static/images/day/sky_01.png"
	};

	if (typeof wdata!=="undefined"){
		if (wdata==="night"){
			setup("night", imgsNightPaths);
		} else {
			setup("day", imgsDayPaths);
		}
	} else {
		setup("day", imgsDayPaths);
	}
	

	function setup(time, paths){
		var body=document.getElementsByTagName("body")[0];
		if(time==="night"){
			body.style.backgroundColor="#2A2F4D";
			renderer.backgroundColor = 0x2A2F4D;
		} else {
			body.style.backgroundColor="#AED200";
			renderer.backgroundColor = 0xAED200;
		}
	
		var hill01=new PIXI.Sprite.fromImage(paths.hill1);
		var hill02=new PIXI.Sprite.fromImage(paths.hill2);
		var mountain01=new PIXI.Sprite.fromImage(paths.mountain);
		var sky01=new PIXI.Sprite.fromImage(paths.sky);
		stage.addChild(sky01);
		stage.addChild(mountain01);
		stage.addChild(hill02);

		var precipitation;
		if (typeof w_code!=="undefined"){
			w_codeInt=parseInt(w_code);

			if (w_codeInt>=500 && w_codeInt<600) {
				switch(w_codeInt) {
					case 500:
						precipitation = new RainEmitter(100);
						break;
					case 501:
						precipitation = new RainEmitter(400);
						break;
					case 502:
						precipitation = new RainEmitter(600);
						break;
					case 503:
						precipitation = new RainEmitter(800);
						break;
					case 504:
						precipitation = new RainEmitter(1000);
						break;
					default:

				}
			}

			if (w_codeInt>=600 && w_codeInt<700) {
				switch(w_codeInt) {
					case 600:
						precipitation = new SnowEmitter(100);
						break;
					case 601:
						precipitation = new SnowEmitter(400);
						break;
					case 602:
						precipitation = new SnowEmitter(600);
						break;
					default:

				}
			}
		}
		
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


};







