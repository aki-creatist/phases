# オブジェクトとインスタンス

new演算子を使ってオブジェクトのインスタンスを作成する

new演算子によって、メモリ空間内にインスタンスが誕生し、どこからも注目されていないと消えてしまう。

## オブジェクトと変数の関係

* new演算子で作成したDateインスタンスを作成
    * インスタンス作成と同時に`変数に代入`する
    * 参照されていないインスタンスは、自動的に削除されてしまう
* 繰り返し処理の中にnew演算子を書くと、繰り返した回数だけインスタンスが作られる
    * 一つの変数に新しいDateインスタンスを代入すると、前のDateインスタンスは変数から切り離される
    * 一定時間後に削除される
    * インスタンスを大量に作成すると、メモリが不足してWebブラウザの動作が不安定になる
    * 繰り返し処理の前にインスタンスを作成し、繰り返し処理の中ではsetterにより値を上書きするのが好ましい
* 変数間で代入した時の結果が異なる
    * 数値やテキストなどの基本型
        * 変数間の代入はコピーになる
            * 変数dから変数eに数値を代入してから変数dの内容を変更しても、変数eの内容に変化はない
    * オブジェクトのインスタンス
        * 「どのインスタンスを参照しているか」という情報がコピーされる
        * 参照型を代入した状態で変数間の代入を行うと、同じインスタンスを参照した状態になる
        * インスタンスは変数の中に入っているのではなく、変数から参照されている
        * `参照型`と呼ばれる

```javascript
var d = 100;
var e = d;
e++;                //変数eに１を加算する
document.write(d); //当然、影響がない

document.write('<br>');

var f = new Date();
var g = f;            //同じDateを参照した状態になる
g.setFullYear(2033);    //「年」を変更する
document.write(f.getFullYear());    //変数fの「年」も変更される
// 100 2033
```

## Dateオブジェクトを利用する

Dateオブジェクトを使うと日付・時刻を扱うことができる

```javascript
var 変数 = new Date();    //今日の日付
var 変数 = new Date(年, 月, 日);    //指定した日付。月は0〜11となる点に注意
var 変数 = new Date('日付を表す文字列');    //テキストから日付を作成
```

Dateオブジェクトは時刻も扱うので、次のように時間も指定可能

```javascript
var 変数 = new Date(年数,月数,日数,時,分,秒);
var 変数 = new Date(ミリ秒);    //1970年1月1日0時0分0秒からの経過ミリ秒
```

## カレンダーの作成

### HTML

* calendar.html

```html
<!doctype html>
<html>
<head>
    <meta charset="UTF-8">
    <title>カレンダー</title>
    <script src="calendar.js"></script>
    <style>
        table{border:solid 1px; border-spacing:0px;}
        th,td{border:solid 1px; padding:4px; text-align: center;}
    </style>
</head>
<body>
<script>
    writeCalendar(2018, 1);
</script>
</body>
</html>
```

### JS

* calendar.js

```javascript
/**
 * 年(year)と月(month)を受け取って、10列×4行の表を作成
 * @param year
 * @param month
 */
function writeCalendar(year, month)
{
    var weekday = ['日', '月', '火', '水', '木', '金', '土'];
    document.write('<table>\n');
    var d = new Date(year, month-1, 0); // Dateインスタンスの作成
    for (var y = 0; y < 4; y++) {
        document.write('<tr>');
        for (var x = 0; x < 10; x++) {
            var oldt = d.getTime(); // Dateオブジェクトから指定日時のタイムスタンプを取得
            d.setTime(oldt + 24 * 60 * 60 * 1000); // ループごとに1日分を加算
            document.write('<td>');
            document.write((d.getMonth()+1) + '/' + d.getDate() + '<br>' + weekday[d.getDay()]);
            document.write('</td>');
        }
        document.write('</tr>\n');
    }
    document.write('</table>\n');
}
```