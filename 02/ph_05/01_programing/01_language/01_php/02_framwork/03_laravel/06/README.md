# Modelチェック

## tinkerコマンド

* tinkerコマンドでモデルの記述コードをチェック可能
* 実際にLaravel内で記述するコードをコマンドから確認

```bash
#tinkerコマンド開始
php artisan tinker
#tinker実行
// peopleテーブル全件取得
>>> $all = App\Person::all();

// peopleテーブルのid=1のデータをGET(取得)する
>>> $name = App\Person::where('id',1)->get();

// nameがaaaaのデータをGET(取得)する
>>> $name = App\Person::where('name','aaaa')->get();

// peopleテーブルの年齢が20( age=20)でidが最新順で、10件のみGET(取得)する
// ※tinkerコマンドは１行なので、横つながりに直してから実行。
>>> $get = App¥Person::where('age', 20)
                        ->orderBy('id', 'desc')
                        ->take(10)
                        ->get();

// peopleテーブルのid=1飲み取得１(データがない場合はnullを返す) 
>>> $get=App\Person::find(1);

// peopleテーブルのid=1飲み取得１(データがない場合はnullを返す) 
>>> App\Person::where('id', 19)->first();
※id=1が複数あった場合、最初の１レコードを取得する
```

あとは以下のサイトを参考に

* [Eloquetモデルの集計関数](https://laravel.com/docs/5.4/eloquent#retrieving-aggregates)
* [Eloquentモデルのリレーション](https://laravel.com/docs/5.4/eloquent-relationships)
* [QueryBuilerからクエリ発行](https://laravel.com/docs/5.4/queries#introduction)
* [QueryBuilderの集計関数](https://laravel.com/docs/5.4/queries#aggregates)
* [QueryBuilderJOIN](https://laravel.com/docs/5.4/queries#joins)
