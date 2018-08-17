# gulp-angular

```bash
npm install --save-dev bower@1.8.4
./node_modules/.bin/bower --allow-root install
```

```bash
mkdir -p src/app/main
touch src/app/main/main.controller.js
```

```javascript
// コントローラとして呼び出されるメソッドの定義
function HelloController($scope) {
    $scope.greeting = { text : "hello world" };
}
// 'app'モジュールにHelloControllerコントローラの登録
angular.module('app', [])
    .controller('HelloController', HelloController);
```

```bash
touch src/app/main/main.html
```

```html
<!DOCTYPE html>
<html ng-app="app">
<head>
    <meta charset="UTF-8">
    <title>hello world</title>
    <script src="../../bower_components/angular/angular.js"></script>
    <script src="main.controller.js"></script>
</head>
<body>
<div ng-controller="HelloController">
    <input type="text" ng-model="greeting.text" value="{{greeting.text}}">
    <p>{{greeting.text}}</p>
</div>
</body>
</html>
```

## コントローラを修正

```javascript
angular.module('app', [])
    .controller('HelloController', function ($scope) {
        console.log('test');
        $scope.greeting = { text : "hello world" };
    });
```

# angular-app

## 設定ファイルの作成

```bash
mkdir config

cat << EOD > config/EnvConfig_dev.json
{
  "APP_CONF": {
    "URL": "./constants.json"
  }
}
EOD

cat << EOD > config/EnvConfig_stg.json
{
  "APP_CONF": {
    "URL": "http://xxx.com"
  }
}
EOD

cat << EOD > config/EnvConfig_prd.json
{
  "APP_CONF": {
    "URL": "http://xxx.com"
  }
}
EOD
```

## ngConfig

```bash
npm install --save-dev gulp-ng-config@1.5.0
```

```bash
mkdir gulp
touch gulp/scripts.js
```

```javascript
var gulp = require('gulp');
var $ = require('gulp-load-plugins')();

var profile = process.env.NODE_ENV || 'dev';

module.exports = function (options) {
    gulp.task('ngconfig', function () {
        return gulp.src('config/EnvConfig_' + profile + '.json')
            .pipe($.ngConfig('MyApp', { createModule: false }))
            .pipe($.rename('constants.js'))
            .pipe(gulp.dest(options.src + '/app'));
    });
};
```

```bash
./node_modules/.bin/gulp ngconfig
NODE_ENV=stg ./node_modules/.bin/gulp ngconfig
```

## HTMLにタグを埋め込む

### inject

```bash
npm install --save-dev gulp-inject@1.1.1 gulp-angular-filesort@1.0.4
```

```javascript
var gulp = require('gulp');

var $ = require('gulp-load-plugins')();

module.exports = function (options) {
    gulp.task('inject', function () {
        var injenctScripts = gulp.src([
            options.src + '/app/**/*.js',
            options.src + '/app/**/**/*.js',
            '!' + options.src + '/app/**/*.spec.js',
            '!' + options.src + '/app/**/**/*.mock.js'
        ])
            .pipe($.angularFilesort());
        var injectOptions = {
            ignorePath: [options.src, options.tmp + '/serve'],
            addRootSlash: false
        };
        return gulp.src(options.src + '/*.html')
            .pipe($.inject(injenctScripts, injectOptions))
            .pipe(gulp.dest(options.tmp + '/serve'));
    });
};
```

```bash
./node_modules/.bin/gulp inject
```

### wiredep

```bash
npm install --save-dev wiredep@2.2.2
vim gulpfile.js
```

```diff
  var options = {
      src: 'src',
      tmp: '.tmp',
+     wiredep: {
+         directory: 'bower_components',
+         exclude: [/jquery/]
+     }
  };
```

```bash
vim gulp/inject.js
```

```diff
+ var wiredep = require('wiredep').stream;

  return gulp.src(options.src + '/*.html')
      .pipe($.inject(injenctScripts, injectOptions))
+     .pipe(wiredep(options.wiredep))
      .pipe(gulp.dest(options.tmp + '/serve'));
```

```bash
./node_modules/.bin/gulp inject
```

## HTMLを圧縮




## 定数を使う

```bash
mkdir src/app/services/
touch src/app/services/message.js
```