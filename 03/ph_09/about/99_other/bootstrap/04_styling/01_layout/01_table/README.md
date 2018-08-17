# テーブルレイアウト

* tableタグで表の結合を駆使してレイアウト
    * メリット: レイアウトが崩れにい
    * デメリット: ソースコードの可読性が悪い

```html
<table border"1" style="width:100%">
<tr>
    <td colspan="2">
        <h4>サイト名</h4>
        <p>ヘッダー</p>
    </td>
</tr>
<tr>
    <td style="width:25%">
        <h4>サイドバー</h4>
        <ul>
            <li>リンク１</li>
            <li>リンク２</li>
            <li>リンク３</li>
        </ul>
    </td>
    <td>
        <!-- ここがメインコンテンツ-->
        <h4>メインコンテンツ</h4>
        <p>本文</p>
    </td>
</tr>
<tr>
    <td colspan="2">
        <h4>フッター</h4>
        <p>フッター</p>
    </td>
</tr>
</table>
```
