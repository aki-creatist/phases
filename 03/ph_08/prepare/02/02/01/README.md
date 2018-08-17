# Routeセッティング

## 概要

## CakePHP3ルーティング

### コントローラの階層構造

* `/config/routes.php`を編集することでコントローラの階層をネスト可能

```php
Router::prefix("ディレクトリ名", function($routes) {
    $routes->fallbacks(DashedRoute::class);
});
```

# Laraveルーティング

## ルーティングの基本

* Laravelはコントローラを経由せずにテンプレートファイル(表示用ファイル)を表示可能

/routes/web.php

```php
<?php
use Illuminate\Http\Request;  //HTTPリクエストを扱うためのメソッドを参照可能にする 

Route::get('/', function () {  //localhost/に接続したら指定したテンプレートを表示する
    return view('テンプレート'); //view関数に引数としてテンプレートを渡す
});                            //view('index')とすればテンプレートindex.blade.phpを表示する
```

## ハマるポイント

* 公開ディレクトリ(ここではデフォルトのままpublic)内のindex.phpが、URLをweb.phpに渡す
* web.phpで定義するのは公開ディレクトリ名以降

```text
http://localhost/公開ディレクトリ名(public)/web.phpで定義したルート
```

例えば、HelloWorldと表示するプログラムにルーティングをする場合、web.phpの記述は以下

```php
// アクセスURL http://localhost/public/hellos
Route::get('/hellos' function() {
    echo "Hello World";
});
```

* アクセスURLがわからなくなったら、index.phpはどこにあるかを探す
* index.phpまでのURLを書いたら、その次にweb.phpを確認する

## コントローラの指定

* cakePHPではコントローラ名がURIになるが、Laravelではコントローラとメソッドを呼び出すURIを設定可能

/routes/web.php

```diff
  Route::get('/', function () {
      return view('テンプレート');
  });

  // localhost/frame-worksに接続したらFrameWorksController.phpのprologue()を呼び出す
+ Route::get('/frame-works/prologue','FrameWorksController@prologue');
```

## コントローラの階層構造

/routes/web.phpを編集することでコントローラの階層をネスト可能

```diff
  // 呼び出し方は変わらず、app/Http/Controllers/FrameWorksControllerにアクセス
- Route::get('/frame-works/prologue','FrameWorksController@prologue');
+ Route::get('/frame-works/prologue','ディレクトリ名/FrameWorksController@prologue');
```
