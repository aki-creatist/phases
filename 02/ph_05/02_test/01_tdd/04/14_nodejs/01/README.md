# モジュールを定義する：最初のテスト

## テストの作成

* コントローラオブジェクトが存在し、コントローラが`create()`を持つことを確認 
    * test/chapp/chat_room_controller_test.js
    
```javascript
var testCase = require("nodeunit").testCase;
var chatRoomController = require("chapp/chat_room_controller");

testCase(exports, "chatRoomController", {
    "should be object": function (test) {
        test.isNotNull(chatRoomController);
        test.isFunction(chatRoomController.create);
        test.done();
    }
});
```

```bash
./run_tests
#Can't find module chapp/chat_room_controller.(chapp/chat_room__controllerモジュールを見つけられない)
```

* 不合格に終わる
* コントローラモジュールを作ればこの問題は解決
    * lib/chapp/chat_room_controller.js

```javascript
var chatRoomController = {
    create: function () {}
}

module.exports = chatRoomController;
```

```bash
./run_tests
```

```text
test/chapp/chat_room_controller_test.js
chatRoomController should be object

OK: 2 assertions (2ms)
```

* テストケースはtestオブジェクトを受け取り、その`done()`を呼び出す
* テストが終了したタイミングを明示的に知らせる必要がある
    * nodeunitは、非同期にテストを実行するため
* Nodeでは、非同期テストを禁じると、全てのシステムコールをスタブまたはモックにしなければならない
* 仮に同期的にテストしようとすると、エラーを起こしやすい
    * テストが難しくなるだけでなく、インターフェイスを強制するものがないため