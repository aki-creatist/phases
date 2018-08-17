var Namespace = require('../libs/Namespace');
Namespace.namespace('util');

(function () {
    function Observable() {
        // this.observers = [];
    }
    Namespace.util.Observable = Observable;
    function addObserver(observer) {
        if (!this.observers) {
            this.observers = [];
        }
        if (typeof observer != "function") {
            throw new TypeError("observer is not function");
        }
        this.observers.push(observer);
    }
    Observable.prototype.addObserver = addObserver;
    function hasObserver(observer) {
        if (!this.observers) {
            return false;
        }
        return this.observers.indexOf(observer) >= 0;
    }
    Observable.prototype.hasObserver = hasObserver;
    function notifyObservers(observer) {
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
    Observable.prototype.notifyObservers = notifyObservers;
}());
