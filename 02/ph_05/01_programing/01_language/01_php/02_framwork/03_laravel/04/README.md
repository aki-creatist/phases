# ページネーション

## 1.ページネーションを使う

１ページに表示する制限数を定めることができる

表示制限を設定した場合、「表示できないページが出てきますが、「２ページ」「３ページ」とリンクが自動で生成されます。

この機能を「ページネーション」と呼んでいる

### 構文

ページネーション記述式

```php
モデル名::paginate( １ページあたりの表示数 );
```

ページネーション記述例

```php
$person = Person::paginate(3);
```

### コントローラの書き換え

app/Http/Controllers/PersonsController.php

```php
$persons = Person::orderBy('created_at', 'asc')->get();
↓
$persons = Person::orderBy('created_at', 'asc')->paginate(3);
```

### テンプレートに追加

ページャーの追加

```php
<div class="row">
    <div class="col-md-4 col-md-offset-4">
        {{ $persons->links()}}
    </div>
</div>
```
