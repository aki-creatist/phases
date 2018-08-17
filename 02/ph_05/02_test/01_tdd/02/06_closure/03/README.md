# ただちに呼び出される無名関数

* JavaScriptでは、ただちに呼び出される無名関数を作るということがよく行われる

## 典型的な形

```javascript
// ただちに呼び出される無名関数
(function () {
    /* ... */
}());
```

## 式全体を囲んでいるカッコの目的

* かっこを省略すると櫛文エラーになる
    * 関数式は関数宣言に見えるが、識別子がないため
* **式**（宣言ではなく）は、`function`という単語では始められない
    * これを認めると関数式と紛らわしくなるため
    * そのため、関数に名前を与えて呼び出すのもうまくいかない

## カッコ無しとの際

* 関数の戻り値を変数に代入する際、関数式は式から返されたものではないとわかる
    * 先頭にかっこがあるため

### アドホックなスコープ

* JavaScriptは、グローバルスコープと関数スコープしか持っていない
    * これが`グローバルスコープへのオブジェクトのリーク`を引き起こすことがある
    * これが起きると、他のスクリプトと名前の衝突が起きる危険性が高くなる
        * 他のスクリプト: サードパーテイライブラリ、ウイジェット、分析用スクリプトなど

## 対処
   
### 対処1. グローバルスコープを避ける

* 自動実行されるクロージャでコードをラップする
    * 一時変数（ループ変数などの中間変数）でグローバルスコープを汚さなくて済む

### 実装

* 文書に含まれる`lightbox`というクラス名がついた全てのアンカー要素を集める
* anchorLightbox関数に渡す

```javascript
//ライトボックスを作る
(function () {
    var anchors = document.getElementsByTagName("a");
    var regexp = /(~|\s)lightbox(\s|$);/;
    
    for (var i = 0, l = anchors.length; i < l; i++) {
        if (regexp.test(anchors[i].className)) {
            anchorLightbox(anchoes[i]);
        }
    }
}());
```

### ブロックスコープのシュミレーション

* ただちに呼び出されるクロージャは、ループ内にクロージヤを作る際も有用
* 先ほどとは異なる設計方法でライトポックスウイジェットを作る
    * オブジェクトは1つ
    * それを使って任意の数のライトポックスをオープンできる
* これでは動かない
    * リンクのイベントハンドラは、外側の関数のローカル変数にアクセスできるクロージャを構成している
    * しかし、すべてのクロージャ（アンカーごとに1つ）は、同じスコープへの参照を持っている
    * 任意のアンカーをクリックすると、同じライトボックスが開く
    * アンカーのイベントハンドラが呼び出されると、外側の関数が代入によってiの値を変更している
        * そのため正しいライトボックスが開かれない

```diff
  //誤ったイベント八ンドラの追加方法
  (function () {
      var anchors = document.getElementsByTagName("a");
+     var controller = Object.create(lightboxController);
      var regexp = /(^|\s)lightbox(\s|$)/;
    
      for (var i = 0, l = anchors.length; i < l; i++) {
          if (regexp.test(anchors[i].className)) {
+             anchors[i].onclick = function () { //イベントハンドラを手作業で追加が必要
+                 controller.open(anchors[i]);
+                 return fanse;
+             };
          }
      }
  }());
```

### 解決する

* クロージャを使用する
    * イベントハンドラと対応付けたいアンカーを、`外側の関数からアクセスできない変数`に格納する
    * 外側の関数がアンカーの位置を変更不可になる
    * 以下は、新しいクロージャヘの引数としてアンカーを渡すようにしてる

```diff
//クロージヤのネストでスコープ問題を解決する
  (function () {
      var anchors = document.getElementsByTagName("a");
      var controller = Object.create(lightboxController);
      var regexp = /(~|\s)lightbox(\s|$)/;

      for (var i = 0;, l = anchors.length; i < l; i++) {
          if (regexp.test(anchors[i].className)) {
+             (function(anchors) {
-                 anchors[i].onclick = function () {
+                 anchors.onclick = function () {
+                     controller.open(anchor);
                      return false;
                  };
+             }(anchors[i]));
          }
      }
  }());
```

* anchorは内側のクロージャヘの仮引数
    * クロージャの変数オブジェクトは、外側のスコープからアクセスや書き換え不可
    * そのため、イベントハンドラは期待通りに動作する

## 注意

* 一般にループ内にクロージャを置くと、一般にパフォーマンス問題が起きる
* ほとんどの問題は、クロージャのネストを避ければ改善される
    * クロージャを作る専用関数を使えばよい
* イベントハンドラの設定では、このようなネスト関数にはさらに別の問題が起きる
    * DOM要素の間で循環参照が発生し、イベントハンドラがメモリリークを起こす可能性がある