# ruby

## 引数の取り方

option_parser.rb

```
require 'optparse'

option = {}
OptionParser.new do |opt|
    opt.on('-a', '1文字オプション 引数なし') { |v| option[:a] = v}
    opt.on('-b VALUE', '1文字オプション 引数あり(必須)') { |v| option[:b] = v}
    opt.on('-c credentials.json', 'credentials.json file') { |v| option[:credentials] = v }
    opt.parse!(ARGV)
end
p option
```

実行

```bash
ruby option_parser.rb -a test1 -b test2 -c test.json
```

## module_class_def

class.rb

```
module Sprocket
  class RedshiftImportCommand
    def setup
      'diameter'
    end
  end
end

p Sprocket::RedshiftImportCommand.new.setup

```

```bash
ruby class.rb
```

## Test

[参考](https://qiita.com/luckypool/items/e3662170033347510c3c)

```bash
sudo gem install rspec
cd {rubyのプロジェクトディレクトリ}
rspec --init
```

```bash
mkdir spec/lib
touch spec/lib/dog_spec.rb
```

```
require 'spec_helper'
require 'dog'

describe Dog do
  it "is named 'Pochi'" do
    dog = Dog.new
    expect(dog.name).to eq 'Pochi'
  end
end
```

```bash
mkdir lib
touch lib/dog.rb
```

```
# 単体テスト実験用のクラス
class Dog
  attr_accessor :name

  def initialize(name = 'Pochi')
    @name = name
  end
end
```

## Guardの導入

* ファイル変更の際に自動でテストが走るようにする
* rubocopで規約チェックをする

[参考](http://ruby-rails.hatenadiary.com/entry/20141019/1413698128)

### 想定する構成

```text
.
├── Gemfile
├── Gemfile.lock
├── Guardfile
├── lib
│   └── dog.rb
└── spec
    ├── lib
    │   └── dog_spec.rb
    └── spec_helper.rb
```

### 事前準備

```bash
#bundleを実行するためにbundlerをインストール
sudo gem install bundler
bundle -v

#画面上に警告を出してくれる
brew install terminal-notifier
```

### Gemfile作成

```bash
touch Gemfile
```

```
# Gemfile
group :development do
  gem 'rubocop'
  gem 'guard-rubocop'
  gem 'terminal-notifier-guard'
end
```

```bash
bundle install

guard init rubocop #Guardfileが生成される
```

```bash
bundle exec guard
# 終了時はexit
```

## 規約の設定

[参考](https://blog-ja.sideci.com/entry/2015/03/26/103000)

```bash
touch .rubocop.yml
```

```yaml
# Use only ascii symbols in comments.
AsciiComments:
  Enabled: false
Style/BlockComments:
  Enabled: false
Style/Documentation:
  Enabled: false
Style/RegexpLiteral:
  Enabled: false
```

