# FPTの設定ファイルの書き換え

```bash
FILE=/etc/vsftpd/vsftpd.conf

#書き換え箇所

#安全のため匿名FTP機能は無効に変更
OLD_ANONYMOUS_ENABLE='anonymous_enable=Yes'
NEW_ANONYMOUS_ENABLE='anonymous_enable=No'

##ASCIIモードでの転送を有効にする設定
##FTPにはASCIIモードとバイナリモードがある
##ASCIIモードではOSごとの改行コードの違いを自動的に調整してくれ
OLD_ASCII_UPLOAD_ENABLE='#ascii_upload_enable=YES'
NEW_ASCII_UPLOAD_ENABLE='ascii_upload_enable=YES'

OLD_ASCII_DOWNLOAD_ENABLE='#ascii_download_enable=YES'
NEW_ASCII_DOWNLOAD_ENABLE='ascii_download_enable=YES'

#IPv4での接続を待ち受けるかどうか
OLD_LISTEN='listen=No'
NEW_LISTEN='listen=Yes'

#IPv6での接続を待ち受けるかどうか
OLD_LISTEN_IPV6='listen_ipv6=YES'
NEW_LISTEN_IPV6='listen_ipv6=No'

#置き換えのコマンドをまとめる
ASCII_UPLOAD_ENABLE="s/${OLD_ASCII_UPLOAD_ENABLE}/${NEW_ASCII_UPLOAD_ENABLE}/g"
ASCII_DOWNLOAD_ENABLE="s/${OLD_ASCII_DOWNLOAD_ENABLE}/${NEW_ASCII_DOWNLOAD_ENABLE}/g"
LISTEN="s/${OLD_LISTEN}/${NEW_LISTEN}/g"
LISTEN_IPV6="s/${OLD_LISTEN_IPV6}/${NEW_LISTEN_IPV6}/g"
ANONYMOUS_ENABLE="s/${OLD_ANONYMOUS_ENABLE}/${NEW_ANONYMOUS_ENABLE}/g"

sed -i -e "${ASCII_UPLOAD_ENABLE}" ${FILE}
sed -i -e "${ASCII_DOWNLOAD_ENABLE}" ${FILE}
sed -i -e "${LISTEN}" ${FILE}
sed -i -e "${LISTEN_IPV6}" ${FILE}
sed -i -e "${ANONYMOUS_ENABLE}" ${FILE}

rm ${FILE}-e
```