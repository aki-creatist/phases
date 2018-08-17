# CakePHP

## cake bakeコマンドについて

* beke
    * 実際に稼働するコードを作成可能
    * CakePHPで必要となる様々なソースコードを自動生成するためのツール
    * cakeコマンドのオプションとして用意されている

## Bakeの起動

### BakeによるMVC自動生成の流れ

* CakePHP3.xでは使用方法が異なる
    * [CakePHP2.x](01_cake2)
    * [CakePHP3.x](01_cake3)

## 実行結果

### Model

* MeetingRoomの実行結果
    * MeetingRoom hasMany Meeting
* Meetingの実行結果
    * Meeting belongsTo MeetingRoom
    * Meeting hasAndBelongsToMany Member
* MeetingsMemberの実行結果
    * MeetingsMember belongsTo Meeting
    * MeetingsMember belongsTo Member
* Memberの実行結果
    * Member hasAndBelongsToMany Meeting
    
### Controller

* MeetingRoomsの実行結果
    * Paginator, Session, Flash
* Meetingsの実行結果
    * Paginator, Session, Flash
* MeetingsMembersの実行結果
    * Paginator, Session, Flash
* Membersの実行結果
    * Paginator, Session, Flash
