# イテレータ

* コレクションオブジェクトの反復処理をカプセル化するオブジェクト
* あらゆるタイプのコレクションを反復処理できる首尾一貫したAPIを提供
    * 単純なfor、Whileループよりも反復処理をきちんと管理可能
    * 例: 要素が複数回アクセスされないようする
        * 要素が厳密にシーケンシャルにアクセスされるようにすることなどが実現できる
    * JSでは、クロージャを使えば、比較的楽にイテレータを実装可能
    
## 実装

### テストの作成

* [test/tdd.js](src/tdd.js)
* tddjs.iteratorによって作られたイテレータの基本的な動作

```javascript
//tddjs.iteratorの実装例
(function () {
    function iterator(collection) {
        var index = 0;
        var length = collection.length;
        
        function next() {
            var item = collection[index++];
            
            return item;
        }
        
        function hasNext() {
            return index < length;
        }
        
        return {
            next: next,
            hasNext: hasNext
        };
    }
    
    if(typeof tddjs == "object") {
        tddjs.iterator = iterator;
    }
}());
```

### 実装

* [test/iterator_test.js](test/iterator_test.js)
* collection、index、1ength自由変数
    * iterator関数は、自由変数にアクセスしたメソッドが属するオブジェクトを返す
    * これはモジュールパターンの実装

## リファクタリング

### 実装のリファクタリング

* イテレータインターフェイスは､Javaのイテレータを真似るように作られている
* このインターフェイスは以下のようにもっとすっきり記述可能
* 全てのnext呼び出しは、hagNextプロパテイを更新する

```javascript
//実際的なイテレータ
(function () {
    function iterator(collection) {
        var index = 0;
        var length = collection.length;
        
        function next() {
            var item = collection[index++];
            next.hasNext = index < length;
            
            return item;
        }
        next.hasNext =  index < length;
        
        return next; ////単純にnext関数を返し、そのプロパテイとしてhagNextを管理する
    }
        
    if (typeof tddjs == "object") {
        tddjs.iterator = iterator;
    }
}());
```

### テストのリファクタリング

* これを利用すると、ループテストは以下のようにアップデート可能
* [test/iterator_test.js#24](test/iterator_test.js#24)