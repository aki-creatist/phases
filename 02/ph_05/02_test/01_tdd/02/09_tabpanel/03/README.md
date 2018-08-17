# ヘルパー関数の準備

* 単純に要素のclass属性へのクラス名の追加、削除を行う

```bash
vim libs/main.js
```

```diff
  module.exports = Namespace;
+ (function () { //クラス名の追加、削除
+     var dom = Namespace.namespace("dom");
+     function addClassName(element, cName) {
+         var regexp = new RegExp("(^|\\s)" + cName + "(\\s|$)");
+         if (element && !regexp.test(element.className)) {
+             cName = element.className + " " + cName;
+             element.className = cName.replace(/^\s+|\s+$/g, "");
+         }
+     }
+     dom.addClassName = addClassName;
+ }());
  require('../src/index')(Namespace);
```

```bash
vim src/index.js
```

```diff
  module.exports = function (Namespace) {
+     var dom = Namespace.dom;
      function create(element) {
          if (!element || typeof element.className != "string") {
              throw new TypeError("element is not an element");
          }
+         dom.addClassName(element, "js-tab-controller"); //クラス名を要素に追加して、CSSがタブをタブとして表示可能にする
+         var tabs = Object.create(this);                 //tabControllerオブジェクトを作成
+         return tabs;
      }
      Namespace.namespace("ui").tabController = {
          create: create,
      };
  };
```

```bash
vim spec/index.js
```

```javascript
it('should return object', function () {
    if (this.tabs != null) {
        var controller = this.tabController.create(this.tabs);
        expect(typeof controller).toBe(typeof {});
    }
});
it('test should add js-tabs class name to element', function () {
    if (this.tabs != null) {
        var tabs = this.tabController.create(this.tabs);
        expect(this.tabs.classList.contains("js-tab-controller")).toBeTruthy();
    }
});
```

### tabControllerオブジェクト

* ここは、`DOM 0`イベントリスナー(onclickプロパティ）を含むと危険
* `DOM 2`イベントリスナーを使った方が安全
* ここで、リスト要素全部のために1つのイベントハンドラを登録
    * そのイベントハンドラにイベントオブジェクトを渡す
    * イベントデリケーシヨンを使っている
    * [イベントデリケーション](https://www.webprofessional.jp/event-bubbling-javascript/)

```bash
vim src/index.js
```

```diff
  function create(element) { //要素にイベントハンドラも追加する
      if(!element || typeof element.className != "string") {
          throw new TypeError("erement is not an element");
      }
      dom.addClassName(element, "js-tab-controller");
      var tabs = object.create(this);
      //ol要素のonclickリスナーの制御をを他のスクリプトに奪われることを想定していない
+     element.onclick = function (event) {
+         tabs.handleTabClick(event || window.event || {});
+     };        
+     element = null;
      return tabs;
  }
+ function handleTabClick(event){
      //後ほど追記する
+ }
    
  tddjs.namespace("ui").tabController = {
      create: create,
+     handleTabClick: handleTabClick
+ };
```

### イベントの処理について

* `handleTabClick()`によって処理される
* ハンドラは、`イベントを発生させた要素`を受け付ける
    * ほとんどのブラウザではイベントオブジェクトの`target`プロパティ
    * Internet Explorerでは`srcElement`
* テキストノードよりも上位の要素ノードを操作するよう
    * テキストノードで直接イベントを生成することのあるブラウザに対応するため
* 最後に、イベントを発生させた要素を`activateTab())`に渡す

```bash
vim src/index.js
```

```diff
+ //handleTabClickの実装
+ function handleTabC1ick(event) {
+     var target = event.target || event.srcElement;
+     while (target && target.nodeType != 1) {
+         target=target.parentNode;
+     }
+     this.activateTab(target);
+ }
+ function activateTab(element) {
+ }
  Namespace.namespace("ui").tabController = {
      create: create,
      handleTabClick: handleTabClick,
+     activateTab: activateTab,
  };
```
