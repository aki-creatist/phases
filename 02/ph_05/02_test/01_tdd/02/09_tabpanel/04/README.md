# イベントハンドラのテスト

## 事前準備

* [DOMテストの準備](https://github.com/aki-creatist/prepare/tree/master/04/03/02_karma/02_karma-jasmine-html2js/02)

## 概要

* tabControllerテストケースは、タブのふるまいに集中すべき
* このようなテストは、`イベントインターフェイス専用テストケース`に入れる
    * ブラウザの違いを吸収することを目的としたテストケース
    
# テストセットアップ

* 一度に1テストケースずつ、tabControllerインターフェイスを作成
* 各テストが最小限のマークアップを作るセットアップコードを共有
* 即時無名クロージャでテストケースをラップ
    * 各テストが最小限のマークアップへの参照を維持可能にするため
* 無名クロージャ内では以下にアクセス可能
    * `名前空間内のオブジェクト`にアクセスするためのショートカット

```bash
vim spec/indexSpec.js
```

```javascript
//共有されるsetUp関数を使ったテストのセットアップ
describe('TabbedControllerActivateTabTest', function () {
    beforeEach(function () {
        document.body.innerHTML = window.__html__['spec/index.html'];
        this.tabs = document.getElementById("tabs");
        if (this.tabs != null) {
            this.controller = this.tabController.create(this.tabs);
            this.links = this.tabs.getElementsByTagName("a");
            this.lis = this.tabs.getElementsByTagName("li");
        } else {
            console.log('this.tabs is empty');
        }
    });
```

```bash
vim spec/index.html
```

```html
<ol id="tabs">
    <li><a href="#news">News</a></li>
    <li><a href="#sports">Sports</a></li>
    <li><a href="#economy">Economy</a></li>
</ol>
```


### activateTab()

* 実際に要素を受け取っているかチェックする
* タグ名がtabTagNameプロパティと一致するかチェックする
* クラス名の追加、削除を行い、最後に`onTabChange()`を呼び出す
* それまでアクティブだったタブをアクティブでなくする処理もする
* タグ名をチェックする理由
    * イベントデリゲーション
        * コンテナ要素のなかの要素ならどれでもクリックイベントを生成する
        * tabTagNameプロパテイを使えば、どの要素が`タブ`なのかを見分けられる
    * タブの状態を変更したときに限り、`activateTab()`は現在と直前のタブを引数としてonTabChangeイベントを生成する

```bash
vim src/index.js
```

```diff
  function activateTab(element) {
+     if (!element || !element.tagName ||
+         element.tagName.toLowerCase() != this.tabTagName) {
+         return;
+     }
+     //タグ名が適切なら、クラス名を追加してタブをアクティブにする
+     var className = "active-tab";
+     dom.removeClassName(this.prevTab, className);
+     dom.addClassName(element, className);
+     var previous = this.prevTab;
+     this.prevTab = element;
+     this.onTabChange(element, previous);
  }
  Namespace.namespace("ui").tabController = {
      create: create,
      handleTabClick: handleTabClick,
      activateTab: activateTab,
+     onTabChange: function (anchor, previous) {},
+     tabTagName: "a"
  };
```

```bash
vim libs/main.js
```

```diff
+ function removeClassName(element, cName) {
+     var r = new RegExp("(^|\\s)" + cName + "(\\s|$)");
+     if (element) {
+         cName = element.className.replace(r, " ");
+         element.className = cName.replace(/^\s+|\s+$/g, "");
+     }
+ }
  dom.addClassName = addClassName;
+ dom.removeClassName = removeClassName;
```

## テストの追加

```javascript
it('test should not fail without anchor', function () {
    expect(this.controller.activateTab).not.toThrow();
});
it('test should mark anchor as active', function () {
    this.controller.activateTab(this.links[0]); //クラスの追加
    expect(this.links[0].classList.contains("active-tab")).toBeTruthy();
});
it('test should deactivate previous tab', function () {
    this.controller.activateTab(this.links[0]);
    this.controller.activateTab(this.links[1]);
    expect(this.links[0]).not.toMatch(/(^|\s)active-tab(\s|$)/);
    expect(this.links[1].classList.contains("active-tab")).toBeTruthy();
});
it('test should not activate unsupported element types', function () {
    this.controller.activateTab(this.links[0]);
    this.controller.activateTab(this.lis[0]);
    expect(this.lis[0]).not.toMatch(/(^|\s)active-tab(\s|$)/);
    expect(this.links[0].classList.contains("active-tab")).toBeTruthy();
});
it('test should fire onTabChange', function () {
    var actualPrevious, actualCurrent;
    this.controller.activateTab(this.links[0]);
    this.controller.onTabChange = function (curr, prev) {
        actualPrevious = prev;
        actualCurrent = curr;
    };
    this.controller.activateTab(this.links[1]);
    expect(actualPrevious).toBe(this.links(0));
    expect(actualCurrent).toBe(this.links(1));
})
```
