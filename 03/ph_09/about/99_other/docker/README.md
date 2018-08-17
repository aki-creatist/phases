# Docker

最低限、PHPが動くAmazonlinux

```yaml
FROM amazonlinux:2017.09

RUN yum -y install yum-plugin-fastestmirror
RUN yum -y update

#OverrayFS用のバッチを当てる(yum install時のchecksumエラーを回避する)
RUN yum -y install yum-plugin-ovl

# Apache
RUN yum -y install httpd24

RUN sed -ie "s/AllowOverride None/AllowOverride All/" /etc/httpd/conf/httpd.conf && \
    sed -ie "s/Options Indexes FollowSymLinks/Options -Indexes +FollowSymLinks/" /etc/httpd/conf/httpd.conf

#PHP54
RUN yum -y install php54 php54-devel php54-mbstring php54-mysqlnd php54-pecl-apc php54-mcrypt php54-pecl-memcached php54-gd php54-pecl-imagick
RUN sed -i -e 's/;date.timezone *=.*$/date.timezone = UTC/' /etc/php.ini && \
    sed -i -e 's/;default_charset *=.*$/default_charset = "UTF-8"/' /etc/php.ini && \
    sed -i -e 's/;error_log *=.*$/error_log = php_errors.log/' /etc/php.ini

WORKDIR /var/www
ENTRYPOINT /usr/sbin/httpd -D FOREGROUND
```