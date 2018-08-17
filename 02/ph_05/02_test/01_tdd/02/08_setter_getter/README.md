# ゲッターとセッター

* ブラウザはゲッターとセッターを実装している
* プロパテイを取得、設定するためのロジックを追加可能
    * クライアントコードを書き換えずに行える

```javascript
//circleがゲッターとセッターを使って仮想diameterプロパテイを追加する例
it('test property accessors', function () {
    var circle = {};
    Object.defineProperty(circle, "diameter", {
        get: function () {
            return this.radius * 2;
        },
        set: function (diameter) {
            if (isNaN(diameter)) {
                throw new TypeError("Diameter should be a number");
            }

            this.radius = diameter / 2;
        }
    });
    circle.radius = 4;
    expect(circle.diameter).toBe(8);
    circle.diameter = 3;
    expect(circle.diameter).toBe(3);
    expect(circle.radius).toBe(1.5);

    // assertException(function () {
    //     circle.diameter = {};
    // });
});
```