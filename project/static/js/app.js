onload=function(){

	var renderer = PIXI.autoDetectRenderer(1000,500, {transparent: false, resolution: 0.6, antialias:false});

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
					var graphics=new PIXI.Sprite(PIXI.loader.resources["static/images/snow_flake_01.png"].texture);
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
					var graphics=new PIXI.Sprite(PIXI.loader.resources["static/images/rain_drop_02.png"].texture);
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

	loadBitmaps();

	function loadBitmaps(){
		PIXI.loader
		.add("static/images/hill_01.png")
		.add("static/images/hill_02.png")
		.add("static/images/mountain_01.png")
		.add("static/images/sky_01.png")
		.add("static/images/snow_flake_01.png")
		.add("static/images/rain_drop_02.png")
		.load(setup);
	}

	function setup(){
		var color_red = 0xe74c3c;
		var color_white = 0xffffff;

		var hill01=new PIXI.Sprite(PIXI.loader.resources["static/images/hill_01.png"].texture);
		var hill02=new PIXI.Sprite(PIXI.loader.resources["static/images/hill_02.png"].texture);
		var mountain01=new PIXI.Sprite(PIXI.loader.resources["static/images/mountain_01.png"].texture);
		var sky01=new PIXI.Sprite(PIXI.loader.resources["static/images/sky_01.png"].texture);
		sky01.alpha = 1;
		// sky01.tint = 0x555555;
		stage.addChild(sky01);
		stage.addChild(mountain01);
		stage.addChild(hill02);
		// var emitter=new SnowEmitter(150, color_white);
		// var emitter=new RainEmitter(150);
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




	// $(function(){
	// var $searchField = $("#inputCity");
	// var cityList = [];

	// $("#searchForm").on("submit", function(e){
	// 	e.preventDefault();
	// 	var searchText = $searchField.val();

	// 	$.getJSON("http://api.openweathermap.org/data/2.5/weather?q="+searchText+"&APPID=").then(function(response){
	// 		$searchField.val("");
	// 		parseWeatherData(response);
	// 	}).catch(function(error){
	// 		console.log("error while trying to fetch data");
	// 	});
	// });
	

	// function parseWeatherData(response){
	// 	cityList.unshift(response);
	// 	console.log(response);

	// 	$firstElement = $("#weatherList").first();
	// 	console.log($firstElement);
	// 	var tempInF = Math.round((cityList[0].main.temp * (9/5))-459.67) + "℉";
	// 	var conditions = cityList[0].weather[0].description;


	// 	var $divRow = $("<div>", {
	// 		class: "row boxBorder"
	// 	});
	// 	var $cityCol = $("<div>", {
	// 		class: "cityBox col-xs-7",
	// 		text: cityList[0].name
	// 	});
	// 	var $tempCol = $("<div>", {
	// 		class: "tempBox col-xs-5 pull-right",
	// 		text: tempInF
	// 	});
	// 	var $conditionCol = $("<div>", {
	// 		class: "conditionBox col-xs-5 pull-right",
	// 		text: conditions
	// 	});

	// 	$("#weatherList").prepend($($divRow)
	// 					 .append($($cityCol))
	// 					 .append($($tempCol))
	// 					 .append($($conditionCol)));

	// }

	// });

};







