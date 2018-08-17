# Laravel

* [ビュー](01)
* [一覧表示](02)
* [テーブル作成](03)
* [ページネーション](04)
* [ログイン認証](05)
* [Modelチェック](06)
* [CRUD自動生成](07)
* [デバッグバー](08)
* [処理の作成の流れ](09)
* [暗号化](10)

## 会議室予約システム

### routes/web.php

```php
Route::get('/meeting-rooms/','MeetingRoomsController@index');
Route::get('/meeting-rooms/view','MeetingRoomsController@view');
Route::get('/meeting-rooms/add','MeetingRoomsController@add');
Route::get('/meeting-rooms/edit','MeetingRoomsController@edit');

Route::get('/meetings/','MeetingsController@index');
Route::get('/meetings/view','MeetingsController@view');
Route::get('/meetings/add','MeetingsController@add');
Route::get('/meetings/edit','MeetingsController@edit');

Route::get('/members/','MeetingMembersController@index');
Route::get('/members/view','MeetingMembersController@view');
Route::get('/members/add','MeetingMembersController@add');
Route::get('/members/edit','MeetingMembersController@edit');
```

### app/Http/Controllers/MeetingRoomsController.php

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class MeetingRoomsController extends Controller
{
    
    public function index(Request $request) {
        return view('MeetingRooms/index');
    }
    
    public function view(Request $request) {
        return view('MeetingRooms/view');
    }
    
    public function add(Request $request) {
        return add('MeetingRooms/add');
    }
    
    public function edit(Request $request) {
        return edit('MeetingRooms/edit');
    }
}
```

### app/Http/Controllers/MeetingsController.php

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class MeetingsController extends Controller
{

    public function index(Request $request) {
        return view('Meetings/index');
    }
    
    public function view(Request $request) {
        return view('Meetings/view');
    }
    
    public function add(Request $request) {
        return add('Meetings/add');
    }
    
    public function edit(Request $request) {
        return edit('Meetings/edit');
    }
}
```

### app/Http/Controllers/MembersController.php

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class MembersController extends Controller
{
    
    public function index(Request $request) {
        return view('Members/index');
    }
    
    public function view(Request $request) {
        return view('Members/view');
    }
    
    public function add(Request $request) {
        return add('Members/add');
    }
    
    public function edit(Request $request) {
        return edit('Members/edit');
    }
}
```

### resources/view/Layout/ディレクトリの作成

```bash
mkdir resources/views/Layout
vim resources/views/Layout/default.blade.php
```

### resources/view/Layout/default.blade.php

```html
<!-- resources/views/Layout/default.blade.php -->

<!DOCTYPE html>
<html lang="ja">
    <head>
        <title></title>
    </head>

    <header>
    @include('Element.topbar')
    @include('Element.sidebar')
    </header>

    <body>
        <main>
        
            <div class="container">
            @yield('content')
            </div>
        
        </main>
        
        <footer>
        </footer>
        
    </body>
</html>
```

### resources/view/Elementの作成

```bash
mkdir resources/views/Element
```

### resources/view/Element/topbar.blade.phpを開く

```bash
vim resources/views/Element/topbar.blade.php
```

### resources/view/Element/topbar.blade.php

```bash
<!-- resources/views/Element/topbar.blade.php -->
```

### resources/view/Element/sidebar.blade.phpを開く

```bash
vim resources/views/Element/sidebar.blade.php
```

### resources/view/Element/sidebar.blade.php

```bash
<!-- resources/views/Element/sidebar.blade.php -->
```
