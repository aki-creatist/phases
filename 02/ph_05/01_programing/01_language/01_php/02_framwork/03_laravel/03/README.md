# テーブル作成

* テーブルはすでにDBの設定で作成した
* personsテーブルを使用する

```bash
php artisan make:model Person
```

* 順序を誤って、先にweb.phpやControllerでuse App¥Personとした場合には下記のようなエラーになる
* use文を一度コメントアウトしてから再実行する

```text
 [ErrorException]                                                     
  The use statement with non-compound name 'App¥Person' has no effect 
```

### スタブの追加

今回作成するルート定義は、先にスタブ(処理が空)のルートを定義していく

/routes/web.php

```php
<?php
use App\Person;
use Illuminate\Http\Request;

// ダッシュボード表示
Route::get('/', function () {
    return view('persons');
});

// person追加
Route::post('/persons', function (Request $request) {
    //
});

// person削除
Route::delete('/person/{person}', function (Person $person) {
    //
});
```

### レイアウトの作成

resources/views/Layout/default.php

```html
<!DOCTYPE html>
<html lang="ja">
    <head>
        <title>Person List</title>
    </head>


    <body>
        <div class="container">
            <nav class="navbar navbar-default">

            </nav>
        </div>


            @yield('content')

    </body>
</html>
```

### 画面の作成

```html
<!-- resources/views/persons.blade.php -->
@extends('Layout.default')

@section('content')
    
    <!-- Bootstrap の定形コード... -->
    
    <div class="panel-body">
        <!-- バリデーションエラーの表示に使用-->
        @include('common.errors')
        <!-- バリデーションエラーの表示に使用-->
        
        <!-- Person登録フォーム -->
        <form action="{{ url('persons') }}" method="POST" class="form-horizontal">
            {{ csrf_field() }}
            
            <!-- Personのタイトル -->
            <div class="form-group">
                <label for="person" class="col-sm-3 control-label">Person</label>
                
                <div class="col-sm-6">
                    <input type="text" name="item_name" id="person-name"class="form-control">
                </div>
            </div>
            
            <!-- Person 登録ボタン -->
            <div class="form-group">
                <div class="col-sm-offset-3 col-sm-6">
                    <button type="submit" class="btn btn-default">
                        <i class="fa fa-plus"></i> Save
                    </button>
                </div>
            </div>
        </form>
    </div>
    
    <!-- Person: 既に登録されてるPersonのリスト -->
@endsection
```

### エラー処理の記述

```html
<!-- resources/views/common/errors.blade.php -->

@if (count($errors) > 0)
    <!-- Form Error List -->
    <div class="alert alert-danger">
        <div><strong>入力した文字を修正。</strong></div> 
        <div>
            <ul>
            @foreach ($errors->all() as $error)
                <li>{{ $error }}</li>
            @endforeach
            </ul>
        </div>
    </div>
@endif
```

### バリデーションを作成

routes/web.phpに追記

```php
Route::post('/persons', function (Request $request) {
    // バリデーション
    $validator = Validator::make($request->all(), [
            // required = 必須　最小3字　最大255文字 パイプ( | )を挟むことで条件の追加が可能
            'person_name' => 'requred|min:3|max:255',
    ]);

    // バリデーションエラー
    if($validator->fails()) {
        return redirect('/')
            ->withInput()
            ->withErrors($validator);
    }
```

### インサート

```php
// Eloquentモデル
$persons = new Person;
var_dump($persons);
$persons->name = $request->name;
$persons->save();
```

下図のようにエラーが出る

[insert01](image/insert01.png)

* peopleというテーブルにnameの他にupdated_atとcreated_atというカラムに日付のデータを入れようとしている
* そもそもpersonsというテーブル自体どこで指定している
* その正体はPerson.phpをnew Personで呼び出した際に、FW側がスネークケース複数形に自動で変換している
* また、updated_atとcreated_atに入る時間は自動で挿入される
* Laravelが挿入しようとしている形に沿ってテーブルを作成することにする
* peopleテーブルの作成

```sql
CREATE TABLE people (
id INT UNSIGNED NOT NULL AUTO_INCREMENT,
name VARCHAR(20) NOT NULL,
updated_at datetime,
created_at datetime,
PRIMARY KEY( id )
);
```

* これで挿入ができるようになる
* MySQLで確認する

## 一覧画面

### 一覧データを取得し、viewへ渡す

routes/web.php

