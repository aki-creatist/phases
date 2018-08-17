# レイアウト作成

* レイアウト用テンプレートの仕組み
* レイアウト・テンプレートの基本形
* オリジナルのレイアウトテンプレートを作る
* スタイルシートとスクリプト
* レイアウトテンプレートのコーディング
* レイアウトテンプレートを使う

## 概要

* CakePHP3では、あらかじめ用意されているレイアウト用のテンプレートを使い、コンテンツをレイアウトし表示する
* このレイアウト・テンプレートは、簡単に自作可能

## レイアウト用テンプレートの仕組み

* ここまで作成したページでは、
* 全て統一されたページレイアウトで表示されている
    * 右上には「Documentation」「API」といったリンクが表示されている
    * 右下にはCakePHPのアイコンが表示されている
    * また表示されるテキストやタイトル、フォームなども全て同じデザインになっている
* これらは全て同じ**レイアウト**を使っていたため、同一されたデザインで表示されていた

src/Template/に、各アクションのテンプレートファイルを用意していた

* がこれらのテンプレートファイルでは、`<body>`内にはめ込んで表示されるコンテンツ部分だけが作成されていた
* それ以外の、ページ全体の枠組みは、実はレイアウト用のテンプレートによって用意されていた
* このレイアウト用テンプレートは、**Template**/**Layout**/」にまとめられている
    * ここに、自分で作成したレイアウトファイルを配置し、コントローラー側で使用するレイアウトを設定する
        * オリジナルレイアウトを使ったページの表示が行えるように
        
### Template/Layout/

以下のようなテンプレートファイルが用意されている

* ajax.ctp
    * Ajax通信を使ってアクセスされた際に用いられる
        * Ajaxでは、ページのレイアウトなどは必要なく、ただコンテンツだけがテキストとして得られればいい
        * 余計なものを全て排除したレイアウトが用意される
* default.ctp
    * これが、通常のWebページ用に用意されているもの
        * これまで作成したWebページは全てこのレイアウトを使っていた
* error.ctp
    * エラー発生時に表示されるエラーページ用のレイアウト
* rs/default.ctp
    * RSS情報などをXMLコードとして出力するような場合に用いるもの
* Email内のdefault.ctp
    * メールの内容を生成する際のもので、テスト用とHTML用が用意されている

## レイアウト・テンプレートの基本形

* **default.ctp**を開くと参考になる
* 余計な部分を省略し、もっとも基本的なコードの形に整理すると下のリスト欄のようなものになる
* 出力関係は全て**fetch**というメソッドを使って出力がされる

```html
<!DOCTYPE html>
<html lang="en">
<head>  
<!--head内は各種のタグを自動出力するための処理が用意されている-->

<!--タイトルの出力
<title><?= h($this->fetch('title') ?></title>

<link rel="shortcut icon" href="favicon.ico" type="image/x-icon">

// 各種ヘッダータグの出力-->
echo $this->fetch('meta');
echo $this->fetch('css');
echo $this->fetch('script');
?>
</head>
<body>

<div id="header">
    <div id="menu">...</div>
</div>

<!--コンテンツの出力(読み込んだテンプレートのレンダリング結果がここに書き出される)-->
<?= $this->fetch('content') ?>

<div id="footer"></div>
</body>
</html>
```

## オリジナルのレイアウトテンプレートを作る

* レイアウトファイルは、通常のテンプレートファイルと同様にctpファイルとして作成する

```bash
touch Template/Layout/sample.ctp
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
<title><?= h($this->fetch('title') ?></title>
<link rel="shortcut icon" href="favicon.ico" type="image/x-icon">

// <b>sample.css</b>というファイルを用意し、これを読み込む
echo $this->Html->css('sample.css');
echo $this->fetch('meta');
echo $this->fetch('css');
echo $this->fetch('script');
?>
</head>
<body>

<div id="header">
    <!--ヘッダーの出力-->
    <?= _($header) ?></div>
</div>

<?= $this->fetch('content') ?>

<!--フッターの出力-->
<div id="footer"><?= _($header) ?></div></div>
</body>
</html>
```

### スタイルシートとスクリプト

続いて、スタイルシートのファイルを用意

* スタイルシートなどの静的ファイルは`webroot/`に配置する
    * 静的ファイル: プログラムを使い、その場で内容を生成するのではなく、ファイルとして設置したものがそのまま使われるもの
    * webroot/
        * cssフォルダ
            * スタイルシートのファイルを用意するところ
        * imgフォルダ
            * イメージファイルを用意するところ
        * jsフォルダ
            * JavaScriptによるスクリプトファイルを用意するところ
* これらを読み込むためのメソッドを利用することで、Webページ内からファイルを利用可能になる

```bash
touch webroot/css/sample.css
```

```css
/*webroot/css/sample.css*/
body{
    font-size:16px;
    color:#660000;
}

h1{
    font-size:20px;
    font-style:bold;
    background:#990000;
    color:white;
    padding:5px 10px;
}

#header{
    font-size:9px;
    color:#666666;
    text-align:center;
}

#footer{
    font-size:9px;
    color:#666666;
    text-align:right;
    border:1px solid #999999;
    border-width:1px 0px 0px 0px;
    margin: 50px 0px 0px 0px;
}
```

* 今回は、以下のタグとIDにスタイルシートを設定
    * `body`
    * `h1`
    * `#header`
    * `#footer`

## レイアウトテンプレートのコーディング

* 作成したオリジナルのレイアウトテンプレートを使う
* Hellosアプリケーションのindexアクションとして処理を用意

```bash
vim HellosController
```

```php
<?php 
namespace App\Controller;

use App\Controller\AppController;

class HellosController extends AppController
{
    public function initialize()
    {
        parent::initialize();

        // レイアウトテンプレートの設定
        $this->viewBuilder()->layout('sample');
        $this->set('header', '* this is sample site*');
        $this->set('footer', 'copyright 2015 AKI Fam.');    
    }
    
    public function index()
    {
        $msg = "これは、サンプルアクションです。";
        $this->set('message', $msg);
    }
}
```

### viewBuilder()

* `$this->viewBuilder()`
    * ビューを作成するためViewBuilderというクラスのインスタンスを取得するためのもの
    * `layout`というメソッドが、使用するレイアウトテンプレートを設定するためのメソッド
    * `layout('sample');`と実行する
        * CakePHP3は、`Layout/sample.ctp`をレイアウトテンプレートとして読み込みページを生成するようになる
* `initialize()`でこれを行うようにする
    * この`HellosController`クラスに用意される全てのアクションでレイアウトが使われるようになる

また、ヘッダーとフッター用の変数も用意している

```php
$this->set('header', '* this is sample site *');
$this->set('footer', 'copyright 2017 AKI fam');
```

* これらは、アクションメソッド側で再設定すれば、そちらが利用される
* とりあえず`initialize`でデフォルトの値を設定しておく
* あとは必要に応じてアクションメソッドで変更する

## レイアウトテンプレートを使う

* 作成したオリジナルのレイアウトテンプレートを使う
* まずは、アクションを用意
* 今回は、サンプルとしてHellosアプリケーションのindexアクションとして処理を用意
* オリジナルのレイアウトを使ったWebページが表示されるようになる

```bash
vim Template/Hellos/index.ctp
```

```html
<!--index.ctp-->
<div>
    <h1>Index Page</h1>
    <p><?= $message ?></p>
</div>
```

