# 複雑なものは分解しTo-Beへ

* 表中の右側は、`判断要素が単純な領域`
* `右側に位置づけられる部分を増やす`には、`左側の領域を分解`して構造化し、単純な要素として定義できるものを切り出す
* 現在のありのまま(`As-Is`)を受け入れるのではなく、あるべき要件の実現方法(`To-Be`)を提案する姿勢を持って望む
* また、◎と○の判断も重要
    * 例: `DWH`を構築するような案件では、なんでもかんでもDWHに取り込もうとするアプローチが後を絶たない
        * DWH: データウェアハウス（DWH）
            * 企業などの業務上発生した取引記録などのデータを時系列に保管したデータベース
        * 「なんとなく」的な発想で用途(電子データ化の価値)も確認せず「今あるものはあれもこれも保存しておきましよう」とは発想しない

| | 判断要素: 複雑 | 判断要素: 単純 |
|:----|:----|:----|
| 電子データ化の価値：大 | △ | ◉ |
| 電子データ化の価値：小 | × | ○ |