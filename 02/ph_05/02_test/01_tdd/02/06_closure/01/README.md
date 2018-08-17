# 関数のバインド

## 背景

* コールバック関数をメソッドに渡す際、暗黙のthisの値は失われる
    * JSでは**メソッドを実行するオブジェクトを一緒に渡す**必要がある
    * `メソッドを実行するオブジェクトを一緒に渡す`とは,,,
        * 見た目としては関数の実行をfunctionステートメントでラップしリターンした状態
* これは、thisのセマンティクスをよく理解していないとわかりにくい
    * `セマンティクス`: プログラム中に含まれた意図

## thisが消失する不都合

* 例: `A`が`B`に`C`という仕事を行わせる場合
    * `A`が書いた手順`C`は、それをなぞれば`B`にも実行可能であるべき
        * 手順は`A`以外が実施しても実行可能であることを前提とする
    * つまり`this`は`A`が持っている能力(メソッドやプロパティ)がなければならない
    * `this`が`B`の能力`メソッドやプロパティ`になってしまうと実施不可になる
        * 手順だけ知っていても実施ができない

## 用語

### コールバック関数

* `コールバック関数`: 関数に引数として渡される関数
    * 渡されたメソッドの側でこの関数を実行する

### 手作業

* ここではthisの消失を防ぐためクロージャなどを記述すること
* 例として、ここでの`手作業ではない状態`はbindなどを利用している状態

```javascript
function showThis(){
    console.log(this);
}

var foo = showThis.bind("AKI");

foo();
```

### クロージャを作るとは

* 変数に無名関数を代入すること

### thisの消失：ライトボックスの例

* `ライトボックス`: ページに重ねあわされ、ページのほかの部分の上に浮いているように見えるボックス
    * あるURLから内容を取り出し、div要素内でそれを表示する
    * `anchorLightbox`関数
        * アンカーをクリックすると、リンクされているページが、現在のページ上のdivにロードされる
* [ライトボックスの擬似コード](anchorLightbox.js)
    * このコードは、この形のままでは実行不可

## 暗黙のバインドの消失

* イベントハンドラとして`lb.open()`代入の際、`thisからlbオブジェクトへの暗黙のバインドが失われる`
    * そのため現時点ではリンクをクリックしても期待したふるまいをしない
    * `暗黙のバインド`があるのは、この関数がlbオブジェクトのプロパテイとして呼び出されたときのみ

```javascript
var lightbox = {
    open: function () {
        ajax.loadFragment( this.url, { //targetオプションが指定するDOM要素にURLの内容をロードする
            target: this.create()
        });

        return false;
    },
    close: function () { /* ... */ },
    destory: function () { /* ... *},
    create: function () {
        /* コンテナを作るか既存のコンテナを返す */
    }
};
//アンカー要素をライトボックスに変換する関数
function anchorLightbox(anchor, options) {
    var lb = Object.create(lightbox); //lightboxオブジェクトを継承する新しいオブジェクトを作る
    lb.url = anchor.href;                   //主要プロパテイを設定
    lb.title = anchor.title || anchor.href; //主要プロパテイを設定
    Object.extend(lb, options);
    anchor.onclick = lb.open; //clickイベントのイベントハンドラを設定する

    return lb; //新オブジェクトを返す
}
```

### 無名関数を使った解決方法

* イベントハンドラとして`無名関数を代入`する
    * すると、クロージャが作られる
    * クロージャを使ってイベントを処理をしている
        * 実質的に`メソッド呼び出しをプロキシ化`している
        * すると、今度はライトボックスアンカーも動作する
    
```diff
//無名プロキシ関数を介したopen呼び出し
  function anchorLightbox(anchor, options){
      /* ... */
-     anchor.onclick = lb.open;     //clickイベントのイベントハンドラを設定する
+     anchor.onclick = function() { //正しいthisの値がセットされた状態でopen()を呼び出す
+         return lb.open();         //これが`メソッドを実行するオブジェクトを一緒に渡す`ということ
+     };
      /* ... */
}
```

### クロージャ使用による変化

* 関数の動作
    * 通常
        * 実行終了後は変数オブジェクトと実行コンテキストは参照されくなる
        * ガベージコレクションの対象になる
    * クロージャ
        * 実行終了後も実行コンテキストのスコープチェーンにアクセス可能なままの状態になる
* 今回の場合`anchorLightbox実行終了後`も、anchorオブジェクトはスコープチェーンにアクセス可能ということ
    * onClickプロパテイを通じて、アクセスする

### 内側の無名関数が使用している変数

* 内側の無名関数はlb変数を使用している
    * これは仮引数でもローカル変数でもない
    * スコープチェーンからアクセス可能な`自由変数`

### リファクタリング

* メソッド呼び出しを手作業でラップするのは、正しい方法ではない
* 複数のイベントハンドラを同様の定義をすると重複を招く
    * コードが理解しずらく保守が困難なものになる
* そこで`bind`を利用した実装に置き換える
    * `bind`: `オブジェクトをthisとして`元の関数を呼び出す

## bind()

