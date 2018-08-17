# List

* 概要
* 主な実装クラス及びコンストラクタ
* (ArrayListのコンストラクタ)
* (LinkedListのコンストラクタ)
* 主なメソッド

## 概要

* Listには、0から始まるインデックスが付いている
* インデックスは配列で言えば添字に相当する番号
    * これを指定した要素の追加や取り出し、削除などを行うことも可能

## 主な実装クラス及びコンストラクタ

Listを実装する油商なクラスには以下がある

* ArrayList<E>
    * 配列で実装するクラスインデックスを用いた要素の参照(取り出し)を高速に行える
* LinkedList<E>
    * リスト構造で実装するクラス要素の追加や削除に伴う負荷が小さい

主なコンストラクタを示する

## (ArrayListのコンストラクタ)

* ArrayList()
    * 初期サイズ10でからのリストを作成する
* ArrayList(Collection<? extends E> c)
    * cに含まれる全要素を格納したリストを作成する

初期要素が格納されたリストを作成するためには、初期要素のコレクションを引数にコンストラクタを実行する引数の

```text
Collection <? extends E>
```

は、EまたはEのサブクラスを要素とするコレクション(ListやSet)を意味する

## (LinkedListのコンストラクタ)

* LinkedList
    * 空のリストを作成する
* LinkedList(Collection<? extends E> c)
    * cに含まれる全要素を格納したリストを作成する

```text
引数のないコンストラクタを呼び出した時、ArrayListは初期サイズ10の空リストを作成し、LinkedListは初期サイズ０の空リストを作成する
この初期サイズの有無は、Javaのメモリ管理に関係するもので、利用にあたって特に意識する必要はない
```

## 主なメソッド

* boolean add(E e)
    * 要素eをリストの最後に追加する
* 引数: e:追加する要素
    * 戻り値: 常にtrue

要素eをリストの最後に追加する使用上は不具合を例外で通知することになっているが、ArrayListやLinkedListで例外が生じることはない

* void add(int index, E e)
    * 要素eをindexで指定した位置に挿入する
    * 引数: index:挿入位置のインデックスe:追加する要素
    * 例外: IndexOutOfBoundsException:インデックスが範囲外の場合

要素eを指定した位置に挿入する挿入位置以降の要素は自動的に後ろにずれる

* E get(int index)
    * 位置indexにある要素を取り出する
    * 引数: index:要素の位置
    * 戻り値: 指定位置にある要素
    * 例外: IndexOutOfBoundsException:インデックスが範囲外の場合

位置indexにある要素を取り出するただし、取り出した要素がリストからなくなるわけではなく指定位置の要素を参照するだけ

* E remove(int index)
    * 位置indexにある要素を削除する
    * 引数: index:削除要素の位置
    * 戻り値: 削除した要素
    * 例外: IndexOutOfBoundsException:インデックスが範囲外の場合

位置indexにある要素を削除する削除位置以降の要素は自動的に前に詰められる

* int size()
    * リスト内の要素数を返す
    * 戻り値: 要素数

リストに格納された要素数を返す
要素数がint型の最大値より大きい場合には、int型の最大値を返す

[Sample](SampleCollectionList01.txt)