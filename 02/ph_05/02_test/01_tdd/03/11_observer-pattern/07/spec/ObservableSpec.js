describe('ObservableTest', function () {
    beforeEach(function () {
        this.Namespace = require('../libs/Namespace');
        require('../src/Observable');
        this.observable = this.Namespace.util.observable;
    });
    afterEach(function () {
        this.observable.observers = [];
    });
    describe('Observable.AddObserverTest', function () {
        it('test should store function', function () {
            var observers = [function () {}, function () {}];
            this.observable.observe("event", observers[0]);
            this.observable.observe("event", observers[1]);
            expect(observers).toEqual(this.observable.observers);
        });
    });
    describe('ObservableHasObserverTest', function () {
        it('test should return true when has observer', function () {
            var observer = function () {};
            this.observable.observe("event", observer);
            expect(this.observable.hasObserver("event", observer)).toBeTruthy();
        });
        it('test should return false when no observers', function () {
            expect(this.observable.hasObserver(function () {})).toBeFalsy();
        });
        it('test should return true when has observer', function () {
            var observers = [function () {}, function () {}];
            this.observable.observe("event", observers[0]);
            this.observable.observe("event", observers[1]);
            expect(this.observable.hasObserver("event", observers[0])).toBeTruthy();
            expect(this.observable.hasObserver("event", observers[1])).toBeTruthy();
        });
    });
    describe('ObservableNotifyObserversTest', function () {
        it('test should call all observers', function () {
            var observer1 = function () { observer1.called = true; };
            var observer2 = function () { observer2.called = true; };
            this.observable.observe("event", observer1);
            this.observable.observe("event", observer2);
            this.observable.notify("event");
            expect(observer1.called).toBeTruthy();
            expect(observer2.called).toBeTruthy();
        });
        it('test should pass through arguments', function () {
            var actual;
            this.observable.observe("event", function (){
                actual = [].slice.call(arguments);
            });
            this.observable.notify("event", "String", 1, 32);
            expect(["String", 1, 32]).toEqual(actual);
        });
        it('test should throw for uncallable oserver', function () {
            var observable = this.observable;
            expect(function () {
                observable.observe({});
            }).toThrow(new Error("observer is not function"));
        });
        it('test should notify all even when some fail', function () {
            var observer1 = function () { throw new Error("Oops"); };
            var observer2 = function () { observer2.called = true; };
            this.observable.observe("event", observer1);
            this.observable.observe("event", observer2);
            this.observable.notify("event");
            expect(observer2.called).toBeTruthy();
        });
        it('test should call observers in the order they were added', function () {
            var calls = [];
            var observer1 = function () { calls.push(observer1); };
            var observer2 = function () { calls.push(observer2); };
            this.observable.observe("event", observer1);
            this.observable.observe("event", observer2);
            this.observable.notify("event");
            expect(observer1).toBe(calls[0]);
            expect(observer2).toBe(calls[1]);
        });
        it('test should not fail if no observers', function () {
            observable = this.observable;
            expect(function () {
                observable.notify("event");
            }).not.toThrow(new Error("observer is not function"));
        });
    });
});