* `オブジェクトをthisとして`元の関数を呼び出す
    * 第1引数としてオブジェクトを受け付け、関数オブジェクトを返す
    * この関数オブジェクトを呼び出すと、第1引数のオブジェクトを`this`として`元の関数`が呼び出される
    * `call`、`apply`の遅延バージョン

### Function.prototype.bind

* bindの利用で`anchorLightbox`は以下のようにアップデート可能

```diff
  //bindの使い方
  function anchorLightbox(anchor, options) {
      /* ... */
-     anchor.onclick=function() { //正しいthisの値がセットされた状態でopen()を呼び出す
-         return lb.open();
-     };
+     anchor.onclick = lb.open.bind(lb);
      /* ... */
  }
```

### bindを実装する

* この関数が実装されていないブラウザのために独自実装も可能
* 返された関数を実行すると**元の関数**が呼び出される
    * `thisとしてバインドされたオブジェクトが明示的に設定された状態`で呼び出される
    * 返された関数に渡された実引数は、すべて**元の関数**に渡される

```javascript
//bindの実装 - thisObj引数と関数自体への参照を維持する関数（クロージャ）を返す
if (!Function.prototype.bind) {
    Function.prototype.bind = function (thisObj) {
        //以下のthisはメソッドの呼び出しに使われたオブジェクトを参照する
        var target = this; //この値へのアクセスは、外側の関数のローカル変数に格納が必要
        
        return function () {
            return target.apply(thisObj, arguments);
        };
    };
}
```

* Function.prototypeに関数を追加する
    * これは`全ての関数オブジェクトのメソッドとしてその関数を使用可能`にする
* `this`は、新しい実行コンテキストに入るときに計算され、スコープチェーンの一部ではない
    * これを**ローカル変数に代入**すると、**内側の関数のスコープチェーンを介してアクセス可能**になる

### 引数とのバインド

* 関数に引数をプレフィルし、オブジェクトにバインドする
* setTimeoutにコールバックを渡して、何らかの計算を先延ばししたいときなどに有用
* 例: SetTimeoutでベンチマークを遅延実行するために、bindを使って引数に関数をプレフイルする
    * `forEach()`にArray `benchmark`を要素の数だけ繰り返させる
    * Array `benchmark`を要素の数だけ繰り返させる処理をコールバック関数として`bench`に渡す
    * `bench`は渡されたコールバック関数を100回繰り返す
    * `setTimeout()`は第二引数の500msごとに`bench`を実行する
    * ここでは、setTimeoutに渡された無名関数呼び出しを手作業で行うのではない
        * bindを使ってbenchmarks配列に`foreach()`をバインド
        * 引数にbench関数をバインドすることによって、benchmarks配列のすべてのベンチマークを実行

```javascript
//bindとsetTimeoutを使ったメソッド呼び出しの遅延実行
function bench(fanc) { //bench関数は、引数として渡された関数を10000回呼び出して、結果をログに書き込む
    var start = new Date().getTime();
    
    for ( var i = 0; i < 100; i++) {
        func();
    }
    
    console.log(func, new Date().getTtime() - start);
}

var benchmarks = {
    function forLoop() { /* ... */ },
    function forLoopCachedLength() { /* ... */ },
    /* ... */
};

setTimeout(benchmarks.forEach.bind(benchmarks, bench), 500);
```

### 手作業だとどうなる？

```javascript
var forEach = function() {
    return 'benchmarksを要素の分だけ繰り返す処理'
}
var bench = function() {
    return 'forEachを100回繰り返す処理'
}
setTimeout(bench, 500)
```

### thisだけでなく引数にも関数をバインドできるbindの実装例

* 単純なのはよいが、パフォーマンスが低い
    * bindは、単純に**オブジェクトに関数をバインドするために使用**される
    * つまり、引数のバインドはあまり行われない
    * この条件のもとでは引数の変換と連結はバインド時とバインドされた関数の呼び出し時の両方
        * これは呼び出しにかかる時間を遅くする

```javascript
//引数のバインドもサポートするbind
if (!Function.prototype.bind) {
    Function.prototype.bind = function (thisObj) {
        var target = this;
        var args = Array.prototype.slice.call(arguments, 1);
        
        //bindに渡された引数を配列で管理
        return function () {
            var received = Array.prototype.slice.call(arguments);
            //バインドされた関数が呼び出された際、配列と、実際の呼び出しが受け付けたその他の引数を連結する
            return target.apply(thisObj.args.concat(received);
        };
    };
}
```

### bindを最適化する

* パフォーマンスを向上する

#### 処理すべき条件は、次の4つ
* オブジェクトに関数をバインドするが、引数にはバインドしない
* オブジェクトに関数をバインドし、1つ以上の引数に関数をバインドする
* バインドされた関数を引数なしで呼び出す
* バインドされた関数を引数つきで呼び出す
* 後ろの2つは、前の2つのどちらでも起きるので、バインド時の条件は2種類、呼び出し時の条件は4種類

### 最適化後のソース

* [src/bind.js](src/bind.js)
* オブジェクトに関数をバインドするだけで引数へのバインドがなく、引数なしで呼び出す
* 戻り値の関数はnew式のなかで使われたときにバインドされた関数としてふるまわなければならない
    * しかしここでは反映していないため注意
