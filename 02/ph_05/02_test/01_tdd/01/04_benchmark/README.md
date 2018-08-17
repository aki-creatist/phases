## パフォーマンスツール

* 相対的なパフォーマンスを計測するベンチマークも、選択の判断要素になる
    * オブジェクト作成にコンストラクタを使うかクロージャを使うかetc

### ベンチマークと相対的なパフォーマンス

* 与えられた問題の解き方が複数ある場合
* ベンチマークを使うと、ある方法がほかの方法と比べてどれくらい高速か、すなわち「相対的なパフォーマンス」がわかる
* 通常、計測のためのコード実行では、精度を上げるために、ループを使って何度も実行する
    * 少なくとも500m秒以上はテストを実行するようにすべき

```javascript
//ベンチマークランナー
var ol;

function runBenchmark(name, test) {
    if (!ol){
        ol = document.createElement("ol");
        document.body.appendChild(ol);
    }
    
    setTimeout(function () {
        var start = new Date().getTime();
        test(); //計測対象のコードを実行する
        var total = new Date().getTime() - start; //最初のDateを減算すると、処理にかかった時間がわかる
        
        var li = document.createElement("li");
        li.innerHTML = name + ": " + total + "ms"; //結果を比較する
        ol.appendChild(li);
    }, 15);
}
```

### 相対的パフォーマンスを計測

* ファイルは、benchmarks/loops.jsに保存する
* 関数が仮引数を取らなければ、benchmarkが自分のループのなかで関数を呼び出す
* そうでなければ、繰り返しの回数は関数に引数として渡され、関数が関数呼び出しのオーバーヘッドを避けて自分でループを実行可能
* テスト中にブラウザを止めないために、setTimeout呼び出しは重要
    * ブラウザは１つのスレッドを使ってJSを実行し、イベントを生成し、Webページをレンダリングする
    * タイマーは、長時間実行されている可能性のあるテストの合間にキューイングされたタスクを拾い上げる「息継ぎ」の機会を与える
        * キューイング: アプリケーションソフト間でデータを交換して連携動作させる際に、送信するデータをいったん保管しておき、相手の処理の完了を待つことなく次の処理を行う方式
        * 息継ぎ: タイマーによって作業を中断すると、ブラウザがテストに割り込んで「スクリプトの実行が遅い」と警告してくるのも避けられる
* このベンチマークを実行するために必要なものは、スクリプトをロードする簡単なHTMLファイルだけ
* [benchmarks/loops.js](benchmarks/loops.js)
* YUI Test HTMLフィクスチャファイル
    * [benchmarks/loops.html](benchmarks/loops.html)
    
```javascript
//テストを実行
runBenchmark("for-loop",
    forLoop);
runBenchmark("for-loop, cached length",
    forLoopCachedLength);
runBenchmark("for-loop, direct array access",
    forLoopDirectAccess);
runBenchmark("while-loop",
    whileLoop);
runBenchmark("while-loop, cached length property",
    whileLoopCachedLength);
runBenchmark("reversed while-loop",
    reversedWhileLoop);
runBenchmark("double reversed while-loop",
    doubleReversedWhileLoop);
```

* 配列のすべての要素をループで処理した後に現在の要素にアクセスする
    * ループ条件で現在の要素にアクセスしているループとそうでないループを比較可能
    * その分、要素へのアクセスによってテストのフットプリントは大きくなる
        * フットプリント: プログラムが動作する際のメモリ使用量の多さ
* テストの結果の変動要因としてのアクセスのオーバーヘッドは、ループスタイルの違いによる結果として無視することができる
    * すべてのテストが現在の要素にアクセスするため
    * オーバーヘッド: 機器やシステムへかかる負荷、余分に費やされる処理時間などのこと
* ベンチマーク上は配列要素の反復処理としては、逆whileが最も高速
* ベンチマークを作業フローに簡単に統合できるようにするためには、ベンチマーク作成から余分な作業をすべて取り除く単純なbenchmark関数が必要
* 単純なベンチマークツール
    * [lib/benchmark.js](lib/benchmark.js)
    * この関数は、第１引数として一連のテストのためのラベル、第２引数として、プロパティ名がテスト名として使われるオブジェクト、プロパティの値がテストされる関数となっているオブジェクトを受け付ける
    * 最後の引数はオプションで、テストを何回実行すべきかをベンチマークに知らせる
    * 結果は、テストごとの全時間と平均時間の両方の形で表示される
* benchmark関数は、各イテレーションを関数として実行する
* テストは関数という形にまとめられ、その関数は指定された回数だけ実行される
* この関数呼び出し自体にフットプリントがあるため、テストにどれだけの時間がかかったかについては、精度が落ちる
* 関数呼び出しによってテストの数値が大きく歪められるのを避けたければ、関数が何個の仮引数を取るかを示すlengthプロパティを利用する方法もある
    * 以下は反復回数を引数として単純に関数を呼び出す

```javascript
// Inside runTests
(function (name, test) {
    setTimeout(function () {
        var start = new Date().getTime();
        var l = iterations;

        if(!test.length) {
            while(l--) {
                test();
            }
        }else {
            test(l);
        }

        var total = new Date().getTime() - start;

        var li = document.createElement("li");
        li.innerHTML = name + ": " + total +
            "ms (total), " + (total / iterations) +
            "ms (avg)";
        view.appendChild(li);
    }, 15);
}(label, tests[label]));
```

* benchmarkの使い方の例として、ループテストを書き換える
* benchmarkの使用例
    * [benchmarks/loops.js](benchmarks/loops.js)
* この例では、ループで処理する配列の長さを少し短くし、全体としての反復回数を増やしている
* コードを簡潔にするために、一部のテストは省略されている
* この種のベンチマーク用ユーティリティは、もっと使いやすいレポートを生成するように書き換えられる
* 例: 最高速のテストと最低速のテストの結果を強調表示することなどが考えられる
* 極端地を計測、強調表示する
    * [lib/benchmark.js](lib/benchmark.js)
* 結果を表示するDOM操作をここから切り離して代替レポートジェネレータを認められるようにする
    * benchmarkをさらに拡張可能
    * そうすれば、サーバーサイドJSランタイムなど、DOMのない環境でもベンチマークテストを実行可能になる

### プロファイリングとボトルネックの検出

* Firebugは、実行されるコードをプロファイリングできるプロファイラを提供している
* 動いているサイトに行き、プロファイラを起動し、スクリプトを起動するリンクをクリックする
* スクリプトが終了してから、プロファイラを止める
* すると、プロファイルレポートが実行された関数の明細とそれぞれの実行にかかった時間を表示する

### まとめ

* JSについての学習を進めるためにも単体テストが使える
* 学習テストスイートを残すと、学習したことのドキュメントとして非常に効果的
* 過去に遭遇したさまざまな問題のハンディなリファレンスになる
* 与えられた問題の有力な解法がいくつもあるときには、ベンチマークを実施するとどれを選べばよいかを決めやすくなる
* 相対的なパフォーマンスを計測すれば、パフォーマンスがよくなる傾向のあるパターンがどのようなものかを学べる
* 学習テストとともにベンチマークを残せば、個人用の知識バンクとして非常に強力なものができあがる

