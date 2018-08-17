# 一覧表示

## 1.一覧データを取得し、viewへ変数を渡す

* 最初に` / `ルート定義内を編集
* 既存のデータ全てをビューに渡す
* view関数は第２引数に、ビューで使用するデータを配列データを配列で受け付ける
* 配列のキーはビューの中で変数となる

```php
// /routes/web.php
Routes::get('/', function() {
    $persons = Person::orderBy('id', 'asc')->get();
    return view('persons', [
        ''persons' => $persons
    ]);
});
```

* view関数に配列データを渡す
* `persons.blade.php`ビューの中で反復処理を行う
* HTMLテーブル要素を作成して表示する反復処理は@foreachを使用
* Blade構文で簡単にループ記述可能
* `@if`,`@for`,`@unless`,`@empty`,`@while`なども使用可能

## 2.@foreach

* `@foreach`を使い`$persons`の値を`$person`に代入して表示する

### 追加処理

### 1.フォームの作成

## ルート定義とコントローラ

* コントローラを使用せずにルート定義に記述して完結することも可能
* しかし、ルーティングが増えた場合にはコードの視認性が悪くなる
* MVCの観点からもルート定義以外の`書く処理のコードはコントローラに移行する
* 書く処理とは、特定のデータ１つを取得したり、保存したりする処理新しく作る
* コントローラは`app/Http/Controllers`ディレクトリに新規作成・配置する
* artisanコマンドを使用する

### コントローラ( Controllers )ディレクトリ

コントローラは/app/Http/Controllers/以下に配置する

#### ルーティング・コントローラ・ビューの流れ

```php
//ルーティング： /routes/web.php
Routes::get('/persons, 'PersonsController@index');
```

```php
//コントローラ： /app/Http/Controller/PersonsController.php
public function index(){
    return view('persons');
}
```

```php
//ビュー：/resouces/views/index.blade.php
@extends('layouts.default')

@section('title')
    一覧表示
@endsection
```

#### Controllerの作成

```bash
php artisan make:controller コントローラ名
```

* 全LaravelコントローラはLaravelに含まれている基本コントローラクラスを継承して使用する
* Personsコントローラが作成

```bash
php artisan make:controller Persons
```

app/Http/Controllers/以下にコントローラが作成できていることを確認する。

### 2.新規作成したコントローラファイルのコードを確認する

```php
<?php
//app/Http/Controllers/PersonsController.php
namespace App¥Http¥Controllers;

use Illuminate¥Http¥Request;

class PersonsController extends Controller
{

}
```

* 上記ファイル`PersonsController.php`で使用するため、`他のクラス`２つを読み込む
* use App¥Person;
* use App¥Validator;
* 下記は`他のクラス`２つを読み込んだコード

```php
<?php
//２つのクラスの読み込み
namespace App¥Http¥Controllers;

use Illuminate¥Http¥Request;
use App¥Person;
use App¥Validator;

class PersonsController extends Controller
{

}
```

### 3.コントローラにupdate()を追加

* `update()`をスタブにする
* `update()`の引数では`Requestパラメータ`を取得
* メソッド内でRequestパラメータを処理するまた`更新処理`は後ほど追加記述する

```php
<?php
//２つのクラスの読み込み
namespace App¥Http¥Controllers;

use Illuminate¥Http¥Request;
use App¥Person;
use App¥Validator;

class PersonsController extends Controller
{
    // 更新
    public function update(Request $request)
    {
    
    }
}
```

### 4.更新処理の記述

```php
<?php
//２つのクラスの読み込み
namespace App¥Http¥Controllers;

use Illuminate¥Http¥Request;
use App¥Person;
use App¥Validator;

class PersonsController extends Controller
{
    // 更新
    public function update(Request $request)
    {
        // バリデーション
        $validator = Validator::make($request->all(), [
            'id' => 'required',
            'name' => 'required|min:3|max:255
        ]);
        // バリデーション：エラー
        if ($validator->fails()) {
            return redirect('/')
                ->withInput()
                ->withErrors($validator);
        }
        $persons = Person::find($request->id);
        $persons->name = $request->name;
        $persons->save();
        return redirect('/');
    }
}
```
