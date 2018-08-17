# メモ化

* クロージヤの最後のサンプルは、メモ化、すなわちメソッドレベルでのキャッシングテクニック
* コストの高い処理の反復実行を避けて、プログラムをスピードアップさせる
* 以下は数列内の特定の位置の値を計算している
    * 2つの再帰呼び出しを使用

```javascript
//フイボナッチ数列の実装を示したもの
function fibonacci(x) {
    if (x < 2) {
        return 1;
    }
    
    return fibonacci(x - 1) + fibonacci(x - 2);
}
```

* フイボナッチ数列は非常にコストが高い
    * あっという間に再帰呼び出しが膨大な数になってブラウザでは処理不可になる
* 関数をクロージヤでラップすれば値を手作業でメモ化し、このメソッドを最適化できる
* [src/fibonacci.js](src/fibonacci.js)
* この新バージョンのfibonacciは、オリジナルと比べて何桁分も高速に実行可能
    * 拡張によって計算できる数が増加

## リファクタリング

* 現在は、計算とキャッシュロジックが混ざっている
    * 問題の分割をするため、Function.prototypeに関数を追加する

```javascript
//計算ロジックを混ぜずに、メソッドをラップしてメモ化機能を追加可能
if (!Function.prototype.memoize) {
    Function.prototype.memoize = function () {
        var cache = {};
        var func = this;
        
        return function (x) {
            if (!(x in cache)) {
                cache[x] = func.call(this, x);
            }
            
            return cache[x];
        };
    };
}
```

* このメソッドを使えば、以下のように、関数をクリーンにメモ化できる

```javascript
//fibonacci関数のメモ化
TestCase("FibonacciTest", {
    "test calculate high fib value with memoization":
    function () {
        var finbonacciFast = fibonacci.memoize();
        
        assertEquals(1346269, fibonacciFast(30));
    }
});
```

## memoize()の注意

* 処理可能なのは`1個の引数を取る関数`のみ
* 用途が限られる
    * プロパテイ代入の性質から、全ての引数を文字列に強制型変換するため

## 改良

* キーとして使うために、すべての引数をシリアライズする
* 引数を単純にjoinしてしまえば、複雑さはすでにあるコードと大差ない
* [src/memoize.js](src/memoize.js)
* このバージョンは、前バージョンほどパフォーマンスは高くない
    * joinを呼び出した上に、callではなくapplyを使っているため
    * 引数の個数について前提条件を設けられないので、applyを使うのはやむをえない
    * 例として引数として渡された`i'120!`と`12`を区別できない
        * 全ての引数を文字列に強制型変換しているため
    * カンマを含む文字列引数を使うと、誤った値がロードされる
        * 最後に、引数をカンマで連結してキャッシュキーを生成しているため
        * つまり、(1, "b")は、("1, b")と同じキャッシュキーを生成する
* 引数の型情報を組み込んだ適切なシリアライザを実装することは可能
    * さらに、tddjs.uidを使ったオブジェクト引数のシリアライズは、単純で高速
        * しかしメソッドが引数に新しいプロパテイを代入してしまう可能性がある
