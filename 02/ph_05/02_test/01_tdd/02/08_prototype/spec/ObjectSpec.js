describe('ES5ObjectTest', function () {
    it('test defineProperty', function () {
        var circle = {};
        //オブジェクトにプロパテイを追加できるかどうかを決めるもの
        Object.defineProperty(circle, "radius", {
            value: 4,
            //writableとconfigurableをfalseにすると、イミュータブルなオブジェクトが作れる
            writable: false,
            configurable: false
        });
        expect(circle.radius).toBe(4);
    });
    it('test inheritance, es5 style', function () { //プロトタイプを取得設定するためのベンダー拡張
        var circle = { /* ... */ };
        var sphere = Object.create(circle);
        expect(circle.isPrototypeOf(sphere)).toBeTruthy();
        expect(Object.getPrototypeOf(sphere)).toBe(circle);
    });
    it('test Object.create with properties', function () { //プロパティとともにオブジェクトを作る
        var circle = { /* ... */ };
        var sphere = Object.create(circle, {
            radius: {
                value: 3,
                writable: false,
                configurable: false,
                enumerable: true
            }
        });
        expect(sphere.radius).toBe(3);
    });
    it('test inheritance via proprietary __proto__', function () {
        var circle = { /* ... */ };
        var sphere = {};
        sphere.__proto__ = circle;
        expect(circle.isPrototypeOf(sphere)).toBeTruthy();
    });
});