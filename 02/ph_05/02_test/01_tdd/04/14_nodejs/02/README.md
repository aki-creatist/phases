# コントローラを作る

* コントローラが、`create()`に渡した引数に対応して、request、responseプロパティを持っていることをアサート

```javascript
//新しいコントローラが作成されていることを確かめる
testCase(exports, "chatRoomController.create", {
    "should return object with request and response":
    function (test) {
        var req = {};
        var res = {};
        var controller = chatRoomController.create(req, res);
        
        test.inherits(controller, chatRoomController);
        test.stringEqual(controller.request, req);
        test.stringEqual(controller.response, res);
        test.done();
    }
});
```

* request、responseを定義する
    * enumerable、configurable、writable属性にデフォルト値がセットされる
    * これでテストに合格する
    
```javascript
//コントローラを作る
var chatRoomController = {
    create: function (request, response) {
        return  Object.create(this, {
            request: { value: request },
            response: { value: response }
        });
    }
};
```