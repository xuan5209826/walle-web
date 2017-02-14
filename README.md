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
```