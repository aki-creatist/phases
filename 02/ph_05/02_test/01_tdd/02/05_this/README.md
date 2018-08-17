# thisキーワード

## 概要

* thisの値は、呼び出し元によって決まる
    * 通常のオブジェクト指向言語では`this`はレシーバオブジェクトを指す
    * この点で、ほかの多くの言語の関数やメソッドとは異なる
* JS関数はオブジェクトであり、実行コンテキストやスコープチェーンが独特の意味を持つ
* また、呼び出し元でthisの値を操作可能
    * 関数の操作方法としては異色

```bash
touch spec/CircleSpec.js
```

```javascript
var circle = {
    radius: 6,
    diameter: function () {
        return this.radius * 2;
    }
};
//thisの値はcircleオブジェクトではない
describe('CircleTest', function () {
    it('test should implicitly bind to object', function () {
        expect(circle.diameter()).toBe(12);
    });
    it('test implicit binding to the global object', function () {
        var myDiameter = circle.diameter;
        radius = 2;
        expect(myDiameter()).toBe(4);
    });
});
```

## thisの値

* thisの値は、呼び出し元によって決まる
* 実行コンテキストに入ると、アクティベーションオブジェクトと変数オブジェクトが作られる
* スコープチェーンに追加されるだけでなく、thisの値も決まる

## thisの暗黙の設定

* thisは、かっこを使って関数を呼び出したときに暗黙のうちに設定される
* 関数をメソッドとして呼び出すとその呼び出しに使ったオブジェクトがthisになる
    * `関数をメソッドとして呼び出す`: 関数をオブジェクトのプロパティとして呼び出すこと

## thisの明示的な設定

* 関数のcallまたは`apply()`を使って明示的に設定する
    * 第１引数をthisとして関数を呼び出す
    * 第２引数以下は、関数を呼び出すときに渡される

```diff
//callの使い方
+ it('test should call radius on anonymous object', function () {
+     expect(circle.diameter.call({ radius: 5 })).toBe(10)
+ })
```

## thisとしてプリミティブを使う

### call()

* callの第１引数はどんなオブジェクトでもかまわない
    * nullでもよい
    * nullを渡すと、thisとしてグローバルオブジェクトが使われる
* 文字列や論理値などのプリミティブ型をthisとして渡すと、その値はオブジェクトでラップされる

```bash
touch spec/BooleanSpec.js
```

```javascript
Boolean.prototype.not = function () { //論理地をthisとしてメソッドを呼び出す
    return !this;
};

describe('BooleanTest', function () {
    it('test should flip value of true', function () {
        expect(true.not()).toBeFalsy();
        expect(Boolean.prototype.not.call(true)).toBeFalsy();
    });
});
```

### Booleanへの強制型変換

* プリミティブの論理値は、thisとして使われるとBooleanオブジェクトに変換される
* しかし、trueの単項論理not演算子を実行すると、falseになる
    * Booleanへの強制型変換を行うと、必ずtrueになってしまうため

```diff
+ it('test should flip value of false', function () {
+     expect(false.not()).toBeFalsy();
+     expect(Boolean.prototype.not.call(false)).toBeFalsy();
+ });
```

## apply()

* callとよく似ているが、２個の引数しか期待していないところが異なる
    * 第１引数: callのときと同じthisの値
    * 第２引数: 呼び出される関数に渡される実引数を配列にまとめたもの
        * 本物の配列オブジェクトでなくてもかまわない
* 例: applyを使えば、配列内のすべての数値の合計を計算できる
    * 以下の関数は、任意個の引数を受け付け、それらはすべて数値だという前提条件のもとで合計を返す
* 第１引数としてnullを使うと、thisは暗黙のうちにグローバルオブジェクトにバインドされる
    * 第１のテストと同様に関数が呼び出されたときと同じ条件になる
    
```bash
touch src/Sum.js
```

```javascript
function sum() { //数値の合計を計算する
    var total = 0;
    for (var i = 0, l = arguments.length; i < l; i++) {
        total += arguments[i];
    }
    return total;
}
module.exports = sum;
```

```bash
touch spec/SumSpec.js
```

```javascript
sum = require('../src/Sum');
//applyを使って数値を合計する
describe('SumTest', function () {
    it('かっこで関数を呼び出して、一連の数値の合計を計算する', function () {
        expect(sum(1, 2, 3, 4, 5)).toBe(15);
        expect(sum.apply(null, [1, 2, 3, 4, 5])).toBe(15);
    });
    it('applyを使って数値の配列の合計を計算する', function () {
        expect(sum(1, 2, 3, 4, 5)).toBe(15);
        expect(sum.apply(null, [1, 2, 3, 4, 5])).toBe(15);
    });
});
```





