# ビュー( レイアウト・テンプレート )
        
## 置き場所

* resources/views/配下に配置する
* 画面の表示は`ビュー`担当するあらかじめ用意しておいたテンプレートを使う
* 必要な値をコントローラーから受け渡ししながら処理していく

## View層の全体

* MVCモデルでは画面表示のためのテンプレートをあらかじめ用意
* それをロードして表示するのが基本

## 1.テンプレートの定義

* Laravelではテンプレートエンジン`Bladeテンプレート`を使用する
* パーツ化せずに使うことも可能
* Bladeテンプレートはベースのテンプレートとパーツを組み合わせ表示
* テンプレート上でif条件分岐することも可能
* そのような制御構文も用意してあり、高機能なテンプレート

#### .blade.php 拡張子

* ビュー表示時にFWへ`Bladeテンプレートエンジン`を使用して表示することを知らせる拡張子
* 必ずファイル名の後に` .blade.php`を付ける
* これでフレームワークがテンプレートだと認識するようになる

### ビュー設置箇所

* Laravelのすべてのビューは、`resources/views/`配下に設置する
* 新しいレイアウトビューも`resources/views`の中に新しく`layouts`フォルダを作成
* その中に`default.blade.php`を作成する
* /resources/views/layouts/default.blade.phpとなる

## 2.テンプレートとレイアウトの親子関係

テンプレートは、親と子に分けられる

* コントローラから指定して最初に呼び出されるのが`子テンプレート`
* .blade.phpから`@extends()`で読み込まれるのが`親テンプレート`


## レイアウトの作成

レイアウトは以下のようにして作成する

```html
<!-- resources/views/layouts/default.blade.php -->

<!DOCTYPE html>
<html lang="ja">
    <head>
        <title>Code</title>

        <!-- CSS と JavaScript -->
    </head>

    <body>
        <div class="container">
            <nav class="navbar navbar-default">
            <!-- ナビバーの内容 -->
            </nav>
        </div>

        @yield('content')
    </body>
</html>
```

レイアウトの`@yield('content')`
    * パーツ配置キーワード共有パーツの`子テンプレート`を`親テンプレート( default.blade.php )`へ配置指定するために使用される

### 3.テンプレートの定義

```html
<!-- resources/views/index.blade.php -->

@extends('layouts.default')

@section('content')
    
    <!-- Bootstrap の定形コード... -->
    
    <div class="panel-body">
        <h1></h1>hello</h1>        
    </div>
    
@endsection
```

続いてコントローラを下記のように編集し、http://localhost:8000/hellosにアクセスする

```php
<?php
///resources/views/hello.blade.php
use Illuminate\Http\Request; 

Route::get('/hellos', function () {
    return view('index);
});
```

#### @extendsディレクティブ( 親テンプレート読み込み )

* `@extends('layouts.default')で親テンプレートを読み込む
* layout.defaultはlayouts/defaultと同意
* `.`は `/`と解釈される
* つまり、親テンプレート`resources/view/layouts/default.blade.php`を読み込むという意味になる

#### @sectionディレクティブ( 名前をつけて一括りにする )

* `@section('content')`から`@endsection`の間の文字/HTMLなどをcontentにくくっている
* 親テンプレート`@yield('content')の`箇所にcontentを挿入する
* 例: contentの箇所は任意で名前をつけられる

#### @includeディレクティブ

* `@include`はPHPで使用する`include`と同じ使い方が可能
* `@include`('ディレクトリ名.ファイル名')を記述した箇所に挿入する

#### Blade内の変数表示

テンプレート内では、`<?php echo $変数名; ?>`ではなく、`{{$変数名}}`で記述可能

#### エスケープ

* `{{ $変数名 }}`
    * エスケープあり
* `{{!! $変数名 !!}}`
    * エスケープなし
* Bladeテンプレートでは`{{ $変数名 }}`を使用時、PHPのエスケープ関数を自動的に通して表示する
    * XSS攻撃を防ぐために、
* 理由がありエスケープしたくない場合には、`{{!!$変数名!!}}`を使用することが可能
* しかし、セキュリティを考慮すると基本は`{{$変数名}}`を使用する

#### 変数表示の切り分け

```php
{{ $name or 'Default' }}
```

* この例の場合、$nameが存在する場合
* * 値が表示されるしかし存在していなければDefaultとう言葉が表示される

#### BladeとJSフレームワーク

* Bladeテンプレートで`{{$変数}}`を使用している
* JSフレームワークでも{{ 変数名 }}を利用するJSフレームワークがある
* その場合の対処方法として、`@`を`{{ 変数 }}`の頭につける
    * `@`の後ろが変数として処理せずに`{{ 変数名 }}`を残してくれる
* つまりはJSの変数としてその記述を変換せずに処理する

```html
@{{ name }} //JSとの書き分け
```

### JSとCSSの配置場所

* publicフォルダ内の`assets/js/`や`assets/css/`に配置する
    * デフォルトでは`asset()`を使用する
* `asset()`: `/public`以下を参照する

### 外部ファイルを読み込み

public/assets/js/xxx.js

```html
<script src="{asset('/assets/js/jquery.min.js')}}"></script>
<script src="{asset('/assets/js/bootstrap.min.js')}}"></script>
```

public/assets/css/xxx.css

```html
<link href="{{asset('/assets/css/bootstrap.min.css')}}" rel="stylesheet">
<link href="{{asset('/assets/css/style.min.css')}}" rel="stylesheet">
```

## 画面のキャッシュのクリア

```bash
php artisan view:clear
```