module.exports = function (Namespace) {
    var dom = Namespace.dom;

    function create(element) {
        if (!element || typeof element.className != "string") {
            throw new TypeError("element is not an element");
        }
        //要素が十分なものなら以下を実施
        dom.addClassName(element, "js-tab-controller"); //クラス名を要素に追加して、CSSがタブをタブとして表示可能にする
        var tabs = Object.create(this);                 //tabControllerオブジェクトを作成
        element.onclick = function (event) {
            tabs.handleTabClick(event || window.event || {});
        };
        element = null;
        return tabs;
    }
    function handleTabClick(event) {
        var target = event.target || event.srcElement;
        while (target && target.nodeType != 1) {
            target = target.parentNode;
        }
        this.activateTab(target);
    }
    function activateTab(element) {
        if (!element || !element.tagName ||
            element.tagName.toLowerCase() != this.tabTagName) {
            return;
        }
        //タグ名が適切なら、クラス名を追加してタブをアクティブにする
        var className = "active-tab";
        dom.removeClassName(this.prevTab, className);
        dom.addClassName(element, className);
        var previous = this.prevTab;
        this.prevTab = element;
        this.onTabChange(element, previous);
    }
    Namespace.namespace("ui").tabController = {
        create: create,
        handleTabClick: handleTabClick,
        activateTab: activateTab,
        onTabChange: function (anchor, previous) {},
        tabTagName: "a"
    };
};