# walle

## 启动
- 启动 websocket : `python ws.py`
- 启动 redis : `redis-server`
- 启动 celery : `celery -A cel worker --loglevel=info`


## 安装
```
sudo easy_install virtualenv


flask/bin/pip install flask
flask/bin/pip install flask-login
flask/bin/pip install flask-openid
flask/bin/pip install flask-mail
flask/bin/pip install flask-sqlalchemy
flask/bin/pip install sqlalchemy-migrate
flask/bin/pip install flask-whooshalchemy
flask/bin/pip install flask-wtf
flask/bin/pip install flask-babel
flask/bin/pip install guess_language
flask/bin/pip install flipflop
flask/bin/pip install coverage
尚未完整，待整理
```
python 2.6升级到2.7
```
wget https://www.python.org/ftp/python/2.7.13/Python-2.7.13.tgz
```
```
./configure
make all
sudo make install
sudo make clean
sudo make distclean
```
把python执行软连接连接到2.7
```
sudo ln -s /usr/local/bin/python /usr/local/bin/python2.6
sudo rm /usr/bin/python
sudo ln -s /usr/local/bin/python2.7 /usr/bin/python
```
编辑yum命令，把路径指明为2.6，因为yum必须基于2.6版本
```
sudo vi /usr/bin/yum
```
把文件头部的#!/usr/bin/python改成#!/usr/bin/python2.6

安装easy_install
```
wget -q http://peak.telecommunity.com/dist/ez_setup.py
sudo python ez_setup.py
```
CentOS安装python包管理安装工具pip的方法如下：
```
wget --no-check-certificate https://github.com/pypa/pip/archive/1.5.5.tar.gz

tar zvxf 1.5.5.tar.gz
cd pip-1.5.5/
sudo python setup.py install
sudo pip install --upgrade pip
```
