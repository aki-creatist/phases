# PhantomJS

## 前提条件

* PhantomJSがインストールされていること

## 動作確認

### HelloWorld

```bash
touch hello.js
```

```javascript
console.log('Hello, world!');
phantom.exit();
```

```bash
phantomjs hello.js
```

### キャプチャ

```bash
touch capture.js
```

```javascript
var page = require('webpage').create();
page.open('http://yahoo.co.jp', function(status) {
  console.log("Status: " + status);
  if(status === "success") {
    page.render('example.png');
  }
  phantom.exit();
});
```