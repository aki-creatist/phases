FROM centos:centos7

# sysconfig network
RUN echo "NETWORKING=yes" > /etc/sysconfig/network

RUN yum -y install epel-release.noarch

# yum
RUN yum update -y
RUN yum install -y passwd
RUN yum install -y sudo
RUN yum install -y gcc
RUN yum install -y gcc-c++
RUN yum install -y make
RUN yum install -y vim
RUN yum install -y git
RUN yum install --enablerepo=epel -y mosh
RUN yum install -y openssl-devel
RUN yum install -y zlib-devel
RUN yum install -y readline-devel
RUN yum install -y bzip2-devel
RUN yum install -y libevent-devel
RUN yum install -y openssh
RUN yum install -y openssh-server
RUN yum install -y openssh-clients
RUN yum install -y cmake
# for ruby install
RUN yum install -y bzip2
# apache
RUN yum -y install httpd

# ssh
RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config
RUN sed -ri 's/#UsePAM no/UsePAM no/g' /etc/ssh/sshd_config
#公開鍵認証を許可する
RUN sed -i -e "s/#PubkeyAuthentication/PubkeyAuthentication/g" /etc/ssh/sshd_config

# user
RUN useradd python_spameggs
RUN echo 'foo' | passwd --stdin python_spameggs

# sudo
RUN echo 'python_spameggs ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers.d/python_spameggs

# timezone
RUN cp -p /usr/share/zoneinfo/Japan /etc/localtime

USER python_spameggs
WORKDIR /home/python_spameggs
# anyenv
RUN git clone https://github.com/riywo/anyenv .anyenv
ENV HOME /home/python_spameggs
RUN echo 'export PATH="${HOME}/.anyenv/bin:${PATH}"' >> .bash_profile
RUN echo 'eval "$(anyenv init -)"' >> .bash_profile

# anyenv update
RUN mkdir -p .anyenv/plugins
RUN git clone https://github.com/znz/anyenv-update.git .anyenv/plugins/anyenv-update

EXPOSE 22

USER root

RUN yum install -y chromium

COPY ./.bash_profile /home/python_spameggs/.bash_profile

RUN /bin/bash -l -c 'anyenv install nodenv'
RUN /bin/bash -l -c 'nodenv install 0.12.7'
RUN /bin/bash -l -c 'nodenv global 0.12.7'
RUN /bin/bash -l -c 'nodenv rehash'
RUN /bin/bash -l -c 'npm install -g karma@~0.12.31'

RUN systemctl enable httpd
RUN systemctl enable sshd
CMD ["/sbin/init"]
#CMD ["/usr/sbin/sshd", "-D"]

# ssh起動
#systemctl start sshd.service