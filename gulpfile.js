var gulp = require("gulp");
var sass = require("gulp-sass");

gulp.task("sass", function() {
	return gulp.src("./project/static/sass/*.scss")
	.pipe(sass())
	.pipe(gulp.dest("./project/static/css"));
});


gulp.task("watch", function(){
	gulp.watch("./project/static/sass/*.scss",['sass'])
})

gulp.task("default", ["sass", "watch"]);

