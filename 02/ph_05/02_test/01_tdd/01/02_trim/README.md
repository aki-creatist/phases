# Trim Test

## 概要

```text
├── libs
│   └── Trim.js
├── package.json
└── spec
    └── TrimSpec.js
```

## オブジェクトの呼び出しテスト

## テスト作成

```bash
touch spec/TrimSpec.js
```

```javascript
var Trim = require('../src/Trim');

describe('String trim test', function() {
    it('test trim should remove leading white-space', function() {
        expect(Trim(' a string')).toBe(' a string'.trim());
    });
    it('shoud remove trailing white-space', function () {
        expect(Trim('a string ')).toBe('a string'.trim());
    });
});
```

## 実装

```bash
touch src/Trim.js
```

```javascript
String.prototype.Trim = function () {
    return this.replace(/^\s+|\s+$/, "");
};
var Trim = function (str) {
    return str.trim();
};
module.exports = Trim;
```