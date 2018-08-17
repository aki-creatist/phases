var gulp = require('gulp');
var wrench = require('wrench');
var gutil = require('gulp-util');

var options = {
    src: 'src',
    tmp: '.tmp',
    errorHandler: function () {
        return function (err) {
            gutil.log(gutil.colors.red('[' + title + ']'), err.toString());
            this.emit('end');
        };
    }
};

wrench.readdirSyncRecursive('./gulp').filter(function(file) {
    return (/\.(js|coffee)$/i).test(file);
}).map(function(file) {
    require('./gulp/' + file)(options);
});

gulp.task('default', ['clean'], function () {
    gulp.start('build');
});