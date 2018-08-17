<?php
class SessionController
{
    protected $セッション名;
    public function __construect()
    {
    }
    public function setSessName($name)
    {
        $this->セッション名 = $name;
    }
    public function getSessName()
    {
        return $this->セッション名;
    }
    /**
     * セッションを開始する
     */
    public function start()
    {
        // セッションの状態を確認
            // セッションが既に開始している場合は何もしない
        // セッション名のセット セッション名の変更はセッション開始の前にする必要がある
        // セッション開始
    }
    /**
     * セッション変数を破壊する
     */
    public function logout()
    {
        // セッション変数を空にする
        // クッキーを削除
        // セッションを破壊
    }
}