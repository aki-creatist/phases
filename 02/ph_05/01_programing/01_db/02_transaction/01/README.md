# トランザクションアイソレーションレベル

* 複数のトランザクションが同時に実行された場合に、お互いの`トランザクションの見え方`をレベルで指定するもの

## トランザクションの見え方

* サーバーシステムは同時に来たリクエストを処理するために以下ように処理を行わせる
    * [スレッド](01_thread)を割り当てたり
    * [プロセス](02_process)を起動したり
* いずれも並列して処理が可能
* [見え方](03_read)
* [ロック](04_lock)

## 定義

トランザクション間でコミットの有無によってデータがどのように見えるのかを指定するもの

* READ_UNCOMMITTED
    * UNCOMMITTEDなデータもREADできてしまう
    * 他のトランザクションがコミットしてないデータの更新も参照できることを意味する
        * コミットされていないデータの更新は不整合で、不確定
    * ダーティリードが発生する
* READ_COMMITTED
    * コミットしていないデータは、他のトランザクションからは参照できない
    * COMMITEDなデータをREADできるということ
    * ダーティリードは発生しない
* REPEATABLE_READ
* SERIALIZABLE

## 概要

* 多くのDB製品では、REPEATABLE_READとSERIALIZABLEを実現するために処理時間とリソースを消費する
    * これは、コミットされたデータも、トランザクション単位でデータのコピーを管理する必要があるため
* トランザクションでのDB操作を工夫することで、同じデータを複数回参照する必要をなくすことができる
    * 1回参照したデータを、トランザクションが終わるまで`メモリの中に保持`していればよい
    * ほとんどのプログラムではアイソレーションレベルをREAD_COMMITTEDにすればよい
        * 実際、多くのDB製品のアイソレーションレベルのデフォルト値は、READ_COMMITTED
            * HibernateでもデフォルトはREAD_COMMITTED
* アイソレーションレベルは、他のトランザクションが更新したデータをどのように見えるかを制御するためのもの
* アイソレーションレベルは見え方を制御するだけ
    * データを他のトランザクションが更新することを制御することはできない
        * ロックが必要になる

## 一覧

<table border="1">
    <tr>
        <th rowspan="2" align="left" valign="top">種類</th>
        <th rowspan="2" valign="top">Transaction</th>
        <th colspan="3" align="center">アイソレーションレベル</th>
    </tr>
    <tr>
        <th>Dirty</th>
        <th>Non-Repeatable</th>
        <th>Fantom</th>
    </tr>
    <tr>
        <td>NONE</td>
        <td>なし</td>
        <td>発生する</td>
        <td>発生する</td>
        <td>発生する</td>
    </tr>
    <tr>
        <td>READ_UNCOMMITTED</td>
        <td>あり</td>
        <td>発生する</td>
        <td>発生する</td>
        <td>発生する</td>
    </tr>
    <tr>
        <td>READ_COMMITTED</td>
        <td>あり</td>
        <td>発生する</td>
        <td>発生する</td>
        <td>発生する</td>
    </tr>
    <tr>
        <td>REPEATABLE_READ</td>
        <td>あり</td>
        <td>発生しない</td>
        <td>発生しない</td>
        <td>発生する</td>
    </tr>
    <tr>
        <td>SERIALIZEBLE</td>
        <td>あり</td>
        <td>発生しない</td>
        <td>発生しない</td>
        <td>発生しない</td>
    </tr>
</table>
