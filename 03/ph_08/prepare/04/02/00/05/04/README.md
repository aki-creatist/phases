# Booleanクラス

* 主なフィールド
* コンストラクタ
* 主なメソッド
* その他のラッパークラス

## Booleanクラス

Booleanクラスは、boolean型に対応するラッパークラスコンストラクタやメソッドの役割は、型の違いを除けばIntegerクラスと変わりない概要のみ掲載する

## 主なフィールド

* static Boolean FALSE: falseをラップするBooleanオブジェクト
* static Boolean TRUE: true

## コンストラクタ

* Boolean( double value ): valueをラップしたオブジェクトを生成する
* Boolean(String s): sが"true"であればtrueをラップしたオブジェクトを生成する"true"以外が指定された場合は、falseをラップする

## 主なメソッド

* int ompareTo`(Boolean anotherBoolean)
    * 自身とanotherBooleanを比較する

Booleanクラスの`compareTo()`は次の比較結果を返却する

| 自身 | anotherBoolean | 返却値 |
|:----|:----|:----|
| true | true | 0 |
| false | false | 0 |
| true | false | 整数 |
| false | true | 負数 |

* boolean equals(Boolean another)
* 自身とanotherを比較する
* static boolean parseBoolean(String s)
* 文字列sをboolean値に変換する
* String toString()
* 自身がラップするboolean値の文字列形式を返する
* static String toString(boolean b)
* boolean値bの文字列形式を返する
* boolean booleanValue()
* 自身がラップするboolean値を返する
* static Boolean valueOf(boolean b)
* boolean値bをラップするBoolean型のオブジェクトを返する

## その他のラッパークラス

* 全ての基本型変数について、それぞれの型に対応するラッパークラスが揃っている
* 従って、他にもLong、Short、Byte、Characterクラスなどが存在する
* なお、Longなど`数値系ラッパークラス`の役割は、IntegerやDoubleとほぼ変わらない
* Characterクラスは文字をラップするラッパークラスで、文字チェックを行うstaticメソッドを多く揃えている
    * ただし、一般のプログラムでは文字よりも文字列を扱う機会が多いため、省略する