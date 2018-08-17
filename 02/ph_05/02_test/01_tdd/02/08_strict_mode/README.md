# 厳密モードでの違い

## 暗黙のグローバルの禁止

* 厳密モードでは、宣言されていない変数を使うとReferenceErrorが起きる

```javascript
function sum(numbers) { //暗黙のグローバル
    "use strict";
    var total = 0;

    for (i = 0; i < numbers.length; i++) {
        total += numbers[i];
    }

    return total;
}
console.log(sum([1,2]));
// 非厳密モード:グローバルオブジェクトのプロパテイiが作られる
// ES5厳密モード:ReferenceError
```

### 厳密モードのarguments

* argumentsのCallerまたはcalleeプロパティにアクセスすると`TypeError`になる
    * 非厳密モードでは、argumentsオブジェクトは仮引数と動的な関係を共有する
* 仮引数を変更すると、argumentsオブジェクトの対応するインデックスの値も変更される
* argumentsオブジェクトの値を変更すると、対応する仮引数も変更される
    * 厳密モードではこのような関係はなくなり、argumentsはイミュータブルになる

```bash
touch spec/StrictSpec.js
```

```javascript
function switchArgs(a, b) { //argumentsと仮引数の関係
    "use strict";
    var c = b;
    b = a;
    a = c;

    return [].slice.call(arguments);
}

describe('ArgumentsParametersTest', function () {
    it('test should switch arguments', function () {
        // ES5厳密モードで合格
        // expect(switchArgs(2, 3)).toEqual([3, 2]);

        // ES3で合格
        expect(switchArgs(2, 3)).toEqual([2, 3]);
    });
});
```

## this

* 厳密モードでは、thisが強制的にオブジェクトに型変換されることはない
* thisがまだオブジェクトでなければ、強制的にオブジェクトに型変換される
* 呼び出された関数のthisはグローバルオブジェクトに変換されない
    * 例: 関数オブジェクトのcall、`apply()`を使う際、`null`や`undefined`を渡しても同様
* また、thisとしてプリミティブ値を使っても、それがラッパーオブジェクトに型変換されることはない

### 厳密モードのオブジェクト、プロパティ、変数

* evalとargumentsは、厳密モードでは識別子として使えない
* この制限は、仮引数、変数、try-catch文の例外オブジェクト、オブジェクトプロパテイに影響を与える
* 暗黙のグローバルは禁止
* configurable属性がfalseのプロパテイでdelete演算子を実行すると、プロパティは削除されない
    * 厳密モードでは、そのような削除は、TypeErrorを起こす