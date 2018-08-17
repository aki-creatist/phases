# 最初のテスト

```bash
touch libs/main.js
```

```javascript
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
```

```bash
touch src/index.js
```

```javascript
module.exports = function (Namespace) {
    function create(element) {
        if (!element || typeof element.className != "string") {
            throw new TypeError("element is not an element");
        }
    }
    Namespace.namespace("ui").tabController = {
        create: create,
    };
};
```

```bash
touch spec/indexSpec.js
```

```javascript
describe('TabTest >', function () {
    beforeEach(function () {
        var Namespace = require('../libs/main.js');
        this.tabController = Namespace.ui.tabController;
    });
    describe('TabControllerCreateTest', function () {
        it('test should fail without element', function () {
            tabController = this.tabController;
            expect(function () {
                tabController.create();
            }).toThrowError("element is not an element");
        });
        it('test should fail without element class', function () {
            tabController = this.tabController;
            expect(function () {
                tabController.create({});
            }).toThrowError("element is not an element");
        });
    });
});
```
