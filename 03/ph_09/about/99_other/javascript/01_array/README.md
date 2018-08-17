# 配列の新機能

* `Array.isArray`
    * `[[Class]]`内部プロパテイをチェックして、オブジェクトが配列かどうかを返す
    * `[[Class]]`内部プロパテイは、`Object.prototype.toString`で参照可能
    * これを使えば以下のように標準準拠実装を作成可能

```javascript
if (!Array.isArray) {
  Array.isArray = (function () {
    function isArray(object) {
      return Object.prototype.toString.call(object) ==
               "[object Array]";
    }

    return isArray;
  }());
}
```