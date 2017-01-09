onload=function(){

	var renderer = PIXI.autoDetectRenderer(1000,400, {transparent: false, resolution: 1.0, antialias:false});

	document.getElementById("canvasContainer").appendChild(renderer.view);

	renderer.view.style.position = "absolute";
	renderer.view.style.display = "block";
	renderer.backgroundColor = 0xAED200;
	renderer.autoResize = true;
	// PIXI.SCALE_MODES.DEFAULT = PIXI.SCALE_MODES.NEAREST;

	var stage = new PIXI.Container();
	renderer.resize(window.innerWidth, window.innerHeight);
	var scaleWidth = window.innerWidth/1000;
	var scaleHeight = window.innerHeight/400;
	if (window.innerWidth>1000){
			scaleHeight = scaleWidth;
	} 
	if (window.innerWidth<=1000){
		scaleHeight = 1.2;
		scaleWidth = 1.2;
	} 
	stage.scale.set(scaleWidth, scaleHeight);
	window.addEventListener("resize", function(event){
		renderer.resize(window.innerWidth, window.innerHeight);
		var scaleWidth = window.innerWidth/1000;
		var scaleHeight = window.innerHeight/400;
		if (window.innerWidth>1000){
			scaleHeight = scaleWidth;
		} 
		if (window.innerWidth<=1000){
			scaleHeight = 1.2;
			scaleWidth = 1.2;
		} 
		
		stage.scale.set(scaleWidth, scaleHeight);
	});



	function getRandomFloat(min, max) {
		return Math.random() * (max - min) + min;
	}

	function getRandomInt(min, max) {
		min = Math.ceil(min);
		max = Math.floor(max);
		return Math.floor(Math.random() * (max - min + 1)) + min;
	}

	class SnowEmitter {
		constructor(amount, color){
			this.amount=amount;
			var emitter = new PIXI.particles.ParticleContainer(600, {
			    scale: true,
			    position: true,
			    rotation: true,
			    uvs: true,
			    alpha: true
			});

			var count=0;
			var timer = setInterval(function() {
				if(count<amount){
					var graphics=new PIXI.Sprite.fromImage("/static/images/elements/snow_flake_01.png");
					graphics.position.x = getRandomInt(0,1000);
					graphics.position.y = -10;
					graphics.scale.set(Math.random()*(0.7-0.1)+0.1);
					var tween = TweenMax.to(graphics.position, getRandomInt(5,8), {y:350, repeat:-1, repeatDelay:0.5, ease:Linear.easeNone, onRepeat:this.randomX});
					var randomWave = "+="+(getRandomInt(10,25)).toString();
					var tween2 = TweenMax.to(graphics.position, getRandomInt(1,3), {x:randomWave, repeat:-1, repeatDelay:0.1, yoyo:true, ease:Linear.easeNone});
					emitter.addChild(graphics);
					count++;
				} else {
					clearInterval(timer);
				}
			}.bind(this), 50);

			stage.addChild(emitter);

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
					var graphics=new PIXI.Sprite.fromImage("/static/images/elements/rain_drop_02.png");
					graphics.position.x = getRandomInt(0,1000);
					graphics.position.y = -10;
					graphics.scale.set(getRandomFloat(0.2, 0.7));
					var tween = TweenMax.to(graphics.position, getRandomFloat(0.5, 1), {y:350, repeat:-1, repeatDelay:0.5, ease:Linear.easeNone});
					emitter.addChild(graphics);
					count++;
				} else {
					clearInterval(timer);
				}
			}.bind(this), 10);

			stage.addChild(emitter);
		}

	}

	class LightningEmitter {
		constructor(timeOfDay){
			var emitter = new PIXI.Container()
			var bolt1=new PIXI.Sprite.fromImage("/static/images/elements/lightning_01.png");
			var bolt2=new PIXI.Sprite.fromImage("/static/images/elements/lightning_02.png");
			if(timeOfDay==="night"){
				bolt1.tint=0xDEDEFF;
			}
			bolt1.alpha=0;
			bolt2.alpha=0;
			emitter.addChild(bolt1);
			emitter.addChild(bolt2);
			var currentBolt = bolt1;
			var timer = setInterval(function() {
				currentBolt.position.x = getRandomInt(0,1000);
				currentBolt.position.y = 0;
				currentBolt.scale.set(getRandomFloat(0.8, 1.0));
				if(getRandomInt(0,1)===0){
					currentBolt.width=currentBolt.width*-1;
				}
				var tl = new TimelineMax({});
				tl.add( TweenLite.to(currentBolt, 0.05, {alpha:1}) );
				tl.add( TweenLite.to(currentBolt, 0.05, {alpha:0}) );
				tl.add( TweenLite.to(currentBolt, 0.05, {alpha:1}) );
				tl.add( TweenLite.to(currentBolt, 0.2, {alpha:0}) );
				tl.play();
				if (currentBolt===bolt1){
					currentBolt=bolt2;
				} else {
					currentBolt=bolt1;
				}
				
			}.bind(this), getRandomInt(3000,5000));

			stage.addChild(emitter);
		}

	}


	class CloudEmitter {
		constructor(timeOfDay, windSpeed, amount){
			var emitter = new PIXI.Container();
			var cloud1=new PIXI.Sprite.fromImage("/static/images/elements/clouds_01.png");
			var cloud2=new PIXI.Sprite.fromImage("/static/images/elements/clouds_02.png");
			var cloud3=new PIXI.Sprite.fromImage("/static/images/elements/clouds_03.png");
			if(timeOfDay==="night"){
				cloud1.tint=0x7676A1;
				cloud2.tint=0x7676A1;
				cloud3.tint=0x7676A1;
			}

			cloud1.position.y = getRandomInt(10,20);
			cloud3.position.y = getRandomInt(30,50);
			cloud2.position.y = getRandomInt(90,100);
			cloud1.position.x = 1010;
			cloud2.position.x = 1010;
			cloud3.position.x = 1010;
			var time1 = getRandomInt(300,320)/windSpeed;
			var time2 = getRandomInt(300,320)/windSpeed;
			var time3 = getRandomInt(300,320)/windSpeed;
			console.log(time1);
			var tl1 = new TimelineMax({});
				var offset1="+="+Math.floor(time3*0.3);
				tl1.add("start", offset1);
				tl1.add( TweenMax.to(cloud1.position, time1, {x:"-=1200", repeat:-1, repeatDelay:1.0, ease:Linear.easeNone}) );
			var tl2 = new TimelineMax({});
				var offset2="+="+Math.floor(time3*0.1);
				tl2.add("start", offset2);
				tl2.add( TweenMax.to(cloud2.position, time2, {x:"-=1200", repeat:-1, repeatDelay:1.0, ease:Linear.easeNone}) );
			var tl3 = new TimelineMax({});
				var offset3="+="+Math.floor(time3*0.7);
				tl3.add("start", offset3);
				tl3.add( TweenMax.to(cloud3.position, time3, {x:"-=1200", repeat:-1, repeatDelay:1.0, ease:Linear.easeNone}) );
			tl1.play("start");
			tl2.play("start");
			tl3.play("start");
			emitter.addChild(cloud1);
			emitter.addChild(cloud2);
			emitter.addChild(cloud3);
			stage.addChild(emitter);
		}
		
	}


	var imgsNightPaths={
		hill1: "/static/images/night/hill_01.png",
		hill2: "/static/images/night/hill_02.png",
		mountain: "/static/images/night/mountain_01.png",
		sky: "/static/images/night/sky_01.png",
		trees: "/static/images/night/trees_01.png"
	};

	var imgsDayPaths={
		hill1: "/static/images/day/hill_01.png",
		hill2: "/static/images/day/hill_02.png",
		mountain: "/static/images/day/mountain_01.png",
		sky: "/static/images/day/sky_01.png",
		trees: "/static/images/day/trees_01.png"
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
		var trees01=new PIXI.Sprite.fromImage(paths.trees);
		stage.addChild(sky01);
		stage.addChild(mountain01);
		stage.addChild(hill02);
		stage.addChild(trees01);

		var precipitation;
		var clouds;
		
		if (typeof w_code!=="undefined"){
			w_codeInt=parseInt(w_code);

			// Thunderstorm
			if (w_codeInt>=200 && w_codeInt<300) {
				if(time==="night"){
					var lightningShow = new LightningEmitter("night");
				} else {
					var lightningShow = new LightningEmitter("day");
				}
				
				switch(w_codeInt) {
					case 200:
						precipitation = new RainEmitter(100);
						
						break;
					case 201:
						precipitation = new RainEmitter(400);
						break;
					case 202:
						precipitation = new RainEmitter(600);
						break;
					case 210:
						precipitation = new RainEmitter(100);
						break;
					case 211:
						precipitation = new RainEmitter(400);
						break;
					case 212:
						precipitation = new RainEmitter(600);
						break;
					case 230:
						precipitation = new RainEmitter(80);
						break;
					case 231:
						precipitation = new RainEmitter(50);
						break;
					case 232:
						precipitation = new RainEmitter(80);
						break;
					default:
						precipitation = new RainEmitter(80);
				}
			}

			// Drizzle
			if (w_codeInt>=300 && w_codeInt<400) {
				switch(w_codeInt) {
					case 300:
						precipitation = new RainEmitter(20);
						break;
					case 301:
						precipitation = new RainEmitter(50);
						break;
					case 302:
						precipitation = new RainEmitter(80);
						break;
					case 310:
						precipitation = new RainEmitter(20);
						break;
					case 311:
						precipitation = new RainEmitter(50);
						break;
					case 312:
						precipitation = new RainEmitter(80);
						break;
					default:
						precipitation = new RainEmitter(80);
				}
			}


			// Rain
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
						precipitation = new RainEmitter(100);

				}
			}

			// Snow
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
					case 620:
						precipitation = new SnowEmitter(100);
						break;
					case 621:
						precipitation = new SnowEmitter(400);
						break;
					case 622:
						precipitation = new SnowEmitter(600);
						break;
					default:
						precipitation = new SnowEmitter(100);
				}
			}

			//Clouds
			if (w_codeInt>=800 && w_codeInt<900) {
				switch(w_codeInt) {
					case 801:
						clouds = new CloudEmitter(time, wind_speed, 100);
						break;
					case 802:
						clouds = new CloudEmitter(time, wind_speed, 400);
						break;
					case 803:
						clouds = new CloudEmitter(time, wind_speed, 600);
						break;
					case 804:
						clouds = new CloudEmitter(time, wind_speed, 100);
						break;
					default:
						clouds = new CloudEmitter(time, wind_speed, 100);
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







