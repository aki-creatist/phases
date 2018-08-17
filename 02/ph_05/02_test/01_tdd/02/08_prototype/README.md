# プロトタイプ継承

## プロトタイププロパテイを直接取得する

* `__proto__`プロパテイを使用する

```bash
touch spec/ObjectSpec.js
```

```javascript
it('test inheritance via proprietary __proto__', function () {
    var circle = { /* ... */ };
    var sphere = {};
    sphere.__proto__ = circle;
    expect(circle.isPrototypeOf(sphere)).toBeTruthy();
});
```

## 新規作成オブジェクトにプロパテイを追加

```javascript
it('test Object.create with properties', function () { //プロパティとともにオブジェクトを作る
    var circle = { /* ... */ };
    var sphere = Object.create(circle, {
        radius: {
            value: 3,
            writable: false,
            configurable: false,
            enumerable: true
        }
    });
    expect(sphere.radius).toBe(3);
});
```

### Object.create

```bash
touch src/Object.js
```

* `Object.create`は`Object.defineProperties`を使ってプロパティを設定する
    * このメソッドはさらに`0bjectdefineProperty`を使う

```javascript
if (!Object.create && Object.defineProperties) { //Object.createの実装例
    Object.create = function (object, properties) {
        function F() {}
        F.prototype = object;
        var obj = new F();

        if (typeof properties != "undefined") {
            Object.defineProperties(obj, properties);
        }

        return obj;
    };
}
```

### ネイティブのObject.createの使用の副作用

* 新オブジェクトを作成するためにプロキシコンストラクタ関数を使わない
    * instanceof演算子は意味のある情報を返さなくなる
* 新しく作成されたオブジェクトは、0bjectのインスタンスだとされてしまう
* オブジェクトの関係を知るためには、`0bject.isPrototypeOf`が役に立つ
* JSのようなダックタイピングの言語では、オブジェクトの継承関係よりもオブジェクトの機能のほうが重要
