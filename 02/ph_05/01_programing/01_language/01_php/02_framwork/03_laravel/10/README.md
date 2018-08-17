## 暗号化

### MD5

```php
//CakePHP3
use Cake\Utility\Security

        $md5 = Security::hash('abc', 'md5');
        print_r($md5);  // 900150983cd24fb0d6963f7d28e17f72
```

```php
//Laravel
use Hash;

        $md5 = \Hash::make('abc');
        print_r($md5);  // 900150983cd24fb0d6963f7d28e17f72
```

```php
//config/app.php
    'providers' => [
        〜中略〜
        // HashはMD5と共存できないため、コメントアウト
        //Illuminate\Hashing\HashServiceProvider::class,
        // MD5を使用したいため下記一行を追加
        App\Providers\MD5HasherServiceProvider::class,
```

```php
<?php
//app/Providers/MD5HasherServiceProvider.php
namespace App\Providers;

use Illuminate\Support\ServiceProvider;

use App\Services\MD5Hasher;

class MD5HasherServiceProvider extends ServiceProvider {

    protected $defer = true;

    public function register()
    {
        $this->app->singleton('hash', function() {
            return new MD5Hasher;
        });
    }

    public function provides()
    {
        return ['hash'];
    }
}
```

```php
<?php
//app/Service/MD5Hahser.php
namespace App\Services;

class MD5Hasher implements \Illuminate\Contracts\Hashing\Hasher {

    public function make($value, array $options = [])
    {
        return md5($value);
    }

    public function check($value, $hashedValue, array $options = [])
    {
        return (md5($value) == $hashedValue);
    }

    public function needsRehash($hashedValue, array $options = [])
    {
        return false;
    }
}
```

```bash
composer dump-autoload
```

[参考](http://www.larajapan.com/2016/01/31/%E3%83%A6%E3%83%BC%E3%82%B6%E3%83%BC%E8%AA%8D%E8%A8%BC%EF%BC%88%EF%BC%91%EF%BC%92%EF%BC%89laravel-5-2-hasher%E3%82%92%E5%A4%89%E3%81%88%E3%82%8B/)
