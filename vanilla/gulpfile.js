// This file moves our compiled JS and CSS assets to the backend where they
// can be served by Express.

'use strict';

const gulp = require('gulp');
const babel = require('gulp-babel');
const uglify = require('gulp-uglify');
var sass = require('gulp-sass');
const pipeline = require('readable-stream').pipeline;
const { watch } = require('gulp');
const watcher = watch(['./src/scripts/*.js']);
sass.compiler = require('node-sass');


gulp.task('watchdev', function () {
    watcher.on('change', watchdev);
});

gulp.task('scripts', buildJS);

function buildJS() {
    return pipeline(
        gulp.src('./src/scripts/*.js'),
        gulp.dest('../backend/public/js')
    );
}

function watchdev() {
    return pipeline(
        gulp.src('./src/scripts/*.js'),
        gulp.dest('../backend/public/js')
    );
}

gulp.task('styles', function () {
    return pipeline(
        gulp.src('./src/style/*.scss'),
        sass().on('error', sass.logError),
        gulp.dest('../backend/public/css')
    )
});

gulp.task('sass:watch', function () {
    gulp.watch('./sass/**/*.scss', ['sass']);
});

gulp.task('build', function () {
    gulp.task('styles', 'scripts')
})
