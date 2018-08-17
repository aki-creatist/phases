# 外部ライブラリを利用したテスト

## 概要

* `strftime()`を利用する
    * 外部ライブラリをインストール

## 構成

```text
.
├── jasmine-runner.js
├── node_modules
├── package.json
├── spec
│   ├── StrftimeSpec.js
│   └── support
└── src
    └── Strftime.js
```

## 事前準備

* 利用するライブラリ
* https://github.com/samsonjs/strftime

```bash
npm install strftime
```

* ソースファイルを生成

```bash
touch src/Strftime.js
```

## ライブラリの読み込みテスト

### ソースの実装

* npm installしたstrftimeの動作確認

```bash
vim src/Strftime.js
```

```javascript
Date.prototype.strftime = require('strftime');

var date = new Date();
console.log(date.strftime("%Y"));
console.log(date.strftime("%m"));
console.log(date.strftime("%d"));
console.log(date.strftime("%y"));
console.log(date.strftime("%F"));
```

### 実施

* コンソールに現在の日時が表示されること

```bash
node src/Strftime.js
```

## オブジェクトの上書き

```bash
vim src/Strftime.js
```

```diff
- Date.prototype.strftime = require('strftime');
+ var strftime = require('strftime');
- var date = new Date();
- console.log(date.strftime("%Y"));
- console.log(date.strftime("%m"));
- console.log(date.strftime("%d"));
- console.log(date.strftime("%y"));
- console.log(date.strftime("%F"));
+ console.log(strftime);
+ Date.prototype.strftime = (function () {
+     strftime.formats = {
+         d: 'test'
+     };
+ }());
+ console.log(strftime);
```

### 実施

* オブジェクトにtestプロパティが追加されていること

```bash
node src/Strftime.js
```

### 結果

```text
{ [Function: _strftime] #メソッド通過前
  localize: [Function],
  localizeByIdentifier: [Function],
  timezone: [Function],
  utc: [Function] }
{ [Function: _strftime] #メソッド通過後
  localize: [Function],
  localizeByIdentifier: [Function],
  timezone: [Function],
  utc: [Function],
  formats: { d: 'test' } } #ここに追加される
```

## オブジェクトの追加

### ソースの修正

```bash
vim src/Strftime.js
```

```diff
- console.log(strftime);
  var date = new Date();
  strftime.formats = {
-     d: 'test'
+     d: function (date) {
+         return zeroPad(date.getDate());
+     }
  };
```

### 実施

* オブジェクトのdプロパティにオブジェクトが追加されていること

```bash
node src/Strftime.js
```

### 結果

```text
{ [Function: _strftime]
  localize: [Function],
  localizeByIdentifier: [Function],
  timezone: [Function],
  utc: [Function],
  formats: { d: [Function] } } #オブジェクトが追加された
```

## Testファイルの作成

```bash
vim spec/StrftimeSpec.js
```

```javascript
var strftime = require('../src/Strftime');
console.log(strftime.formats.d);
```

```bash
npm test
```

* 不合格
* ソースファイルで定義したプロパティが見つからない

```text
console.log(strftime.formats.d);
                            ^
TypeError: Cannot read property 'd' of undefined
```

## ソースファイルの修正

```bash
vim src/Strftime.js
```

```diff
+ module.exports = strftime;
```

```bash
npm test
```

```text
Executed 0 of 0 specs SUCCESS in 0.004 sec.
```

## Testの作成

```bash
vim spec/StrftimeSpec.js
```

```diff
  var strftime = require('../src/Strftime');
- console.log(strftime.formats.d);
+ describe('strftime test', function () {
+     it('npm installしたstrftimeが機能していること', function () {
+         expect(strftime('%F %T', new Date(1307472705067))).toBe('2011-06-08 03:51:45')
+     });
+ });
```

```bash
npm test
```

```text
  strftime test
    ✓ npm installしたstrftimeが機能していること
```

## Testの追加

```bash
vim spec/StrftimeSpec.js
```

```diff
+ var date = new Date(2018, 8, 23, 13, 39, 00);

  describe('strftime test', function () {
      it('npm installしたstrftimeが機能していること', function () {
          expect(strftime('%F %T', new Date(1307472705067))).toBe('2011-06-08 03:51:45')
      });
+     it('src/Strftimeが機能していて追加のプロパティが設定されていること', function () {
+         expect(strftime.formats.d(date)).toBe('23')
+     });
  });
```

```bash
npm test
```

* zeroPadが定義されていないため不合格

```text
  - ReferenceError: zeroPad is not defined
```

## ソース修正

```bash
vim src/Strftime.js
```

```diff
- console.log(strftime.formats.d);
+ function zeroPad(num) {
+     return (+num < 10 ? "0" : "") + num;
+ }
  module.exports = strftime;
```

```bash
npm test
```

```text
  strftime test
    ✓ src/Strftimeが機能していて追加のプロパティが設定されていること
    ✓ npm installしたstrftimeが機能していること
```

## Testの追加

```bash
vim spec/StrftimeSpec.js
```

```diff
+ it('1桁の月を渡したら先頭を0で埋めて返すこと', function () {
+     expect(strftime.formats.m(date)).toBe('08')
+ });
```

```bash
npm test
```

```text
 TypeError: undefined is not a function
```

## ソース修正

```bash
vim src/Strftime.js
```

```diff
+ m: function (date) {
+     return zeroPad(date.getMonth())
+ },
```

```bash
npm test
```

```text
  strftime test
    ✓ npm installしたstrftimeが機能していること
    ✓ src/Strftimeが機能していて追加のプロパティが設定されていること
    ✓ 1桁の月を渡したら先頭を0で埋めて返すこと
```

## 完成

```bash
cat src/Strftime.js
```

```javascript
var strftime = require('strftime');

var date = new Date(2018, 8, 23, 13, 39, 00);

Date.prototype.strftime = (function () {
    strftime.formats = {
        m: function (date) {
            return zeroPad(date.getMonth())
        },
        d: function (date) {
            return zeroPad(date.getDate());
        }
    };
}());

console.log(strftime.formats.d);

function zeroPad(num) {
    return (+num < 10 ? "0" : "") + num;
}

module.exports = strftime;
```

```bash
cat spec/StrftimeSpec.js
```

```javascript
var strftime = require('../src/Strftime');

var date = new Date(2018, 8, 23, 13, 39, 00);

describe('strftime test', function () {
    it('npm installしたstrftimeが機能していること', function () {
        expect(strftime('%F %T', new Date(1307472705067))).toBe('2011-06-08 03:51:45')
    });
    it('1桁の月を渡したら先頭を0で埋めて返すこと', function () {
        expect(strftime.formats.m(date)).toBe('08')
    });
    it('src/Strftimeが機能していて追加のプロパティが設定されていること', function () {
        expect(strftime.formats.d(date)).toBe('23')
    });
});
```