# x△○◎の4つに分類

特に**△と○**の判断は注意

* `◉`: 確実にコンピュータ支援する
* `×`: コンピュータ支援しない
* `○`: できるだけコンピュータ支援する
* `△`： 無理にコンピュータ支援しない
    * 主に例外処理
        * 例外処理は後回しにすべき
        * 例外処理の要件には、ー般的な処理の何倍もの要求事項が折り重なっている
        * 検討の初期に、判断要素を口頭で列挙された段階では「なんとかなりそう」と思いがち
            * いざ詳細設計の段階で仕様を詰めようとすると、要求自体に矛盾がある場合がほとんど
        * 例外処理における具体的な条件の組み合わせごとに判断結果の分岐がどうなるかなどはコンピュータ支援しない
        
| | 判断要素: 複雑 | 判断要素: 単純 |
|:----|:----|:----|
| 電子データ化の価値：大 | △ | ◉ |
| 電子データ化の価値：小 | × | ○ |

* 判断要素
    * 複雑の例
        * 「その月の営業成績を加味し、セールスマンと店長の裁量の範囲で、過去の取引実績に応じた割引を行う」
        * 保険の契約
            * 下記の諸々の事情を総合的に判断
                * 年齢や性別といった明確な条件
                * 顧客のライフステージ、趣味、嗜好、将来の希望
            * 判断に応じてお勧めする商品や必要な補償額、保険金の受け取り方などを決める必要がある

