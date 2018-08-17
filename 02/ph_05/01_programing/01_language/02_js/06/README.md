# タブパネルを作成する(loadメソッド)

* タブパネルを作成します。タブの部分をクリックすると、パネルの内容を切り替えるユーザーインターフェース
* 見慣れたUIを例に、jQueryのもっとも基本的なAjax機能であるloadメソッドについて学ぶ

```js
$(function() {
  var tabs = $('#container');
  $('> ul li:first a', tabs).addClass('selected');
  $('> div', tabs).load(
    $('> ul li:first a', tabs).attr('href'));
  $('> ul li a', tabs).click(function(e) {
    if (!$(this).hasClass('selected')) {
      $('> ul li a.selected', tabs).removeClass('selected');
      $(this).addClass('selected');
      $('> div', tabs).load($(this).attr('href'));
    }
    e.preventDefault();
  });
});
```

## タブパネルの構造を理解する

* 例によって、まずはタブパネルを実装するための前提となるHTML、CSSのコードについて確認します。</p>

### (1)タブパネルの基本的な骨格

* タブを`<ul>`要素で、タブの内容を表すパネル部分を<div>要素で表現している
* また、タブパネル全体を`<div id = "container">`要素で囲んでいる点にも注目
* これは、タブとパネルを収めるためのコンテナー(入れ物)の役割を果たす
* 以下は、タブパネルの最低限の骨格

```html
<div style="background-color:#CFC">

<div id="container"> //タブパネル全体
<div style="background-color:#FF6">
    　　<ul> //タブリスト
    　　　　<li><a href="html.html">HTML</a></li>
    　　　　　~中略~
    　　</ul>
</div>
<div style="background-color:#F6F">　　<div></div> //表示パネル部分</div>
</div>
</div>
```

### (2)タブリストを横並びにスタイル付けする

* タブのスタイル付けをしているのは、tab.cssの以下の部分

```css
#contain > ul li {
  list-style-type: none;
  float: left;
  line-height: 160%;
  width: 138px;
  height: 40px;
}
```

* `<ul>`リストでは、箇条書き項目が縦並びに、かつ、箇条書きを表す`・`が先頭に付与されるのがデフォルト
* そこでスタイルシートの側でそれぞれの項目が横並びになるよう`(float:left)`、かつ行頭マークがつかないように`(list.style-type:none;)`を設定

### (3)タブパネルの内容(リンク先)は<a>要素で表す

* パネルに表示すべき内容(リンク先)は、`<a>`要素のhref属性で表す

```html
<li><a href="html.html">HTML</a></li>
```

* これは、JavaScrip機能がオフになっている場合に備えての措置

### (4)標準＆選択時のスタイルを定義する

* タブに対して、標準状態 `(#container > ul li a)`、タブが選択されている状態`(#container > ul li a.selected)`と、２種類のスタイルを定義しておく

```css
#container > ul li a {
  display: block;
  text-align: center;
  text-decoration: none;
  background-color: #cfc;
  color: #000;
  border: solid 1px Black;
}

#container > ul li a.selected {
  background-color: #000;
  color: #fff;
}
```

* 基本的なスタイルは<`span style="background-color:#FADBE1">#container > ul li a</span>`セレクターで定義
* `<span style="background-color:#FADBE1">#container > ul li a.selected</span>`セレクターでは背景/文字色のみを差し替えている

## 外部ファイルを読み込む --loadメソッド--

* loadメソッドは、jQueryで提供されているAjax関連メソッドの中でももっともシンプルなメソッドで、指定されたファイルを読み込み、現在の要素に反映させる

```js
$(セレクター).load(読み込むファイルのパス)
```

* htmlメソッドについはすでに触れていますが、`loadメソッドはhtmlメソッドのAjax対応版`と考えるとわかりやすい
* htmlメソッドではページに埋め込むべきコンテンツを文字列で直接指定するのに対して、`loadメソッドではコンテンツを含んだファイルで指定`する
* 例えば、`<div id="result">`要素にhtml.htmlの内容を埋め込むには、以下のように記述する

```js
$('#result').load('html.html');
```

## タブクリック時にパネルの内容を読み込む

### (1)先頭のタブを選択状態にする

* ページを読み込んだタイミングで、タブパネルを初期化する

```js
var tabs = $('#container');
$('> ul li:first a', tabs).addClass('selected');
$('> div', tabs).load(
  $('> ul li:first a', tabs).attr('href'));
```

* まず、先頭のタブは$(> ul li:first a', tabs)で取得できます。タブの選択状態を表すには、スタイルクラスとしてあらかじめ用意しておいたselectedを適用すれば良いのでした。
* 続いて、３行目〜４行目は、パネルの表示を最初のタブの内容で初期化しています。
* `範囲検索`が行われている点も注目
* 以下の書式が使用されている

```js
$(セレクター, 基点)
```

* `$()`関数は、まず文書全体に対して検索を行うのが基本
* 基点を指定することで、特定の要素を基点として検索も可能
* 近接する要素がすでに取り出せているならば、「基点」をきちんと指定した方がスピードはアップする
* `$('> div', tabls).load(...)`はリンク先の内容をタブパネル(`<div>要素`)に反映させないという意味

### (2)タブが選択された時にパネル内容を書き換える

* あとは、タブをクリックした時にタブのスタイルを変更し、パネルの内容を書き換えるだけ

```js
$('> ul li a', tabs).click(function(e) {
  if (!$(this).hasClass('selected')) {
    $('> ul li a.selected', tabs).removeClass('selected');
    $(this).addClass('selected');
    $('> div', tabs).load($(this).attr('href'));
  }
  e.preventDefault();
});
```

* タブ($('> ul li a', tabls)をクリックしたときのイベント処理を設定します。
* ９行目では、まずタブが選択状態であるか(クリックされた<a>要素がselectedクラスを持つかどうかを判定しています。すでに選択状態であるならば、以降の処理は必要ないからです。その場合は、処理をスキップして、１５行目でclickイベントのキャンセルのみを行います。(さもないと、リンクの本来の挙動によってページが移動してしまいます)。
* 続いて、１１〜１３行目は選択状態にないタブが新たにクリックされた場合の処理です。この場合、まずは選択状態のタブ($('< ul li a,selected', tabs))からselectedクラスを除去します。
* その上で、「$(this).addClass('selected');」で、クリックされたタブ($(this))に対してselectedクラスを改めて適用します。
* タブを処理できたら、あとはパネル全体を書き換えるだけです。「$('> div', tabs)」はタブパネルを、「$(this).attr('href')」はクリックされたタブのリンク先をそれぞれ意味します。
* よって、「$('> div', tabs).load(...)」で「タブパネルを、クリックされたタブのリンク先によって書き換えなさい」という意味になります。
