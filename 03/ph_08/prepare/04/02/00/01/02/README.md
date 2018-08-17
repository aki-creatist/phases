# StringBufferクラス

* 概要
* コンストラクタ
* 主なメソッド
* Stringクラスと同じ機能を持つメソッド
* 追加メソッド
* 挿入メソッド
* 削除メソッド
* その他のメソッド

## 概要

* StringBufferクラスは下辺の文字列を表すクラスで、追加/挿入/削除のような`文字列を加工する処理`を実行することが可能
* 加工用の予備領域を持つバッファ月の文字列
* 同じような下辺文字列を表すクラスにStringBuilderクラスがあるが、StringBuffer/StringBuiderは、同期をとる/とらないの違いしかない
* StringBufferは同期を取るため、マルチスレッド環境下では不具合が生じる恐れがあるが、StringBufferに比べて高速に動作する
* そのため、マルチスレッドではない環境ではStringBuilderの方が有利
* StringBuffer/StringBuilderは同じコンストラクタ、メソッドを保つため、StringBufferクラスのみ説明

## コンストラクタ

* よく用いられるコンストラクタ
    * StringBuffer()
        * 空の下辺文字列を生成する
    * StringBuffer(String str)
        * strの内容で初期化された下辺文字列を生成する

## 主なメソッド

## Stringクラスと同じ機能を持つメソッド

* charAt(int index)
    * indexの位置にある１文字を返却
* indexOf(String str, int fromIndex)
    * strを検索
* indexOf(String str)
    * fromIndexの位置からstrを検索
* lastIndexOf(String str)
    * 末尾から、前方に向かってを検索
* lastIndexOf(String str, int fromIndex)
    * fromIndexの位置から、前方に向かってstrを検索
* length
    * 文字列の長さ(文字数)を返却
* substring(int beginIndex)
    * beginIndexの一から始まる部分文字列を抽出
* substring(int beginIndex, int endIndex)
    * beginIndexから始まりendIndexの直前で終わる部分文字列を抽出

## 追加メソッド

追加メソッドは、文字列の末尾に引数の値(引数の文字列表現)を追加する

* StringBuffer append(int i)
    * 引数の文字列表現を自身に追加する
    * 引数: i:追加する整数値
    * 戻り値: 追加後の自身

引数の整数値を文字列表現(10進数の数字列)として自身に追加する返却値は追加後の自分自身

* StringBuffer append(charSequence s)
    * 引数の文字列を自身に追加する
    * 引数: s:追加する文字列
    * 戻り値: 追加後の自身

引数の文字列を自身に連結するsが空文字列であれば"null"を連結する

* 文字列の連結といえば、つい`+演算子`を使いたくなるが危険
    * `+`の結果はString型となり型が変わってしまう

StringBuffer型のまま連結するためには、`append()`を使用する

これら以外にも、次の`append()`が用意されている

* StringBuffer append(boolean b)
    * 真偽値bの文字列表現(true/false)を追加
* StringBuffer append(char c)
    * 文字cを追加
* String Buffer append(charSequence s, int start, int end)
    * 文字列sの部分文字列を追加
* StringBuffer append(double d)
    * 実数値の文字列表現を追加
* StringBuffer append(float f)
    * 制度の差以外はappend(double)と同じ
* StringBuffer append(long lng)
    * 整数値lngの文字列表現を追加
* StringBuffer append(object obj)
    * objの文字列表現(`toString()`の返却値)を追加

## 挿入メソッド

挿入メソッドは、文字列の指定位置に引数の値(引数の文字列表現)を挿入する

* StringBuffer insert(int index, int i)
    * 整数iの文字列表現を文字列位置indexに追加する
    * 引数: index:挿入を行う文字位置 i:挿入する整数
    * 戻り値: 挿入後の自身
    * 戻り値: StringIndexOutOfBoundsException:無効な挿入位置

引数の整数値を文字列表現(10進数の数字列)として自身の文字位置indexに挿入する
返却値は挿入後の自分自身

これら以外にも次の`insert()`が用意されている

* StringBuffer insert(int index, boolean b)
    * 真偽値bの文字列表現(true/false)を挿入
* StringBuffer insert(int index, char c)
    * 文字cを挿入
* StringBuffer insert(int index, CharSequence s)
    * 文字列sを挿入
* StringBuffer insert(int index, CharSequence s, int start, int end)
    * 文字列sの部分文字列を挿入
* StringBuffer insert(int index, double d)
    * 実数値の文字列表現を挿入
* StringBuffer insert(int index, float f)
    * 精度差以外は(int index, double d)と同じ
* StringBuffer insert(int index, long 1)
    * 整数値１の文字列表現を挿入
* StringBuffer insert(int index, Object obj)
    * objの文字列表現(`toString()`の返却値)を挿入

## 削除メソッド

削除メソッドは、文字列の一部を削除する

* StringBuffer delete(int start, int end)
    * 文字列から引数で指定された範囲を削除する
    * 引数: start:削除範囲の開始位置
        * end:削除範囲直後の位置
    * 戻り値: 削除後の自身
    * 例外: StringIndexOutOfBoundsException:無効な削除範囲

自身の文字列から`startからendの直前`の部分を削除する

これ以外にも、次の削除メソッドがある

* StringBuffer deleteCharAt(int index)
    * 位置indexの文字を削除

## その他のメソッド

* StringBuffer replace(int start, int end, String str)
    * 指定された範囲を文字列strで置換する
    * 引数: 挿入後の自身
    * 戻り値: 置換後の自身
    * 例外: StringIndexOutOfBoundsException:無効な挿入位置

StringBufferクラスの置換メソッドは、置換したい部分を文字列位置で指定可能

Stringクラスの置換メソッドとは異なり、StringBuffer型の文字列が戻される点に注意

* StringBuffer setCharAt(int index, char ch)
    * 文字位置indexの文字をchで置換する |
    * 引数: index:文字位置
        * ch:置換する文字
    * 例外: StringIndexOutOfBoundsException:無効な文字位置

これら以外にも、次のメソッドがある

* StringBuffer reverse()
    * 文字列を逆順に並べ替える