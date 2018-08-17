# 同じユーザーからの反復メッセージを抑える

## 概要

* メッセージフォームコントローラに進む前に、もう１つテストを追加する

## 要件

* 同じユーザーから複数の連続したメッセージを受け取る
* その際にコントローラがそのユーザーのメッセージを繰り返さないようにする
    * ２つの連続したメッセージが同じユーザーから送られたら、第２のdt要素を追加しない

## テストの追加

* ２つのメッセージを追加し、1個のdt要素しかないことを確かめる 
* テストは不合格になる

```javascript
//コントローラがdt要素を繰り返さないことを確かめる
"test should not repeat same user dt's": function() {
    this.controller.addMessage({
        user: "Kyle",
        message: "One-two-three not it!"
    });
    this.controller.addMessage({ user:"Kyle", message:":)" });

    var dts = this.element.getElementsByTagName("dt");
    var dds = this.element.getElementsByTagName("dd");
    assertEquals(1, dts.length);
    assertEquals(2, dds.length);
}
```

## ソース修正

* テストに合格するためには、コントローラに前のユーザーを管理させる
* 単純に、最後に発言したユーザーを格納するプロパティを管理する
* 以下は、更新後の`addMessage()`

```javascript
//最後に発言したユーザーを管理する
function addMessage(message) {
    if (this.prevUser != message.user) {
        var user = document.createElement("dt");
        user.innerHTML = "@" + message.user;
        this.view.appendChild(user);
        this.prevUser = message.user;
    }
    /* ... */
}
```

* 存在しないプロパティはundefinedとなり、現在のユーザーとは決して等しくならない
* そのため、このプロパティは初期化する必要がない
* 最初のメッセージを受け取ったとき、dtが追加される
    * prevUserプロパティはユーザーと一致しないため
* その後は、新しいdt要素が作られ、追加される
    * 但し、新しいユーザーからのメッセージが届いたときに限る
* 注意: getElementsByTagNameなどが返すノードリストが生きたオブジェクト
    * つまり、DOMの現在の状態をいつも反映している
* 両方のテストからdt、dd要素のコレクションにアクセスしている
    * 重複を避けるためにsetUpでリストを取り出すことも可能

## 残タスク

* カレントユーザー宛のメッセージは、クラス名をdd要素でマーキングして強調表示したい
* カレントユーザーはgetElementsByTagNameから得る
    * `宛の`: `@usr:から始まるメッセージ`