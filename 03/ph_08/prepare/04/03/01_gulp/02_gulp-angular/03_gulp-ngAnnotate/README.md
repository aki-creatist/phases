# gulp-ng-annotate

## AngularJSのDI

* コントローラーに必要なオブジェクトを注入する機能
    * 定義しておいた変数にセットしてくれる

## minifyとAnnotate

* minifyにより引数の変数が短縮される
* Angularは何を注入すべきかわからなくなる
* この問題に対処するため、annotation機能が用意されている
    * 文字列として注入すべきオブジェクトの名称を渡す機能
* ng-annotateはannotationを自動生成する

## ng-annotate

```bash
npm install --save-dev ng-annotate@1.2.2
```

```bash
touch test.js
```

```javascript
angular
  .module('ngAnnotationTestApp', ['ngRoute'])
  .service('HogeService', function($scope){
    //...
    console.log($scope);
  });
```

## 動作確認

```bash
./node_modules/.bin/ng-annotate -a in.js
#出力する場合
./node_modules/.bin/ng-annotate -a in.js > out.js
diff in.js out.js
```

```text
3c3
<     .service('HogeService', function($scope){
---
>     .service('HogeService', ["$scope", function($scope){
6c6
<     });
---
>     }]);
```

## gulp-ng-annotate

```bash
npm install --save-dev gulp-ng-annotate@0.5.3
```

```bash
touch gulpfile.js
```

```javascript
var gulp = require('gulp');
var $ = require('gulp-load-plugins')();

gulp.task('html', function () {
    return gulp.src('./in.js')
        .pipe($.ngAnnotate())
        .pipe(gulp.dest('dist'));
});
```

## 動作確認

* 前回の動作確認ファイルと同様の動作であることを確認

```bash
diff out.js dist/in.js
```

```text
4c4
<
---
>
```