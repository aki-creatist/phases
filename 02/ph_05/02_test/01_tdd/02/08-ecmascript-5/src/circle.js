function Circle(radius) { //Object.createを使ったコンストラクタ
  var _radius;

  var circle = Object.create(Circle.prototype, {
    radius: {
      configurable: false,
      enumerable: true,

      set: function (r) {
        if (typeof r != "number" || r <= 0) {
          throw new TypeError("radius should be > 0");
        }

        _radius = r;
      },

      get: function () {
        return _radius;
      }
    }
  });

  circle.radius = radius;

  return circle;
}

/**
 * 新オブジェクトを作るCreate()を外部に公開する1個のオブジェクトを作る
 * そのため、newもPrototypeも不要だが、プロトタイプ継承は、期待通りに動作する
 */
Circle.prototype = Object.create(Circle.prototype, {
  diameter: {
    get: function () {
      return this.radius * 2;
    },

    configurable: false,
    enumberable: true
  },

  circumference: { /* ... */ },
  area: { /* ... */ }
});

module.exports = Circle;