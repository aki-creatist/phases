# JS Test

## 概要

```text
├── libs
│   └── Sum.js
├── package.json
└── spec
    └── SumSpec.js
```

## 足し算のテスト

### testの作成

```bash
touch spec/SumSpec.js
```

```javascript
const sum = require('../libs/sum');

it('adds 1 + 2 to equal 3', function () {
    expect(sum(1, 2)).toBe(3);
});
```

### ソース実装

```bash
touch libs/Sum.js
```

```javascript
function sum(a, b) {
    return a + b;
}
module.exports = sum;
```

### テストの実施

```bash
npm test
```

### 実施結果

```text
  Top level suite
    ✓ adds 1 + 2 to equal 3
```