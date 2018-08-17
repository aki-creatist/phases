# Cloud Design Pattern

* 基本パターン
* 可用性向上パターン
* 動的コンテンツの処理パターン
* 静的コンテンツの処理パターン
* データアップロードのパターン
* リレーショナルデータベースのパターン
* 非同期処理/バチ処理のパターン
* 運用保守のパターン
* ネットワークのパターン

## 基本パターン

| 名称 | 概要 |
|:-----------|:------------|
| Snapshot | データのバックアップ |
| Stamp | サーバの複製 |
| Scale Up | 動的なサーバのスペックアップ/ダウン |
| Scale Out | サーバ数の動的増減 |
| Ondemand Disk | 動的なディスク容量の増減 |

## 可用性向上パターン

| 名称 | 概要 |
|:-----------|:------------|
| Multi-Server | サーバの冗長化 |
| Maulti-Datacenter | データセンターレベルの冗長化 |
| Floating IP | IPアドレスの動的な移動 |
| Deep Health Check | システムのヘルスチェック |
| Routing-Based HA | ルーティングによる接続先の透過的な切り替え |

## 動的コンテンツの処理パターン

| 名称 | 概要 |
|:-----------|:------------|
| Clone Server | サーバのクローン |
| NFS Sharing | 共有コンテンツの利用 |
| NFS Replica | 共有コンテンツの複製 |
| State Sharing | ステート情報の共有 |
| URL Rewriting | 静的コンテンツの退避 |
| Rewrite Proxy | URL書き換えプロキシーの設置 |
| Cache Proxy | キャッシュの設置 |
| Scheduled Scale Out | スケジュールに合わせたサーバ増減 |
| IP Pooling | 接続許可済みIPアドレスのプール |

## 静的コンテンツの処理パターン

| 名称 | 概要 |
|:-----------|:------------|
| Web Storage | 可用性の高いインターネットストレージ活用 |
| Direct Hosting | インターネットストレージで直接ホスティング |
| Private Distribution | 特定ユーザへのデータ配布 |
| Cache Distribution | ユーザの物理的に近い位置へのデータ配置 |
| Rename Distribution | 変更遅延のない配信 |
| Private Cache Distribution | CDNを用いたプライベート配信 |
| Latency Based Origin | 地域によりコンテンツの配信元のサーバを変更 |

## データアップロードのパターン

| 名称 | 概要 |
|:-----------|:------------|
| Write Proxy | インターネットストレージへの高速アップロード |
| Storage Index | インターネットストレージの効率化 |
| Direct Object Upload | アップロード手順の簡略化 |

## リレーショナルデータベースのパターン

| 名称 | 概要 |
|:-----------|:------------|
| DB Replication | オンラインDBの複製 |
| Read Replica | 読み込み専用レプリカによる負荷分散 |
| Inmemory DB Cache | 頻度の高いデータのキャッシュ化 |
| Sharding Write | 書き込みの効率化 |

## 非同期処理/バッチ処理のパターン

| 名称 | 概要 |
|:-----------|:------------|
| Queuing Chain | システムの疎結合化 |
| Priority Queue | 優先順位の変更 |
| Job Observer | ジョブの監視とサーバの追加・削除 |
| Fanout | 複数種類の処理を非同期かつ並列に実行 |

## 運用保守のパターン

| 名称 | 概要 |
|:-----------|:------------|
| Bootstrap | 起動設定の自動取得 |
| Cloud DI | 変更が多い部分の切り出し |
| Stack Deployment | サーバ群立ち上げのテンプレート化 |
| Server Swapping | サーバの移行 |
| Monitoring Integration | モニタリングツールの一元化 |
| Weighted Transition | 重み付けラウンドロビンDNSを使った移行 |
| Log Aggregation | ログの集約 |
| Ondemand Activation | メンテナンス時の一時的な設定変更 |

## ネットワークのパターン

| 名称 | 概要 |
|:-----------|:------------|
| Backnet | 管理用ネットワークの設置 |
| Functional Firewall | 階層的アクセス制限 |
| Operational Firewall | 機能別アクセス制限 |
| Multi Load Balancer | 複数ロードバランサーの設置 |
| WAF Proxy | 高価なWeb Application Firewallの効率的な活用 |
| Cloud Hub | VPN拠点の設置 |
| Sorry Page | バックアップサイトへの自動切り替え |
| Self Registration | 自分の情報をDBに自動登録 |
| RDP Proxy | Proxyを利用した管理コンソールのFirewall越し接続 |
| Floating Gateway | クラウド上のネットワーク環境の切り替え |
| Shared Service | システム共通サービスの共用化 |
| High Availability NAT | 冗長化されたNATインスタンス |