# 属性の上書き可能なプロパティ属性

ユーザー定義のプロパティデスクリプタが、プロパティの次の属性を上書きすることを認めている

* enumerable
    * for-inループでプロパテイを反復処理できるかどうかを決める
* configurable
    * delete演算子でプロパティを削除できるかどうかを決める
* writable
    * プロパティを上書きできるかどうかを決める
* get
    * プロパティアクセスの戻り値を計算する関数
* set
    * プロパテイに代入を行うために、代入すべき値を引数として呼び出される関数
    
## プロパテイ設定可能方法
    
* `Object.defineProperty()`
    * オブジェクトの新しいプロパテイを定義する
    * プロパテイデスクリプタの更新もする
        * プロパテイデスクリプタの更新
            * プロパテイのconfigurable属性がtrueに設定されているときに限り実行可能

## 属性を更新する方法

### 前提条件

* ブラウザが以下をサポートしていること
    * `ObjectgetOwnPropertyDescriptor`
    * `Object.defineProperty`
* デスクリプタを使用した一部の属性だけを更新する方法

```javascript
//プロパティデスクリプタの変更
it('test changing a property descriptor', function () {
    var circle = { radius: 3 };
    var descriptor = Object.getOwnPropertyDescriptor(circle, "radius");
    descriptor.configurable = false;
    Object.defineProperty(circle, "radius", descriptor);
    delete circle.radius;
    // Non-configurable radius cannot be deleted
    expect(circle.radius).toBe(3);
});
```

### seal()

```bash
touch src/Object.js
```

```javascript
if (!Object.seal && Object.getOwnPropertyNames && //Object.sealの実装例
    Object.getOwnPropertyDescriptor &&
    Object.defineProperty && Object.preventExtensions) { //Object.preventExtensions(obj)を呼び出せば、オブジェクトはさらなる拡張を禁止できる
    //0bject.seal()を使えば、オブジェクト全体をシーリング（封印）できる
    Object.seal = function (object) {
        //Object.getOwnPropertyNamesは､enumerable属性がfalseになっているものも含め、オブジェクト自身のすべてのプロパテイを返す
        var properties = Object.getOwnPropertyNames(object);
        var desc, prop;

        for (var i = 0, l = properties.length; i < l; i++) {
            prop = properties[i];
            desc = Object.getOwnPropertyDescriptor(object, prop);

            if (desc.configurable) {
                desc.configurable = false;
                Object.defineProperty(object, prop, desc);
            }
        }

        Object.preventExtensions(object);

        return object;
    };
}
```
    
### その他

* `Object.isSealed`
    * オブジェクトがシーリングされているかどうかを調べられる
* `Object.freeze`
    * オブジェクト全体を手軽にイミュータブルにしたい場合に使用
    * 関連メソッドながらもっと制限の厳しい
    * freezeはsealと同様に動作する
    * さらにすべてのプロパティの`writable`属性を`false`にする
    * こうすると、オブジェクトは一切変更できなくなる
