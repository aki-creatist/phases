# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
        . ~/.bashrc
fi

# User specific environment and startup programs

PATH=$PATH:$HOME/.local/bin:$HOME/bin

#anyenv
if [ -d $HOME/.anyenv ] ; then

    # $PATHにディレクトリ名を格納
    export PATH="$HOME/.anyenv/bin:$PATH"

    # 初期設定を行うコマンドを追記
    eval "$(anyenv init -)"

fi