//addObserverが内部配列に観察者を追加することを確かめる

describe('Observable.AddObserverTest', function () {
    var Namespace = require('../libs/Namespace');
    var Observable = require('../src/Observable');
    it('test should store function', function () {
        var observable = new Namespace.util.Observable();
        var observers = [function () {}, function () {}];
        observable.addObserver(observers[0]);
        observable.addObserver(observers[1]);
        expect(observers).toEqual(observable.observers);
    });
});
describe('ObservableHasObserverTest', function () {
    var Namespace = require('../libs/Namespace');
    var Observable = require('../src/Observable');
    it('test should return true when has observer', function () {
        var observable = new Namespace.util.Observable();
        var observer = function () {};
        observable.addObserver(observer);
        expect(observable.hasObserver(observer)).toBeTruthy();
    });
    it('test should return false when no observers', function () {
        var observable = new Namespace.util.Observable();
        var observer = function () {};
        observable.addObserver(observer);
        expect(observable.hasObserver(function () {})).toBeFalsy();
    });
    it('test should return true when has observer', function () {
        var observable = new Namespace.util.Observable();
        var observers = [function () {}, function () {}];
        observable.addObserver(observers[0]);
        observable.addObserver(observers[1]);
        expect(observable.hasObserver(observers[0])).toBeTruthy();
        expect(observable.hasObserver(observers[1])).toBeTruthy();
    });
});
describe('ObservableNotifyObserversTest', function () {
    var Namespace = require('../libs/Namespace');
    var Observable = require('../src/Observable');
    it('test should call all observers', function () {
        var observable = new Namespace.util.Observable();
        var observer1 = function () { observer1.called = true; };
        var observer2 = function () { observer2.called = true; };
        observable.addObserver(observer1);
        observable.addObserver(observer2);
        observable.notifyObservers();
        expect(observer1.called).toBeTruthy();
        expect(observer2.called).toBeTruthy();
    });
    it('test should pass through arguments', function () {
        var observable = new Namespace.util.Observable();
        var actual;
        observable.addObserver(function (){
            actual = [].slice.call(arguments);
        });
        observable.notifyObservers("String", 1, 32);
        expect(["String", 1, 32]).toEqual(actual);
    });
    it('test should throw for uncallable oserver', function () {
        var observable = new Namespace.util.Observable();
        expect(function (){
            observable.addObserver({});
        }).toThrow(new Error("observer is not function"));
    });
    it('test should notify all even when some fail', function () {
        var observable = new Namespace.util.Observable();
        var observer1 = function () { throw new Error("Oops"); };
        var observer2 = function () { observer2.called = true; };

        observable.addObserver(observer1);
        observable.addObserver(observer2);
        observable.notifyObservers();
        expect(observer2.called).toBeTruthy();
    });
    it('test should call observers in the order they were added', function () {
        var observable = new Namespace.util.Observable();
        var calls = [];
        var observer1 = function () { calls.push(observer1); };
        var observer2 = function () { calls.push(observer2); };
        observable.addObserver(observer1);
        observable.addObserver(observer2);
        observable.notifyObservers();
        expect(observer1).toBe(calls[0]);
        expect(observer2).toBe(calls[1]);
    });
});
