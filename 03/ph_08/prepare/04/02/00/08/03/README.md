# Set

* 概要
* 主な実装クラス及びコンストラクタ
* (HashSetのコンストラクタ)
* (TreeSetのコンストラクタ)
* 主なメソッド

## 概要

* Setは集合をモデル化した入れ物で、インデックスのような管理番号を持たない
* また、重複要素(`equals()`で等しいと判断する要素)を持つこともできない
* `要素を重複なく格納する`ための、ごく単純な入れ物

## 主な実装クラス及びコンストラクタ

Setを実装する主要なクラスには、以下がある

* HashSet<E>
    * 要素の順序を保証しないクラス
* TreeSet<E>
    * 要素の順序を保証するクラス

```text
TreeSetが保証する順序は、要素の持つ`compareTo()`による順序(自然順序)
これ以外の順序付けを行いたいのであれば、`compare()`を実装したComparatorをコンストラクタで指定する
```

## (HashSetのコンストラクタ)

* HashSet()
    * 空のセットを作成する
* HashSet(Collection<? extends E> c
    * cに含まれる全要素を格納したセットを作成する

## (TreeSetのコンストラクタ)

* TreeSet()
    * 空のセットを作成する
* TreeSet(Collection<? extends E> c
    * cに含まれる全要素を格納したセットを作成する
* TreeSet(Collection<? super E> Comparator
    * コンパレータに従って順序付けされる空のセットを作成する

## 主なメソッド

* boolean add(E e)
    * 要素eをセットに追加する
    * 引数: e:追加する要素
    * 戻り値: true:正しく追加できた場合false:eと重複する要素が既に格納されていた場合
    * 例外:  ClassCastException:eが比較可能でない場合NullPointerException:eがnullであり、nullを比較できない場合
    * 例外は共に順序に関わるもので、HashSetを用いた場合にはこれらの例外は生じない
* boolean remove(object o)
    * oと同じ要素があればセットから削除する
    * 引数: o:削除要素
    * 戻り値: true:正しく削除した場合false:oと同じ要素がセットに存在しない場合
    * 例外: ClassCastException:eが比較可能でない場合NullPointerException:eがnullであり、nullを比較できない場合

例外は共に順序に関わるもので、HashSetを用いた場合にはこれらの例外は生じない

* int size() :
    * セット内の要素数を返する
    * 戻り値: 要素数

[Sample](SampleCollectionList02.txt)