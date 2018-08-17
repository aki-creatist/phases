<?php
class AuthController extends Database
{
    const TABLE = 'members';
    private $認証情報の格納先名;
    /**
     * 値を取り替えられるようにで内部の変数に設定
     */
    public function setAuthName($name)
    {
        $this->認証情報の格納先名 = $name;
    }
    /**
     * メソッドでその変数に設定した名前を取り出す
     * これは管理者側でもこのクラスを利用可能にするため
     */
    public function getAuthName()
    {
        return $this->認証情報の格納先名;
    }
    /**
     * 認証の証拠を確認する
     */
    public function check()
    {
        //`認証情報の格納先名` で設定された配列名を取得
        //このセッション変数に1以上の数値があればtrueが返す
    }
    public function getUser($username)
    {
    }
    /**
     * 入力されたパスワード`$password`をハッシュ値にする
     */
    public function getHashedPW($password)
    {
        //コストパラメーターとして2桁の数字を設定する
        //ソルトを作成するため関数でランダムなデータを生成
        //さらに`base64_encode`で文字列を半角の英数字列にする (`+`が入る)
            //そのため`strstr関数`で `.` に変換する
        //ハッシュ値を生成する
    }
    public function checkPW($password, $hashed_password)
    {
        //パスワードとハッシュ値を引数として渡す
    }
    /**
     * セッションIDを再発行し、セッションハイジャックを排除
     */
    public function authOK($userdata)
    {
    }
    public function authNG()
    {
    }
}