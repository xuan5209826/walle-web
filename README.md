# walle-web

walle-web.io a deployment kit


Quickstart
----------

```
# 开发分支尝鲜
git clone https://github.com/meolu/walle-web
cd walle-web
git checkout development # 开发分支

# 配置环境
pip install virtualenv
virtualenv venv
pip install -r requirements/dev.txt

# 数据导入
flask db init
flask db migrate
flask db upgrade
# 失败了可以直接导入walle_python.sql

# 数据库连接（自己找下,小小地考验下）
vi settings.py

# 激活环境
source venv/bin/activate

# 运行（内含Flask的一些配置）
sh run.sh

# 怎么可能没有标准的单元测试呢
python -m flask test

# postman api collection 自行导入体验restful api
walle.json.postman_collection

```

.. code-block:: bash

    export WALLE_SECRET='something-really-secret'

Before running shell commands, set the ``FLASK_APP`` and ``FLASK_DEBUG``
environment variables ::

    export FLASK_APP=/path/to/autoapp.py
    export FLASK_DEBUG=1

Then run the following commands to bootstrap your environment ::

    git clone https://github.com/meolu/walle-web
    cd walle
    pip install -r requirements/dev.txt
    bower install
    flask run

You will see a pretty welcome screen.

Once you have installed your DBMS, run the following to create your app's
database tables and perform the initial migration ::

    flask db init
    flask db migrate
    flask db upgrade
    flask run


Deployment
----------

In your production environment, make sure the ``FLASK_DEBUG`` environment
variable is unset or is set to ``0``, so that ``ProdConfig`` is used.


Shell
-----

To open the interactive shell, run ::

    flask shell

By default, you will have access to the flask ``app``.


Running Tests
-------------

To run all tests, run ::

    flask test


Migrations
----------

Whenever a database migration needs to be made. Run the following commands ::

    flask db migrate

This will generate a new migration script. Then run ::

    flask db upgrade

To apply the migration.

For a full migration command reference, run ``flask db --help``.
