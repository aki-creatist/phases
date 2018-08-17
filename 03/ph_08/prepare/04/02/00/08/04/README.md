# Map

* 概要
* 主な実装クラス及びコンストラクタ
* HashMapコンストラクタ
* TreeMapのコンストラクタ
* 主なメソッド

## 概要

* Mapは入れ物というよりも`キー(Key)と値(value)との対応表`
* なお、キーも値も共にオブジェクトの実体
* キーを指定した取り出しなど、オブジェクトをキーで管理することが可能
* 値は複数のキーに対応づけることが可能が、キーは一つの値にしか対応不可
    * キーというと、何らかの管理番号のようなものを想像しがちだが、そう限ったものではない
    * 例えば、キーに英単語、値に日本語を関連づけてマップに記録する場合、英和辞典を作ることが可能
    * キーと値をひっくり返せば、和英辞典の出来上がり
    * 英和辞典や和英辞典はMapを説明する例としてよく用いられる
        * それもそのはず、Mapの前身はDictionaryという名の抽象クラスだったため

## 主な実装クラス及びコンストラクタ

Mapを実装する主要なクラスには、以下がある

* HashMap<K, V>
    * 要素の順序を保証しないクラス
* TreeMap<K, V>
    * 要素の順序を保証するクラス

HashMapとTreeMapの違いはSetと同じなので省略する

## HashMapコンストラクタ

* HashMap()
    * 初期容量16で空のマップを作成する
* HashMap( Map<? extends K, ? extends V> m)
    * mに含まれる全エントリを格納したマップを作成する

## TreeMapのコンストラクタ

* TreeMap()
    * 空のマップを作成する
* TreeMap(Map<? extends K,? extends V> m)
    * mに含まれる全エントリを格納したマップを作成する
* TreeMap(Comparator<? super K> comparator)
    * コンパレータに従って順序付け荒れるからのマップを作成する

## 主なメソッド

* v get(object key)
    * キーkeyに対応づけられた値を取り出す
    * 引数: key:キー
    * 戻り値: 取り出した値keyがマップになければnull
    * 例外: ClassCastException:keyが比較可能でない場合NullPointerException:keyがnullであり、nullを比較できない場合
* v put(k key, V value)
    * エントリ(key, value)をマップに登録する
    * 引数: key:キーvalue:値
    * 戻り値: これ以前にkeyに関連づけられていた値なければnull
    * 例外: ClassCastException:keyが比較可能でない場合NullPointerException:keyがnullであり、nullを比較できない場合

```text
(key, value)をマップに登録するマップに同じkeyを持つ対応(key, oldValue)が存在していた場合、oldValueに置き換えてoldValueに返却する
マップにkeyが存在しない場合、(key, value)を登録してnullを返す
```

例外は共に順序に関わるもので、HashMapを用いた場合にはこれらの例外は発生しない

[Sample](SampleCollectionList03.txt)

* v remove(object key)
    * マップからkeyとの対応を削除する
    * 引数: key:キー
    * 戻り値: 削除した値なければnull
    * 例外: ClassCastException:keyが比較可能でない場合NullPointerException:keyがnullであり、nullを比較できない場合
* int size() :
    * マップ内のキー値マッピングの数を返す
    * 戻り値: キー値マッピングの数

キーとマッピングの数とは、キーから見た対応数のことで、平たく言えば`マップに登録されたキー数`

* int size():
    * マップ内のキー値マッピングの数を返す
    * 戻り値: キー値マッピングの数
* set<k> keySet():
    * マップ内のキーを全て含むセットを返す
    * 戻り値: マップに含まれるキーのセット

マップ内に登録されている全てのキーをセットとして見ることが可能セットはマップと連動しているので、それぞれの変更は他方に反映される

[Sample](SampleCollectionList04.txt)