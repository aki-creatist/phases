function addEventHandler(element, type, listener) { //ブラウザの推測を使ってイベントリスニングの違いを吸収する
    if (tddjs.isHostMethod(element, "addEventListener")) {
        element.addEventListener(type, listener, false);
    } else if (tddjs.isHostMethod(element, "attachEvent") &&
        listener.call) {
        element.attachEvent("on" + type, function () {
            // listenerの引数としてイベントを渡し、thisの値を修正する
            // IEはグローバルオブジェクトをthisとしてlistenerを呼び出す
            return listener.call(element, window.event);
        });
    } else {
        // イベントプロパティにグレードダウンするか処理を中止するか
    }
}
