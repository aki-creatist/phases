# スコープチェーン

* 関数が呼び出されると、制御は新しい実行コンテキストに入る
* 関数内の識別子の解決には、アクティベーションオブジェクトが使われる
* 実は、識別子の解決はスコープチェーンを通じて行われる
    * その出発点が現在の実行コンテキストのアクティベーションオブジェクト
    * スコープチェーンの終点は、グローバルオブジェクト

## 関数の実装

* この関数に数値を与えて呼び出すと、関数が返される
* この関数を呼び出すと、引数に先ほどの数値を加えた値が返される

```bash
touch spec/AddrSpec.js
```

```javascript
function adder(base) { //ほかの関数を返す関数
    return function (num) { //インクリメント、デクリメント関数
        return base + num;
    };
}
describe('AdderTest', function () {

});
```

## テストの実装

* adderを使ってインクリメント、デクリメント関数を作成
    * `inc()`
        * スコープチェーンの先頭は、inc自身のアクティベーションオブジェクト

## 前提のテスト

```bash
vim spec/AddrSpec.js
```

```diff
  describe('AdderTest', function () {
+     it('test should add or subtract one from arg', function () {
+         var inc = adder('これはbaseになり、');
+         expect(inc('これはnumになる')).toBe('これはbaseになり、これはnumになる');
+     })
  });
```

* adderで作られ、返された関数の内部では、base変数は**自由変数**
    * すなわちadder関数が実行を終了した後も生き残る変数
    * この動作は**クロシージャ**とも呼ばれる
    
```diff
  it('test should add or subtract one from arg', function () {
-     var inc = adder('これはbaseになり、');  
+     var inc = adder(1);
+     var dec = adder(-1);

-     expect(inc('これはnumになる')).toBe('これはbaseになり、これはnumになる');
+     expect(3).toBe(inc(2));
+     expect(3).toBe(dec(4));
+     expect(3).toBe(inc(dec(3)));
  })
```

### 関数式について

* 関数式は、条件に基づいて関数を定義しなければならないときに役立つ
* 関数宣言は、ブロック内では関数のホイストのために、必ず第2実装が使われる
    * if-else式の中etc
* `trim()`を持たないブラウザではString.prototypeオブジェクトで直接定義する
* ブラウザが`trim()`をネイティブにサポートしていなくても実行可能
    * " string ".trim()を使って空白を除去可能
    
```javascript
//条件に基づいて文字列メソッドを提供する
if (!String.prototype.trim) {
    String.prototype.trim = function () {
        return this.replace(/^\s+|\s+$/g, "");
    };
}
```

* しかし、こうして定義したメソッドを使うとデバッグ時に困る
    * ナビゲートしたりエラーの原因をみつけたりしにくくなる
    * 以下のような名前付き関数式なら、この問題を解決可能
* 識別子は内側のスコープに属し、関数を定義している側のスコープからは見えない

## 注意

* Internet Explorerは、名前つき関数を前にすると、２つの別々の関数オブジェクトを作る
    * 識別子を外側のスコープにリークし、そのうちの１つをホイストしてしまう
* 同じ名前の変数に関数式を代入すれば、関数オブジェクトの重複は避けられる
    * しかしスコープリークとホイストは消えない
* 必要に応じて分岐が異なれば名前も変わるようにして、クロージャ内の関数宣言を使い、名前つき関数式を避けるようにする
* もちろん、関数宣言はホイストされ、外側のスコープからも見える
