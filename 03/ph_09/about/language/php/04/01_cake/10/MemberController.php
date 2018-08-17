<?php
// Cake 2.x
// 変数の値は、「コントローラクラスで特に指定をしなかった場合の初期値

App::uses ( 'AppController', 'Controller' );

class MembersController extends AppController {

// このコントローラで使用する主なモデルクラス名
// 初期値(true)ならコントローラ名と同名のモデルを指定したのと同じ振る舞い(falseならモデルを使用しません)
    public $uses = ture;

// このコントローラで使用するHelperの名前。(Helperクラス名から「Helper」を除いたもの)
// 何も指定しなくてもHtmlhelperとFormHelperは呼び出されるので、public $helpers = array( 'Html', 'Form' );と指定したのと同じ振る舞い。
    public $helpers = array();

// このコントローラで使用するComponentの名前(Componet
// クラス名から「Component」を除いたもの)
    public $components = array( 'Paginator', 'Session', 'Flash' );

// ブラウザからのHTTPリクエストに関する情報が格納される
    public $request;

// アクションの処理終了後に表示される画面ファイルの名前
// 指定しなければ「/app/View/コントローラ名/アクション名.ctp」が呼び出される
    public $view = null;    // (自動的にアクション名がセットされる)

// 表示される画面のレイアウトファイルの名前。特に指定しなければ「/app/View/Layouts/default.ctp」が呼び出される
    public $layout = 'default';
}