```php
Route::get('/', function () {
    $persons = Person::orderBy('created_at', 'asc')->get();

    // view関数は第二引数に、ビューで使用するデータを配列で受け付ける
    return view('persons',[
            // 配列のキーはビューの中で変数になる
            'persons' => $persons
    ]);
});
```

### 一覧表示

resources/views/perosons.blade.php

```html
<!-- Person: 既に登録されてるPersonのリスト -->
<!-- 現在 Persons -->
@if (count($persons) > 0)
    <div class="panel panel-default">
        <div class="panel-heading">
            現在 persons
        </div>
        <div class="panel-body">
            <table class="table table-striped task-table">
                <!-- テーブルヘッダ -->
                <thead>
                    <th>人一覧</th>
                    <th>&nbsp;</th>
                </thead>
                <!-- テーブル本体 -->
                <tbody>
                    @foreach ($persons as $person)
                        <tr>
                            <!-- 名前 -->
                            <td class="table-text">
                                <div>{{ $person->name }}</div>
                            </td>

                            <!-- 人: 削除ボタン -->
                            <td>

                            </td>
                        </tr>
                    @endforeach
                </tbody>
            </table>
        </div>
    </div>
@endif
```

## Bladeのテンプレートの制御構文

* Bladeテンプレートは`@extends`、`@section`、`@include`以外の制御構文を用意
* `@`を先頭につけた短縮系の記述で、`{ ... }`を使用しない

分岐処理

```html
@if (count ($persons) == 1)
    人が一人いる！
@endif
```

多分岐処理

```html
@if (count($persons) = 1)
    人が一人いる
@elseif (count($persons) > 1)
    人が２人以上いる
@else
    人が全くいない
@endif

```

反復処理(インデックス)

```html
@for ($i = 0; $i>10; $i++)
    現在のCOUNT : {{ $i }}
@endfor
```

