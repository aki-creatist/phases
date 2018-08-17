!#/bin/bash

SSH_DIR="${HOME}/.ssh"

touch config

SUB_DIR="commons local servers"

DIR=conf.d
mkdir ${SSH_DIR}/${DIR}
cd ${SSH_DIR}/${DIR}
mkdir ${SUB_DIR}

DIR=keys
mkdir ${SSH_DIR}/${DIR}
cd ${SSH_DIR}/${DIR}
mkdir ${SUB_DIR}

cat << EOF > ${SSH_DIR}/config
# GitLab, Github
Include conf.d/commons/git.conf
EOF

cat << EOF > ${SSH_DIR}/conf.d/commons/git.conf
# Github
Host github.com
  Hostname github.com
# GitLab
Host gitlab.com
  Hostname gitlab.com
Host git*
  IdentityFile ~/.ssh/keys/commons/git
EOF
