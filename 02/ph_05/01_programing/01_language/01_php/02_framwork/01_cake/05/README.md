# ページネーション

多量のデータを一定数ごとに切り分けて表示するために用意されているのが、`ページネーション`という機能

## ページネーションとPaginator

* 多量のデータを表示時にページ分けをし、１ページずつ表示する

## ソース

```php
<?php
//Controller/PersonsController.php
namespace App/Controller;

use App/Controller/AppController;
ues Cake/Datasource/ConnectionManager;

class PersonsController extends AppController
{
    public $paginate = [    // paginateプロパティを用意し、設定を行う
        'limit' => 5,       // １ページあたりの表示数を`５`に設定
        'order' => [        // nameフィールドを使って昇順にエンティティを並べ替える
            'Persons.name' => 'asc' // orderのフィールド名は、`クラス.プロパティ`という形で記述
        ]
    ];
    
    public function initialize()
    {
        parent::initialize();       // スーパークラスのinitializeを呼び出し
        $this->loadComponent('Paginator'); // Paginartorコンポーネントのロード
    }
    
    public function index()
    {
        $persons = $this->paginate();   // 表示するエンティティの取得を行なう
        $this->set('persons', $persons);// テンプレート側にセットする
        
        //$this->set('persons', $this->paginate()); //一行にまとめてしまってもOK
    }
}
```

* Template/Element/にpagination.ctp

```html
<!--Template/Element/pagination.ctp-->
<ul class="pagination">
    <?php echo $this->Paginator->prev(__('<<'), array('tag' => 'li'), null, array('tag' => 'li','class' => 'disabled','disabledTag' => 'a')); ?>
    <?php echo @$this->Paginator->numbers(array('separator' => '', 'currentTag' => 'a', 'currentClass' => 'active', 'tag' => 'li')); ?>
    <?php echo $this->Paginator->next(__('>>'), array('tag' => 'li','currentClass' => 'disabled'), null, array('tag' => 'li','class' => 'disabled','disabledTag' => 'a')); ?>
</ul>
```

```php
<!--Template/Persons/index.ctp-->
<div>
    <h3>List Persons</h3>
    <?= $this->element('pagination'); ?>
    <table>
    <thead>
        <tr>
            <th>ID</th>
            <th>NAME</th>
            <th>AGE</th>
            <th>MAIL</th>
        </tr>
    </thead>
    <tbody>
    <?php foreach ($persons as $person): ?>
        <tr>
            <td><?= h($person->id) ?></td>
            <td><?= h($person->name) ?></td>
            <td><?= h($person->age) ?></td>
            <td><?= h($person->mail) ?></td>
        </tr>
    <?php endforeach; ?>
    </tbody>
    </table>
</div>
```

## Paginatorヘルパー・テンプレート

### Viewファイルを用意

```diff
      <h3>List Persons</h3>
+ <?php
+ if($this->Paginator->first('<<first') !==''){
+     echo $this->Paginator->first('<<first');
+ }else{
+     // &amp;lt;としないと<がタグとして認識され、動作不具合となる
+     echo &quot;&amp;lt;&amp;lt;first&quot;;
+ }
+ ?>
+ <?= $this->Paginator->prev('<prev'); ?>
+ <?= $this->Paginator->numbers(); ?>
+ <?= $this->Paginator->next('next>'); ?>
+ <?php
+ if($this->Paginator->last('last>>') !==''){
+     echo $this->Paginator->last('last>>');
+ }else{
+     // &amp;lt;としないと<がタグとして認識され、動作不具合となる
+     echo &quot;last&amp;gt;&amp;gt;;
+ }
+ ?>    
```

### テンプレートの読み込み

```diff
  class PersonsController extends AppController
  {
+     public $helpers = ['Paginator' => ['templates' => 'paginator-templates'] ];

      public $paginate = [
```

### テンプレートファイルの作成

```php
<?php
//config/paginator-templates.php
<?php
return [
    /* 前ページ用リンク */    
    // 前ページリンクがアクティブ(使える)とき
    'prevActive' => '<span class="prev"><a rel="prev" href="{{url}}">{{text}}</a></span> | ',
    // 前ページリンクが非アクティブ(リンクが不要)なとき
    'prevDisabled' => '<span class="disabled">{{text}}</span> | ',
    
    /* 次ページ用リンク */    
    // 次ページリンクがアクティブ(使える)なとき
    'nextActive' => '<span class="next"><a rel="next" href="{{url}}">{{text}}</a></span>',
    // 次ページリンクが非アクティブ(不要)なとき
    'nextDisabled' => '<span class="disabled">{{text}}</span> | ',
    
    /* 最初と最後へのジャンプ */    
    // 最初のページ用のリンク
    'first' => '<span class="first"><a rel="first" href="{{url}}">{{text}}</a></span> | ',
    
    // 最後のページ用のリンク
    'last' => '<span class="last"><a rel="last" href="{{url}}">{{text}}</a></span>',
    
    /* ページ番号 */    
    // ページ番号のリンク
    'number' => '<span><a href="{{url}}">{{text}}</a></span> |',
    
    // 現在表示しているページ番号
    'current' =>'<span class="current">{{text}}</span> |',
];
```

### 全件数表示

```php
//全件数
<?= $this->Paginator->counter(['format'=>'全{{count}}件']); ?>
//表示件数
<?= $this->Paginator->counter(['{{start}}〜{{end}}件']); ?>
```