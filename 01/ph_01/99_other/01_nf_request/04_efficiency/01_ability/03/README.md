# ③詳細設計時

* パフォーマンス設計
    * `ハード × プログラム × DB`
    * 机上計算の元になるDB処理性能やCPU処理性能の基礎数値を取得
    * より明確になった機能動作内容で性能机上計算を行ってサイジングを精緻化

## 背景

* 基本設計の段階では、本番機で使うCPUは触っていない
    * 既存システムで使っているCPUとの性能の比率やTPCの数値を参考にしていた
    * DBのパフォーマンスは実際に開発してから負荷テストをして、はじめて問題に気付くことが多い

## ゴール

* [プログラム](../../../../../ph_04/01_program/02)
    * SQLを検討
    * ディスクI/Oの発生を減らす
* DBのパフォーマンス
    * ディスクI/Oを減らす
    
## 前提条件

* 基本設計時のDB論理設計で正規化されている
    * テーブルの結合(JOIN)はうまく設計しないと、データベースのパフォーマンスが低下する
    * 検索条件によっては検索の結果が返ってこないままブラウザの応答がなくなり、通信がタイムアウトしてしまう
    
## 概要

* 詳細設計に入ると性能の詳細化が行われる
    * 基本設計で行った机上計算を詳細化された機能に合わせて精緻化
    * サイジングの精緻化をさらに進めることができる

## 目的

* 開発前にパフォーマンス設計を行い、負荷テスト時の問題発生時に対応しやすくする

## 事前準備

* 開発機を用意する
    * 本番機と同じ世代のCPUが搭載されたものを選ぶ
            
## 手順

* パフォーマンステスト
* 性能確認

### パフォーマンステスト

* 開発機によるパフォーマンステスト
* パフォーマンステストでは基礎性能を計る
    * Webの処理に何秒かかるなど
        * セレクトに何秒かかるとか

### 性能確認

* 机上計算をすることでかなり正確な数値が得られる
    * 早い段階から必要にして十分な構成を知ることができる
    * 早い段階から必要にして十分な構成を知ることができる
        * 台数不足による急な追加や過剰投資など
