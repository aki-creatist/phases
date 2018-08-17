# ECMAScript第5版

### ES3とES5のプロトタイプ継承を融合

* [src/circle.js](src/circle.js)
* コンストラクタ内でObject.createを使ってES3とES5のプロトタイプ継承を融合する例
* このコンストラクタは、ほかのコンストラクタと同様に使える
    * Object.createも意味のある値を返してくる
    
### コンストラクタの使い方を示したテストケース

* [test/circle_test.js#3](spec/circle_test.js#3)
* 単純に関数を呼び出すだけでも、同じ効果が得られる
    * myCirclecreate(radius)を呼び出せば、myCircleを継承する円を作成可能
    * これは、JSでコンストラクタを使わずに継承を実装する方法のうちの1つ
    * コンストラクタとnewキーワードが不要なことを示している


