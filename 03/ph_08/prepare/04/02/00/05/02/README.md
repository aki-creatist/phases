# Integerクラス

* 主なフィールド
* コンストラクタ
* 主なメソッド

Integerクラスは、int型に対応するラッパークラス

#### 主なフィールド

* static int MAX_VALUE: intで表すことができる最大値
* static int MIN_VALUE: intで表すことができる最小値

#### コンストラクタ

* Integer(int value): valueをラップしたオブジェクトを生成する
    * 引数: value：ラップする整数値
* Integer`(String s): sが表す整数値をラップしたオブジェクトを生成する
    * 引数: s：ラップする整数値を表す数字列

`new Integer(123)`も`new Integer("123")`も、共に123をラップしたIntegerオブジェクトを生成する

#### 主なメソッド

* int compareTo(Integer anotherInteger)
    * 自身とanotherIntegerを比較する
    * 引数: anotherInteger：比較対象の整数オブジェクト
    * 戻り値: 自身の整数値 - anotherIntegerの整数値
* boolean equals(Object another)
    * 自身とanotherを比較する
    * 引数: another：比較対象オブジェクト
    * 戻り値: 自身とanotherが同じ整数値であれば真
* static int parseInt`(String s)
    * 文字列sを整数に変換する
    * 引数: s：変換対象の文字列
    * 戻り値: sを整数に変換した値
    * 例外: NumberFormatException：sが整数に変換できない文字列である場合
* perseIntは文字列を整数に変換するメソッドで、特に入出力処理に用いる
* Javaでは数値は文字列で入力されるため、処理に際してこれを整数に変換しなければならないため
* 変換対象の文字列は数字のほか、負数を表す`-`記号が許されるが、それ以外の文字が含まれていた場合にはNumberFormatException例外を投げる
* static int perseInt(String s, int radix)
    * 文字列sをradix進数の数字列とみなして整数に変換する
    * 引数: s：変換対象の文字列: radix：基数
    * 戻り値: sを整数に変換した値
    *  NumberFormatException：sが整数に変換できない文字列である場合
* String toString()
    * 自身がラップする整数値の文字列形式を返す
    * 戻り値: 自身の文字列形式
* static String toString(int i)
    * 整数iの文字列形式を返す
    * 引数: i：文字列に変換する整数値
    * 戻り値: iの文字列形式
* static String toString`(int i, int radix)
    * 整数iをradix進数に変換した文字列形式を返す
    * 引数: i：文字列に変換する整数値: radix：基数
    * 戻り値: iの文字列形式(radix数)

```text
toString()にはstaticでないメソッドと、staticなメソッドがあることに注意
staticでないメソッドは、これまで述べたオブジェクトの基本メソッドで、文字列表現が必要な時に自動的に呼び出されるもの
staticなtoString()は、parseIntとついになるメソッドで、引数に指定した値を文字列に変換する
(staticな)toStringとparseIntを使えば、数字と文字列の相互変換を行うことが可能
```

* 以下のメソッドは、ボクシング/アンボクシング時に自動的に用いられるもの
    * 明示的に呼び出す機会はほとんどない
    * ただし、ボクシン/アンボクシングを理解しておくためにも、このようなメソッドが存在することをぜひ知っておく
* int intValue(): 自身がラップするint型の値を返す
* static Integer valueOf( int i ):  整数値iをラップするInteger型のオブジェクトを返する
    * [Sameple](SampleWrapper02.txt)