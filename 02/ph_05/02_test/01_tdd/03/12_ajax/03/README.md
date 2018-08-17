# XMLHttpRequestオブジェクトのスタブを使う

* `get()`が動作する際には、`XMLHttpRequest`オブジェクトを作る必要がある
* 単純に`get()`に`ajax.create`を使ってオブジェクトを作らせればよい
    * こうすると、要求APIと作成APIの間にちょっとした密結合が生まれることに注意
    * おそらく、トランスポートオブジェクトを注入したほうがよいが、今の段階では単純にしておく
        * 後で大きな構図がより鮮明に見えてからでもリファクタリング可能
* メソッドが呼び出されたら、本来の実装をフェイクしなければならない
* 本物のオブジェクトをまねるオブジェクトを作る2つの方法
    * スタブ
    * モック
* `フェイク`、`ダミー`とともに、これらは集合的に**テストダブル**と呼ばれる
    * テストダブル: 本来の実装が使いにくいときや、依存ファイルからインターフェイスを切り離したいときに使用する

## 手作業によるスタブ化

* XMLHttpRequest
    * 本来の実装が使いにくい
    * 依存ファイルからインターフェイスを切り離したい
* `ceate()`を手作業でスタブに置き換える
    * テストの動作
        * もとのメソッドの参照を保存
        * 呼び出されたらテストがアサートできるフラグを設定するスタブ関数で上書き
        * 最後にもとのメソッドを復元する

```javascript
"test should obtain an XMLHttpRequest object": function () {
    var originalCreate = ajax.create;
    
    ajax.create = function () { // 本物のオブジェクトを作る代わりに、ajax.createをスタブに置き換え
        ajax.create.called = true;
    };    
    ajax.get("/url");           // ajax.getを呼び出し
    assert(ajax.create.called); // ajax.createが呼び出されていることをアサート
    ajax.create = originalCreate;
}
```

* この方法には2つの問題点がある
    * テストが不合格になると、もとのメソッドが復元されなくなる
        * アサートは、テストが成功しない限り、最後の行は実行されない
            * 失敗するとAssertError例外を投げるため
        * この問題は、もとのメソッドの参照の保存、復元をそれぞれ`setUp()`、`tearDown()`に移動すれば解決
    * 冗長なこと
        * 解決手順
            * 呼び出されたらフラグをセットする関数を作るヘルパーメソッドを抽出する
            * このフラグにアクセス可能にする
* ajax.createを安全にスタブに置き換え、復元する

```javascript
TestCase("GetRequestTest",{
    setUp: function() {
        this.ajaxCreate = ajax.create;
    }
    
    tearDown: function () {
        ajax.create = this.ajaxCreate;
    },
    
    /* ... */
    
    "test should obtain an XMLHttpRequest object":
    function () {
        ajax.create = function () {
            ajax.create.called = true;
        };
    
        ajax.get("/url");
    
        assert(ajax.create.called);
    }
});
```

* 次の問題を解決する前に、問題のメソッドを実装しなければならない
* ajax.getのなかにオブジェクトを作るコードを1行追加するだけでよい
* [src/request.js#87](../src/request.js#87)
* この1行を追加すると、テストは再び緑に戻る