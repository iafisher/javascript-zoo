'use strict';

const gulp = require('gulp');
const babel = require('gulp-babel');
const uglify = require('gulp-uglify');
var sass = require('gulp-sass');
const pipeline = require('readable-stream').pipeline;
const { watch } = require('gulp');
const watcher = watch(['./src/scripts/*.js']);

gulp.task('watchdev', function () {
    watcher.on('change', watchdev);
});

gulp.task('compress', compressJS);

function compressJS() {
    return pipeline(
        gulp.src('./src/scripts/*.js'),
        babel({ presets: ['@babel/env'] }),
        uglify(),
        gulp.dest('../backend/ui/static/ui/vanilla/js')
    );
}

function watchdev() {
    return pipeline(
        gulp.src('./src/scripts/*.js'),
        gulp.dest('../backend/ui/static/ui/vanilla/js')
    );
}

sass.compiler = require('node-sass');

gulp.task('sass', function () {
    return pipeline(
        gulp.src('./src/style/*.scss'),
        sass().on('error', sass.logError),
        gulp.dest('../backend/ui/static/ui/vanilla/css')
    )
});

gulp.task('sass:watch', function () {
    gulp.watch('./sass/**/*.scss', ['sass']);
});