Circle = require('../src/Circle')
/**
 * コンストラクタがプリミティブ値ではなくオブジェクトを返す場合、
 * その新しいオブジェクトはthisとして作られるわけではない
 * その場合、newキーワードは構文的にはまったくの装飾になる
 */
describe('CircleTest', function () {
    it('test Object.create backed constructor', function () { //八イブリッドCircleの使い方
        var circle = new Circle(3);

        expect(circle instanceof Circle).toBeTruthy();
        expect(circle.diameter).toBe(6);

        circle.radius = 6;
        expect(circle.diameter).toBe(12);

        delete circle.radius;
        // expect(circle.diameter).toBe(6);
    });
    it('test omitting new when creating circle', function () { //newなしでCircleを使う
        var circle = Circle(3);

        expect(circle instanceof Circle).toBeTruthy();
        expect(circle.diameter).toBe(6);
    });
    it('test using a custom create method', function () { //Obiect.createと関数を使う
        var circle = Object.create({}, {
            diameter: {
                get: function () {
                    return this.radius * 2;
                }
            },

            circumference: { /* ... */ },
            area: { /* ... */ },

            create: {
                value: function (radius) {
                    var circ = Object.create(this, {
                        radius: { value: radius }
                    });

                    return circ;
                }
            }
        });

        var myCircle = circle.create(3);

        // expect(circle.diameter).toBeUndefined();
        expect(circle.isPrototypeOf(myCircle)).toBeTruthy();

        // // circle is not a function
        // assertException(function () {
        //     assertFalse(myCircle instanceof circle);
        // });
    });
});

