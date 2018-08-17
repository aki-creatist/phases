# 準備

* [ルーティング](01)
* [ソースの生成](02)
* [フォームヘルパー](03)

## 開発用サーバーで実行する

```bash
#サーバを立ち上げる - Laravel
php artisan serve
open -a Google\ Chrome http://localhost:8000
```

```bash
#サーバーを立ち上げる - CakePHP
bin/cake server
open -a Google\ Chrome http://localhost:8765
```

## ディレクトリ構成

* [Laravel](https://github.com/aki-creatist/Laravel5)
* [cakePHP2](https://github.com/aki-creatist/CakePHP2)
* [cakePHP3](https://github.com/aki-creatist/CakePHP3)
    * クラスファイル名とクラスファイルを配置するフォルダ名は`キャメルケース`
    * それ以外のファイル名とフォルダ名は`スネークケース`

## 公式

タイムゾーンに関する解説は[公式ページ](https://book.cakephp.org/3.0/ja/core-libraries/time.html)

### ディレクトリ構成の変更

* publicの移動
    * config/app.phpを修正

```diff
// Laravelプロジェクト本体の名前がlaravelの場合
- require __DIR__.'/../bootstrap/autoload.php';
+ require __DIR__.'/../laravel/bootstrap/autoload.php';

- $app = require_once __DIR__.'/../bootstrap/app.php';
+ $app = require_once __DIR__.'/../laravel/bootstrap/app.php';
```