var Namespace = require('../libs/Namespace');
Namespace.namespace('util');

(function () {
    function observe(event, observer) {
        if (!this.observers) {
            this.observers = [];
        }
        if (typeof observer != "function") {
            throw new TypeError("observer is not function");
        }
        this.observers.push(observer);
    }
    function hasObserver(event, observer) {
        if (!this.observers) {
            return false;
        }
        return this.observers.indexOf(observer) >= 0;
    }
    function notify(event, observer) {
        if (!this.observers) {
            return;
        }
        var args = Array.prototype.slice.call(arguments, 1);
        for (var i = 0, l = this.observers.length; i < l; i++) {
            try {
                this.observers[i].apply(this, args);
            } catch (e) {
                //
            }
        }
    }
    Namespace.namespace("util").observable = {
        observe: observe,
        hasObserver: hasObserver,
        notify: notify
    };
}());
