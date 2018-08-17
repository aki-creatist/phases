//主なセッションコンポーネントのメソッド

/**
* /lib/Cake/Controller/Component/SeesionComponent.php
*
*セッションに情報を保存する
*
* @param string $name セッションキー名階層構造にするには
*        `Aaa.key1`のようにピリオドで区切る
* @param string $value セッションに保存する値
* @return boolean 保存に成功したか
*/
public function write ($name, $value = null) {}

/**
* セッションに情報を取得する
*
* @param string $name セッションキー名保存してある情報が
*        配列などで階層構造になっている場合は、`Aaa.key1`の
*        のようにピリオドで区切ることで深い階層の情報も取得可能
*
* @return mixed 取得した情報
*/
public function read ($name = null) {}

/**
* セッションに保存している情報を削除する
*
* @param string $name セッションキー名
* @return boolean
*        true    :    セッションキーが存在して削除できた場合
*        false    :    セッションキーが存在しなかった場合
*/
public function delete ($name) {}

/**
* セッションキー名が存在するかどうかチェックする
*
* @param string $name セッションキー名
* @return boolean 存在するかどうか
*/
public function check ($name) {}