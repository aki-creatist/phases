# gulp

## install

```bash
npm install --save-dev gulp@3.8.11 gulp-util@3.0.8
```

```bash
touch gulpfile.js
```

```javascript
var gulp = require('gulp');

gulp.task('default', function() {
    console.log('Hello World.');
});
```

## 動作確認

```bash
./node_modules/.bin/gulp
```

```text
Hello World.
```
