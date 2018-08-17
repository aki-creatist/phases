# Laravel

```bash
#Modelの作成
php artisan make:model MeetingRooms
#Model created successfully.
php artisan make:model Meeting
#Model created successfully.
php artisan make:model MeetingsMember
#Model created successfully.
php artisan make:model Member
#Model created successfully.
```

* モデル名を指定しないと以下のようなエラーになる

```text
  [Symfony\Component\Console\Exception\RuntimeException] 
  Not enough arguments (missing: "name").
```

* [app/MeetingRoom.php](https://github.com/aki-creatist/Laravel5/blob/develop/app/MeetingRoom.php)
* [app/Meeting.php](https://github.com/aki-creatist/Laravel5/blob/develop/app/Meeting.php)
* [app/MeetingsMember.php](https://github.com/aki-creatist/Laravel5/blob/develop/app/MeetingsMember.php)
* [app/Member.php](https://github.com/aki-creatist/Laravel5/blob/develop/app/Member.php)

```bash
php artisan make:controller MeetingRoomsController
#Controller created successfully.
php artisan make:controller MeetingsController
#Controller created successfully.
php artisan make:controller MembersController
#Controller created successfully.
```

* [app/Http/Controllers/MeetingRoomsController.php](https://github.com/aki-creatist/Laravel5/blob/develop/app/Http/Controllers/MeetingRoomsController.php)
* [app/Http/Controllers/MeetingsController.php](https://github.com/aki-creatist/Laravel5/blob/develop/app/Http/Controllers/MeetingsController.php)
* [app/Http/Controllers/MembersController.php](https://github.com/aki-creatist/Laravel5/blob/develop/app/Http/Controllers/MembersController.php)

```bash
#resources/views/MeetingRooms/index.phpの作成
mkdir resources/views/MeetingRooms
vim resources/views/MeetingRooms/index.blade.php
```

resources/views/MeetingRooms/index.blade.phpに以下の内容を貼り付ける

```html
@extends('Layout.default')

@section('content')

    <div class="panel-body">


    </div>

@endsection
```

```bash
#index.phpをコピーしてCRUD画面を作成
cp resources/views/MeetingRooms/index.blade.php resources/views/MeetingRooms/view.bladephp
cp resources/views/MeetingRooms/index.blade.php resources/views/MeetingRooms/add.blade.php
cp resources/views/MeetingRooms/index.bladephp resources/views/MeetingRooms/edit.blade.php
```

```bash
#MeetingRoomsディレクトリを複製する
cp -R resources/views/MeetingRooms resources/views/Meetings
cp -R resources/views/MeetingRooms resources/views/Members
```
