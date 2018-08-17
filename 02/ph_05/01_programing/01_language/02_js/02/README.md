# クリック以外のイベントを利用する

* フォームで役に立つイベントは、clickイベントばかりではない
* コントロールが選択状態になった時に発生するfocusイベントや、キーの押し放しで発生するkeyup、keydownイベントなどがある
* これらのイベントを利用して、入力状態のチェックなどを行う

## HTML要素の表示/非表示を切り替える

* Webページ上にJavaScriptを使って何かを表示させる場合、後から要素を追加するよりは、要素を隠しておいて表示させた方が容易
* メッセージのために４つのスタイルを定義しており、名前に「_hide」が付く２つには、「display:none」というCSSプロパティを設定している
* これは設定した要素を非表示にする働きがある
* つまり、目的の要素のclass属性に「_hide」を設定したら非表示、それ以外を設定すれば、表示される

```css
.desc_show{font-size:12px; background:cyan; padding:4px;
position:absolute; left:330px; top:20px; width:120px;}
.desc_hide{display: none;}
.alert_show{font-size:12px; background:red; color:white; padding:4px;
position:absolute; left:330px; top:0px; width:120px;}
.alert_hide{display: none;}
```

* 初期状態ではメッセージを非表示にしておきたい
* 「desc_hide」とalert_hide」をclass属性に指定している

```html
<div id="desc_amount" class="desc_hide">
購入個数を入力してください（1以上）。</div>
<div id="alert_amount" class="alert_hide">購入個数が0個です。</div>
```

## フォーカスによって発生するイベント

* フォームのコントロールが選択され、入力可能な状態になることを「フォーカスを得る」という
* コントロールがフォーカスを得たときはfocusイベント、失ったときはblurイベントが発生する
* これらのイベントを利用して、操作しているコントロールに関するメッセージを表示させている
* イベントの設定方法は、clickイベントやloadイベントと全く変わらない
* フォーカスを得たときはamount_gotFocus関数、フォーカスを失ったときはamount_losFocus関数が呼び出されるように設定される

```js
elem = document.getElementById('txt_amount');
elem.addEventListener('focus', amount_gotFocus, false);
elem.addEventListener('blur', amount_lostFocus, false);
```

* それぞれの関数内で、classNameプロパティに「desc_show」か「desc_hide」を設定する
* これでフォーカスを得た時にメッセージが表示され、失った時にメッセージが非表示になるようになる

```js
//フォーカス取得時のメッセージ表示
function amount_gotFocus(event){
var desc = document.getElementById('desc_amount');
desc.className = 'desc_show';
}
function amount_lostFocus(event){
var desc = document.getElementById('desc_amount');
desc.className = 'desc_hide';
}
```

## キーの押し放しによって発生するイベント

* テキストボックスに入力されたものが、１以上の数値でない場合、警告メッセージを表示させている
* コントロールの値の変化によって発生するイベントにはchangeイベントがある
    * テキストボックスでは値を変更させたい場合は、keydownやkeyupなどのキーボードイベントを使用する
* keydownはキーボード上の何らかのキーが押し下げられた時、keyupは話された時に発生する
* つまり２つのイベントは、順番に発生する
* keyupに対してamount_keyup関数を設定しているが、用途的にはキーが操作されていることがわかればいい
    * keyupとkeydownのどちらを使っても構わない

```js
elem.addEventListener('keyup', amount_keyup, false);
```

* amout_keyup関数では、その時のてきすボックスの値を取得して、それが0より大きい数値であれば警告メッセージを消し、それ以外なら警告メッセージを表示させている
* ここではテキストボックスの値を取り出すために、Eventオブジェクトを利用している

```js
//入力チェック
function amount_keyup(event){
var amount = event.currentTarget.value;
var alert = document.getElementById('alert_amount');
if(amount > 0){
    alert.className = 'alert_hide';
} else {
    alert.className = 'alert_show';
}
}
```

* Eventオブジェクトは発生したイベントに関する情報をまとめたもので、イベントハンドラに設定した関数に渡される
* EventオブジェクトのcurrentTargetプロパティを使って、テキストボックスのElementオブジェクトを取得し、そのvalueプロパティから値を取り出している

| プロパティ・メソッド | 説明 |
|:----|:----|
| altKey | [Alt]キーが押されていたらtrueを返す |
| bubble | イベントが浮上(バブルアップ)中なら、trueを返す |
| button | イベントがどのマウスボタンに関するものか示します |
| cancelable | イベントの規定のアクションがキャンセル可能ならtrueを返す |
| charCode | keypressイベントで、押された文字キーを表す値(ユニコード)を示します |
| clientX | マウスポインタの水平位置を返します |
| clientY | マウスポインタの垂直位置を返します |
| ctrlKey | [Ctrl]キーが押されていたらtrueを返します |
| currentTarget | イベントが登録されているオブジェクトへの参照を返します |
| detail | イベントの詳細情報を返します。イベントの種類によって異なります |
| eventPhase | イベントの流れのうちどの段階に当たるのかを示します |
| isChar | 文字入力関連イベントならtrueを返します |
| keyCode | 文字以外のキーを含む、全てのキーのUnicode値を返します |
| layerX | 現在のレイヤー上におけるマウスポインタの相対的な水平座標を返します |
| layerY | 現在のレイヤー上におけるマウスポインタの相対的な垂直座標を返します |
| metaKey | [meta]キーが押されていたらtrueを返します |
| pageX | ページ上におけるマウスポインタの相対的な水平座標を返します |
| pageY | ページ上におけるマウスポインタの相対的な垂直座標を返します |
| screenX | スクリーン上におけるマウスポインタの水平位置を返します |
| screenY | スクリーン上におけるマウスポインタの垂直位置を返します |
| shiftKey | [Shift]キーが押されていたらtrueを返します |
| target | イベントが最初に送出されたオブジェクトへの参照を返します |
| timeStamp | イベントが生成された時刻を返します |
| type | イベントの名前を返します |
| preventDefault | イベントの規定のアクションをキャンセルします |
| stopPropagation | イベントの電波を中止します |

## まとめ

* 「display:none」というCSSプロパティを設定すると、HTMLの要素が非表示になる
* コントロールがフォーカスを得るとfocusイベントが、失うとblurイベントが発生する
* キーを押したときはkeyup、失うとblurイベントが発生する
* イベントの情報はEventオブジェクトに格納されている