反復処理(配列||連想配列||オブジェクト

```html
@foreach ($persons as $person)
    <p>名前 : {{ $person->name }}</p>
@endforeach
```

反復処理(配列||連想配列||オブジェクト

```html
@forelse ($persons as $person)
    <li>名前 : {{ $person->name }}</li>
@empty
    <li>誰もいません</li>
@endforelse
```

条件式が偽(False)の場合の処理

```html

@unless (Auth::check())
    ログインしていません
@endunless
```

条件式が偽(False||True)の場合の処理

```html
@unless(Auth::check())
    ログインしていません
@else
    ログインしています
@endunless
```

## 削除

### 削除ボタンの追加

resources/views/persons.blade.php

```html
<td>
    <form action="{{ url('person/' .$person->id) }}" method="POST">
        {{ csrf_field() }}
        {{ method_field('DELETE') }}

        <button type="submit" class="btn btn-danger">
            <i class="fa fa-trash"></i>削除
        </button>
    </form>
</td>
```

### 削除処理

* クリックしたデータを削除する
* ロジックをルートへ追加する
    * `{person}`ルートパラメータに対応するPersonモデルを自動的に取得するため、
* 暗黙のモデル結合が使用可能

routes/web.php

```php
// person削除
Route::delete('/person/{person}', function (Person $person) {
    $person->delete();
    return redirect('/');
});
```

#### 擬似的メソッド

擬似的メソッド

```html
{{ method_field('DELETE') }}
```

* 定義しているルートはRoute::deleteである点に注意
    * 削除ボタンフォームのmethodがPOSTを使用しているのに関わらず
* HTMLのフォームはGETとPOSTのみが許可されている
    * そのため、フォームDELETEリクエストを使う場合は、擬似的に使える方法がある
* フォームの中でmethod_field('DELETE')関数の結果を出力することにより、DELETEリクエストに見せかけることが可能
* Laravelはこれを認識し、実際のHTTPリクエストメソッドをオーバーライドする生成されるフィールドは次の内容

```html
<!--生成されるHTM-->
<input type="hidden" name="_method" value="DELETE">
```

#### CSRFからの保護

CSRFからの保護

```html
{{ csrf_field() }}
```

* CSRFはユーザーになり代わり悪意のある操作をするハッキング手法の一つ
* LaravelにはCSRFからアプリケーションを簡単に守るためのヘルパー関数が用意されている
* 基本的にはログイン認証後などのフォームには必須の記述のため『常に記述する』という感覚で構わない

### Bootstrapの読み込み

resources/views/Layout/default.blade.php

```html
<head>
    <title>Person List</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

    <!-- Optional theme -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">

    <!-- Latest compiled and minified JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>

</head>
```

## 更新処理

routes/web.php

```php
//更新画面
Route::post('/personsedit/{persons}', function(Person $persons) {
    //{persons}id 値を取得 => Person $persons id 値の1レコード取得
    return view('personsedit', ['person' => $persons]);
});

//更新処理
Route::post('/persons/update', function(Request $request){
    //バリデーション
    $validator = Validator::make($request->all(), [
            'id' => 'required',
            'name' => 'required|min:3|max:255',
    ]);
    //バリデーション:エラー
    if ($validator->fails()) {
        return redirect('/')
        ->withInput()
        ->withErrors($validator);
    }
    
    //データ更新
    $persons = Person::find($request->id);
    $persons->item_name   = $request->name;
    $persons->save();
    return redirect('/');
});
```

### 更新ボタンの追加

```html
<!-- 人: 更新ボタン -->
<td>
    <!-- url関数内で'personsedit/'のURL文字列にid値のパラメータを持たせることで、
    ルーティング定義Route::post('/personsedit/{persons}との関係を作成する -->
    <form action="{{ url('personsedit/'.$person->id) }}" method="POST">
        {{ csrf_field() }}
        <button type="submit" class="btn btn-primary">
            <i class="glyphicon glyphicon-trash"></i> 更新
        </button>
    </form>
</td>

```

## updateをコントローラに移行

### コントローラ作成

```bash
php artisan make:controller PersonsController
```

### スタブの作成

app/Http/Controllers/PersonsController.phpにスタブ作成

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

use App\Book;
use Validator;

class PersonsController extends Controller
{
    public function update(Request $request)
    {
        // 
    }
}
```

### web.phpから処理を切り出す

```php
routes/web.phpの更新処理の以下の部分を切り取る
<pre class="brush:php; toolbar:false gutter:false" title="">
//バリデーション 
$validator = Validator::make($request->all(), [
        'id' => 'required',
        'name' => 'required|min:3|max:255',
]);
//バリデーション:エラー
if ($validator->fails()) {
    return redirect('/')
    ->withInput()
    ->withErrors($validator);
}

//データ更新
$persons = Person::find($request->id);
$persons->name   = $request->name;
$persons->save();
return redirect('/');
```

### コントローラに移行する

切り取った箇所をapp/Http/Controllers/PersonsController.phpに貼り付ける

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

use App\Person;
use Validator;

class PersonsController extends Controller
{
    public function update(Request $request)
    {
        //バリデーション
        $validator = Validator::make($request->all(), [
                'id' => 'required',
                'name' => 'required|min:3|max:255',
        ]);
        //バリデーション:エラー
        if ($validator->fails()) {
            return redirect('/')
            ->withInput()
            ->withErrors($validator);
        }

        //データ更新
        $persons = Person::find($request->id);
        $persons->name   = $request->name;
        $persons->save();
        return redirect('/');
    }
}
```

### web.phpの書き換え

routes/web.phpの修正

```php
//更新処理
Route::post('/persons/update', function(Request $request){

});
↓以下に書き換え
Route::post('/persons/update', 'PersonsController@update');
```

## store(登録処理)をコントローラに移行

### コントローラにスタブの追加

app/Http/Controllers/PersonsController.php

```php
public function store(Request $request)
{
    //
}
```


### web.phpの登録処理を切り取る

routes/web.php

```php
// person追加
Route::post('/persons', function (Request $request) {

});
```

web.phpから切り取った処理

```php
// バリデーション
$validator = Validator::make($request->all(), [
        // required = 必須　最小3字　最大255文字 パイプ( | )を挟むことで条件の追加が可能
        // キーは自由に設定できる。エラー時にはThe name field is required.と表示される
        'name' => 'required|min:3|max:255',
]);

// バリデーションエラーの場合、セッションに値を保存し、ユーザーをルートURLへリダイレクトする
if($validator->fails()) {
    // ルートURL(/)へリダイレクト
    return redirect('/')
        ->withInput()    // セッションに値を保存
        /*
         * 指定されたvalidatorインスタンスのエラーをフラッシュデータとしてセッションに保存し
         * ビューの中で$errorsとしてアクセスできるようにする
         * フォームのバリデーションを表示するためにerrors.blade.phpで使用する
         */
        ->withErrors($validator);
}

// Eloquentモデル
$persons = new Person;    // Person.phpの呼び出し
$persons->name = $request->name;
$persons->save();        // 保存
return redirect('/');    // ルートにリダイレクト
```

### コントローラに移行する

app/Http/Controllers/PersonsController.phpに移行

```php
    public function store(Request $request)
    {
        // バリデーション
        $validator = Validator::make($request->all(), [
                // required = 必須　最小3字　最大255文字 パイプ( | )を挟むことで条件の追加が可能
                // キーは自由に設定できる。エラー時にはThe name field is required.と表示される
                'name' => 'required|min:3|max:255',
        ]);
        
        // バリデーションエラーの場合、セッションに値を保存し、ユーザーをルートURLへリダイレクトする
        if($validator->fails()) {
            // ルートURL(/)へリダイレクト
            return redirect('/')
            ->withInput()    // セッションに値を保存
            /*
             * 指定されたvalidatorインスタンスのエラーをフラッシュデータとしてセッションに保存し
             * ビューの中で$errorsとしてアクセスできるようにする
             * フォームのバリデーションを表示するためにerrors.blade.phpで使用する
             */
            ->withErrors($validator);
        }
        
        // Eloquentモデル
        $persons = new Person;    // Person.phpの呼び出し
        $persons->name = $request->name;
        $persons->save();        // 保存
        return redirect('/');    // ルートにリダイレクト
    }
}

```

### web.phpの書き換え

```diff
- Route::post('/persons', function (Request $request) {
+ Route::post('/persons', 'PersonsController@store');
```

## ルート定義をコントローラに移行

### コントローラにスタブの追加

app/Http/Controllers/PersonsController.php

```php
public function index()
{
    //
}
```

### web.phpの処理を切り取る

routes/web.php

```php
// ダッシュボード表示
Route::get('/', function () {

});
```

web.phpから切り取った処理

```php
$persons = Person::orderBy('created_at', 'asc')->get();

// view関数は第二引数に、ビューで使用するデータを配列で受け付ける
return view('persons',[
        // 配列のキーはビューの中で変数になる
        'persons' => $persons
]);
```

### コントローラに移行する

app/Http/Controllers/PersonsController.php

```php
public function index()
{
    $persons = Person::orderBy('created_at', 'asc')->get();

    // view関数は第二引数に、ビューで使用するデータを配列で受け付ける
    return view('persons',[
            // 配列のキーはビューの中で変数になる
            'persons' => $persons
    ]);
}
```

### ルート定義を変更

routes/web.phpのルート定義を書き換え

```php
// ダッシュボード表示
Route::get('/', function () {

});
↓下記のように書き換え
Route::get('/', 'PersonsController@index');
```

### use Illuminate\Http\Request;を削除

web.phpの下記の部分は不要になるので削除する

```php
use Illuminate\Http\Request;
```


## edit(変更処理)をコントローラに移行する

### コントローラにスタブを追加する

app/Http/Controllers/PersonsController.phpにスタブを追加

```php
// 更新画面
public function edit(Person $persons)
{
    //
}
```

### web.phpから処理を切り取る

routes/web.phpから処理を切り取る

```php
//更新画面
Route::post('/personsedit/{persons}', function(Person $persons) {

});
```

切り取った処理

```php
//{persons}id 値を取得 => Person $persons id 値の1レコード取得
return view('personsedit', ['person' => $persons]);
```

### コントローラに貼り付ける

app/Http/Controllers/PersonsController.php

```php
// 更新画面
public function edit(Person $persons)
{
    //{persons}id 値を取得 => Person $persons id 値の1レコード取得
    return view('personsedit', ['person' => $persons]);
}
```

### ルート定義の変更

routes/web.phpのルート定義を書き換え

```php
//更新画面
Route::post('/personsedit/{persons}', function(Person $persons) {

});
↓以下に変更
//更新画面
Route::post('/personsedit/{persons}', 'PersonsController@edit');
```

## delete(削除処理)をコントローラに移行する

### コントローラにスタブを追加する

app/Http/Controllers/PersonsController.phpにスタブを追加

```php
// 削除処理
public function destroy(Person $person)
{
    //
}
```

### web.phpの処理を切り取る

routes/web.php

```php
// person削除
Route::delete('/person/{person}', function (Person $person) {

});
```

切り取った処理

```php
$person->delete();
return redirect('/');
```

### コントローラに貼り付ける

app/Http/Controllers/PersonsController.php

```php
// 削除処理
public function destroy(Person $person)
{
    $person->delete();
    return redirect('/');
}
```

### ルート定義の変更

routes/web.phpのルート定義を書き換え

```php
// person削除
Route::delete('/person/{person}', function (Person $person) {

});
//↓下記に書き換え
Route::delete('/person/{person}', 'PersonsController@destroy');
```
