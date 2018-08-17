# コントローラ

## HellosControllerクラスを作る

* i`ndex()`内はechoしたものがそのままサーバーからクライアント側へ出力
* レイアウトのON/OFF
* `$this`: このクラス`HellosController`のインスタンス

```bash
touch src/Controller/HellosController.php
```

```php
<?php
namespace App\Controller;

use App\Controller\AppController;

class HellosController extends AppController
{
    // アクションメソッド
    public function index()
    {
        $this->autoRender = false; //レンダリング機能を使わず、全てアクション内でページを作成する
        echo "<h1>Hello</h1>";
    }
}
```

```bash
open -a Google\ Chrome http://localhost/hellos
```

## テンプレートを作成する

```bash
touch Template/Hellos/index.ctp
```

```html
<!--Template/Hellos/index.ctp-->
<div>
    <h3>Index Page</h3>
    <p>This is sample.</p>
</div>
```

```php
public function index($a='')
{
}

public function err()
{
    $this->autoRender = false;
    echo '<p>パラメータがありませんでした。</p>;
}
```

```bash
open -a Google\ Chrome http://localhost/hellos
```


## HellosController.phpから値を渡す

```php
public function index()
{
    $this->set('message', 'Hello!');
}
```

```diff
  <h3>Index Page</h3>
- <p>This is sample.</p>
+ <p><?= $message ?></p>
```

## Formから値を受け取る

```diff
  <p><?= $message ?></p>
+ <form method="post" action="/hellos/index">
+     <input type="text" name="text1">
+     <input type="submit">
+ </form>
```

```diff
+ public function index()
+ {
+     $str = $this->request->data('text1');
+     if ($str != null) {
-         $this->set('message', 'Hello!');
+         $this->set('message','typed:' . $str);    
+     } else {
+         $this->set('message','not typed...');
+     }
+ }
```

## 動作確認

* フォームに何か書いて送信する
* 画面に`you typed:○○`という形で送信したテキストが表示される

## FormHelperを利用する

```diff
  <p><?= $message ?></p>
+ <?=$this->Form->create(null) ?>

+   <?=$this->Form->control('text1') ?>
+   <?=$this->Form->button(__('送信')) ?>
    
+ <?=$this->Form->end() ?>

+ debug($this->request->data);
```

## オプション設定

```diff
- <?=$this->Form->control('text1') ?>
+ <?=$this->Form->control('text1', ['label'=>'名前']) ?>
- <?=$this->Form->button(__('送信')) ?>
+ <?=$this->Form->button(__('送信'), ['class'=>'btn']) ?>
```

## Create()の第二引数を利用する

```diff
- <?=$this->Form->create(null) ?>
+ <?=$this->Form->create(null,[
+     'type' => 'post',
+     'url' => ['controller' => 'Hellos',
+         'action' => 'index']
+     ]
+ ) ?>
```

```php
public functon index()
{
    $str = $this->request->data('text1');
    $msg = 'typed: ' . $str;
    
    if ($str == null) $msg = "please type...";
    
    $this->set('message',$msg);
}
```