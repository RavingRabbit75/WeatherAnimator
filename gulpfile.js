'use strict';

var gulp = require("gulp");
var sass = require("gulp-sass");
var cssbeautify = require("gulp-cssbeautify");

gulp.task("sass", function() {
	return gulp.src("./project/static/sass/*.scss")
	.pipe(sass())
	.pipe(cssbeautify())
	.pipe(gulp.dest("./project/static/css"));
});


gulp.task("watch", function(){
	gulp.watch("./project/static/sass/*.scss",['sass']);
});

gulp.task("default", ["sass", "watch"]);

