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

require('../src/index')(Namespace);
require('../src/tab_panel')(Namespace);
