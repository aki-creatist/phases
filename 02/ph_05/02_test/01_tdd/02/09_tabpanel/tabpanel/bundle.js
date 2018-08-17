/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};

/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {

/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId])
/******/ 			return installedModules[moduleId].exports;

/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			exports: {},
/******/ 			id: moduleId,
/******/ 			loaded: false
/******/ 		};

/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);

/******/ 		// Flag the module as loaded
/******/ 		module.loaded = true;

/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}


/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;

/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;

/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";

/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ function(module, exports, __webpack_require__) {

	var Namespace = {
	    namespace: function (string) {
	        var object = this;
	        var levels = string.split('.');
	        for (var i = 0, l = levels.length; i < l; i++) {
	            if (typeof object[levels[i]] === 'undefined') {
	                object[levels[i]] = {};
	            }
	            object = object[levels[i]];
	        }
	        return object;
	    }
	}
	module.exports = Namespace;

	//メソッド1
	(function () {
	    var dom = Namespace.namespace("dom");
	    function addClassName(element, cName) {
	        var regexp = new RegExp("(^|\\s)" + cName + "(\\s|$)");
	        if (element && !regexp.test(element.className)) {
	            cName = element.className + " " + cName;
	            element.className = cName.replace(/^\s+|\s+$/g, "");
	        }
	    }
	    function removeClassName(element, cName) {
	        var r = new RegExp("(^|\\s)" + cName + "(\\s|$)");
	        if (element) {
	            cName = element.className.replace(r, " ");
	            element.className = cName.replace(/^\s+|\s+$/g, "");
	        }
	    }
	    dom.addClassName = addClassName;
	    dom.removeClassName = removeClassName;
	}());

	__webpack_require__(1)(Namespace);
	__webpack_require__(2)(Namespace);

	console.log(Namespace);

/***/ },
/* 1 */
/***/ function(module, exports) {

	module.exports = function (Namespace) {
	    var dom = Namespace.dom;
	    function test() {
	        return 'OK';
	    }
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
	        test: test,
	        create: create,
	        handleTabClick: handleTabClick,
	        activateTab: activateTab,
	        onTabChange: function (anchor, previous) {},
	        tabTagName: "a"
	    };
	};

/***/ },
/* 2 */
/***/ function(module, exports) {

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

/***/ }
/******/ ]);