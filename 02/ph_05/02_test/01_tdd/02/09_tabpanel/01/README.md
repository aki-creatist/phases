# 準備

```bash
mkdir css libs spec src
touch libs/main.js
touch src/index.js
touch spec/indexSpec.js
```

## libs/main.js

```javascript
var ClassA = {
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
module.exports = ClassA;

//メソッド1
(function () {
    var space_A = ClassA.namespace("space_A");
    function methodA() {}
    function methodB() {}
    space_A.methodA = methodA;
    space_A.methodB = methodB;
}());

require('../src/index')(ClassA);

console.log(ClassA);
```

## src/index.js

```javascript
module.exports = function (ClassA) {
    (function () {
        function methodC() {
            return 'OK';
        }
        function methodD() {}
        ClassA.namespace("space_B").method_CD = {
            methodC: methodC,
            methodD: methodD
        };
    }());
};
console.log(ClassA);
```

## spec/indexSpec.js

```javascript
var ClassA = require('../src/main');

describe('requireTest', function() {
    it('methodC()を呼び出してOKが返ること', function() {
        var method_CD = ClassA.space_B.method_CD;
        expect(method_CD.methodC()).toBe('OK');
    });
});
```