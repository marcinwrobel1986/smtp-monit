#!/bin/bash -xe

PYTHON_VERSION="3.8"
PYTHON_RELEASE="3.8.3"
sudo apt update && sudo apt upgrade -y
sudo apt install build-essential libncursesw5-dev libreadline-gplv2-dev libssl-dev libgdbm-dev libc6-dev libsqlite3-dev libbz2-dev libffi-dev wget curl gcc make zlib1g-dev -y
cd /opt || exit
sudo wget https://www.python.org/ftp/python/${PYTHON_RELEASE}/Python-${PYTHON_RELEASE}.tgz
sudo tar xzf Python-${PYTHON_RELEASE}.tgz
cd Python-${PYTHON_RELEASE} || exit
sudo ./configure --enable-optimizations
sudo make altinstall
sudo rm ../Python-${PYTHON_RELEASE}.tgz
cd ~/ || exit
curl -O https://bootstrap.pypa.io/get-pip.py
python${PYTHON_VERSION} get-pip.py
sudo /usr/local/bin/python${PYTHON_VERSION} -m pip install --upgrade pip
sudo pip install pipenv