# グローバルオブジェクト

* JSエンジンは、コードの実行前にグローバルオブジェクトを作成する
    * グローバルオブジェクト: 組み込みオブジェクト
        * 組み込みオブジェクト: Object、String、Arrayなど
            * 初期プロパティがECMAScriptで定義されている
* JSのブラウザ実装は、グローバルオブジェクトのプロパティ
    * それ自体もグローバルオブジェクトであるwindowを提供している

```javascript
// Native Object
console.log(Object()); // {}
console.log(String()); // 何も出力されないがエラーにはならない
console.log(Array());  // []
```

## グローバルオブジェクトへのアクセス

* グローバルオブジェクトはグローバルスコープではthisとしてもアクセス可能

```javascript
document.write(this);   // [object Window]
document.write(window); // [object Window]

if (this === window) {
    document.write(true); //trueが返る
}

//windowをthisに書き換えた
if (this.addEventListener) {
    this.addEventListener('load', alert("a"), false);
}
```

## ブラウザ内のwindowとグローバルオブジェクトの関係

```javascript
var global = this;

TestCase("GlobalObjectTest", {
    "test window should be global object": function () {
        assertSame(global, window);
        assertSame(global.window, window);
        assertSame(window.window, window);
    }
});
```

* グローバルスコープでは、グローバルオブジェクトは変数オブジェクトとして使われる
    * varで変数を宣言すると、グローバルオブジェクトに対応するプロパティが作られる
* 以下の2つの代入は、ほとんど同じ意味

```javascript
//グローバルオブジェクトのプロパティへの代入
var assert = function () { /* ... */ };
this.assert = function () { /* ... */ };
```

```javascript
var aa = "aa";
this.aa = "bb"; //値の書き換え

document.write(aa); //値が書きかわる
document.write(window.aa); //windowオブジェクトのプロパティとしてアクセス可能
```

## プロパティ代入の方法ではホイストされない

* 変数宣言はホイストされるが、プロパティ代入の方法ではホイストされない
* 文脈中で変数宣言のない変数を出力しようとするとエラーを吐く
* プロパティ代入を行っていないものは全てundefinedを吐く
* つまり、プロパティ代入のundefinedはホイストとは別の原理に基づいている

```javascript
document.write(aa);         //undeifined(ホイストされた)
document.write(window.bb);  //undefined(ホイストではない)
document.write(cc);         //Error(参照できるものがない)
document.write(window.dd);  //undefined(ホイストではない)
var aa = "aa";
this.bb = "bb";
```