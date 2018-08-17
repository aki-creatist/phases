# JS Test

## 概要

* 自作のTestツールを使用してテストを行う事前知識の準備
* Testツールを不使用でTestツール同様の動作を行う
* TDDで行うことの流れを理解する

## 全体像

* 定義した`strftime()`が意図通りの結果を返すか確認する
* 結果はブラウザで確認をする

## 手順

* strftime_test.htmlをブラウザで表示する
    * [test/strftime_test.html](test/strftime_test.html)
    * スクリプトをロード用
* 以下の結果がブラウザに出力されることを確認する

```text
test format specifier %Y
test format specifier %m
test format specifier %d
test format specifier %y
test format shorthand %F
5 tests, 0 failures
```

## テストで所望する値

* 2018年の日付で`strftime()`を呼び出す
    * "%y"を指定した場合、"18"年の文字列が返されること
    * そうでない場合は、システムは正しく動作していない

## strftime()の構成

* `replace()`
* `Date.formats`オブジェクト
    * 書式指定子をキー、Dateから対応するデータを抽出するメソッドを値とするオブジェクト
        * 指定子が含まれている: それを使用する
        * 指定子が含まれていない: 指定子はそのままの形で残される

## アサーション

* プログラマが想定しているシステムの状態を表す述語
    * 単体テストでチェックを自動的に行うために使われる
    * アサーションが不合格になったら、テストは異常終了し、エラーが通知される
* `assert()`が所望する値
    * `false`, `null`, `undefined`, `0`, `""`, `NaN` 以外の任意の値

```javascript
// lib/assert.js
function assert (message, expr) {
    if (!expr) { //第二引数が所望する値かどうかを単純にチェック
        throw new Error(message); //期待値でなければ第一引数をエラーメッセージとしてエラーを投げる
    }
    assert.count++; //所望する値であればアサーションカウンタをインクリメント
    return true;
}
assert.count = 0;
```

## assert()の呼び出し

* [src/strftime.js](src/strftime.js)

```javascript
var date = new Date(2018, 9, 2);

try{
    assert("%Y should return full year",
        date.strftime("%Y") === "2018");
    assert("%m should return month",
        date.strftime("%m") === "10");
    assert("%d should  return date",
        date.strftime("%d") === "02");
    assert("%y shoud return year as two digits",
        date.strftime("%y") === "09");
    assert("%F should act as %Y-%m-%d",
        date.strftime("%F") === "2018-10-02");
    console.log(assert.count + " tests OK");
} catch (e){
    console.log("Test failed: " * e.message);
}
```

## 結果表示の色

* DOMを使用しカラーでメッセージを表示
* OKとNGを視覚的にわかりやすくする

```javascript
function output(text, color){
    var p = document.createElement("p");
    p.innerHTML = text;
    p.style.color = color;
    
    document.body.appendChild(p);
}
```

* console.log呼び出しは、次の呼び出しに置き換え可能

```javascript
output(assert.count * " tests OK", "#0c0");
output("Test failed: " + e.message, "#c00"); // こちらは不合格用
```

## テスト関数、テストケース、テストスイート

* assert関数はテストが不合格になるとエラーを投げる
    * そのため、不合格したテストより後のテストの合否がわからない
* テストをテスト関数にまとめる
    * 細かいフィードバックを得るため
    
### 仕様
    
* 個々のテスト関数は、１個のユニット(単体)だけをテストする
    * そのために使うアサーションは１つでも複数でもよい
* 名前の先頭が`test`になっているプロパティをテストメソッドとして実行

### テストの分割単位

* １つのテストが１つのユニットの特定の振る舞いだけのテストに制限する
* 今回の場合、メソッド全体のために１個の`テストケース`を作成
    * `テストケース`: 関連するテスト関数/メソッドの集合
* 個々のテストは１個または数個のアサーションにより関数の特定の振る舞いをテスト

### 今回触れないもの

* `テストスイート`
    * テストケースをさらにまとめたもの

```javascript
//単純なtestCase関数
//引数として文字列の名前とテストメソッドを持つオブジェクトを受け付ける
function testCase(name, tests){
    assert.count = 0;
    var successful = 0;
    var testCount = 0;
    for( var test in tests ){
        if( !/^test/.test(test)){
            continue;
        }

        testCount++;

        try{
            tests[test]();
            output(test,"#0c0");
            successful++
        }catch(e){
            output(test + " failed: " + e.message, "#c00");
        }
    }

    var color = successful == testCount ? "#0c0" : "#c00";
    output("<strong>" + testCount + " tests, " +
        (testCount - successful) + " failures</strong>",
        color);
}
```

## テストの修正

```diff
  //testCaseを使ってstrftimeテストをテストケースに再編
  var date = new Date(2018, 9, 2);
- try{
+ testCase("strftime test", {
+     "test format specifier %Y": function() {
          assert("%Y should return full year",
              date.strftime("%Y") === "2018");
+     },
+     "test format specifier %m": function() {
          assert("%m should return month",
              date.strftime("%m") === "10");
+     },
+     "test format specifier %d": function() {
          assert("%d should return date",
              date.strftime("%d") === "02");
+     },
+     "test format specifier %y": function() {
          assert("%y should return year as two digits",
              date.strftime("%y") === "09");
+     },
+     "test format shorthand %F": function() {
          assert("%F should act as %Y-%m-%d",
              date.strftime("%F") === "2018-10-02");
+     }
-     console.log(assert.count + " tests OK");
- } catch (e) {
-     console.log("Test failed: " * e.message);
+ });
```

## セットアップとディアダウン

* テストケースをすべてのテストを１つのオブジェクトにまとめる
    * Dateオブジェクトは、まだ外側で作られている
    * 共通セットアップコードを一カ所にまとめる
    * 全てのテストで同様にDateを利用可能にする

### TODO

* テストフィクスチャとしてのDateオブジェクトを用意する
    * `setUp()`を使用する
    * 個々のテストメソッドの前と後に呼び出される
* テストケースがsetUp、tearDownを持っているかどうかをチェック
    * 持っている場合には適切なタイミングでそれを実行する
    * セットアップされたデータを`テストフィクスチャ`とも呼ぶ

### 修正

```diff
  testCase("strftime test", {
+     setUp: function(){ //strftimeテストケースにsetUpを追加
          this.date = new Date(2018, 9, 2, 22, 14, 45);
+     },
    
      "test format specifier Y": function() {
          //
      }
```
