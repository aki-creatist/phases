var Namespace = require('../libs/Namespace');
Namespace.namespace('util');

(function () {
    function observe(observer) {
        if (!this.observers) {
            this.observers = [];
        }
        if (typeof observer != "function") {
            throw new TypeError("observer is not function");
        }
        this.observers.push(observer);
    }
    function hasObserver(observer) {
        if (!this.observers) {
            return false;
        }
        return this.observers.indexOf(observer) >= 0;
    }
    function notify(observer) {
        if (!this.observers) {
            return;
        }
        for (var i = 0, l = this.observers.length; i < l; i++) {
            try {
                this.observers[i].apply(this, arguments);
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
