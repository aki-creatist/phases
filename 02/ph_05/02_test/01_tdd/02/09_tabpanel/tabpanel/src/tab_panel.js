/**
 * 各セクションへのリンクを含んでいるol要素からタブコントローラを作る
 */
module.exports = function (Namespace) {

    if (typeof document == "undefined" ||
        !document.getElementById) {
        return;
    }
    var dom = Namespace.dom;
    var ol = document.getElementById("news-tabs");
    /**
     * 実引数をチェックし、受け取ったものが要素でなければ処理を中止する
     *   onTabChange()は、curr、prevアンカーをチェックせずにgetPanelを呼び出し可能になる
     *   初めて呼び出すときにはprevがunaefinedになるが、問題は起きない
     */
    function getPanel(element) { //アンカーがトグルすべきパネルを見つける
        if (!element || typeof element.href != "string") {
            return null;
        }
        var target = element.href.replace(/.*#/, ""); //`#`より文字の後ろの部分を取り出し
        var panel = document.getElementsByName(target)[0]; //その名前に対応する要素をルックアップし、最初に見つけたものを返す
        while (panel && panel.tagName.toLowerCase() != "div") {
            panel = panel.parentNode;
        }
        return panel;
    }
    try {
        var controller = Namespace.ui.tabController.create(ol); //ol要素からタブコントローラを作る
        dom.addClassName(ol.parentNode, "js-tabs"); //タブをクリックしたときに、タブがactive-tabのクラス名をトグルする
        controller.onTabChange = function (curr, prev) { //タブコントローラのonTabChangeコールバックにフック
            //アンカーと情報セクションを使って、パネルのアクティブ状態をトグルさせる
            dom.removeClassName(getPanel(prev), "active-panel"); //それまでのパネルを無効に
            dom.addClassName(getPanel(curr), "active-panel");    //新しく選択されたパネルを有効に
        };
        controller.activateTab(ol.getElementsByTagName("a")[0]); //最初のタブアンカーがフェッチされてアクティブ化する
    } catch (e) {}
};