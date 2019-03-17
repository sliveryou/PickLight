# 拾光网公益赠书平台


## 特性

- 蓝图注册视图函数
- WTForms 进行表单与参数校验
- 编写 ViewModel 处理原始数据
- Jinja2 模板引擎
- 基于 SQLAlchemy 的 CRUD 操作
- 使用 with 的上下文特性自动开启事务
- flask_login 处理用户登陆逻辑
- flask_mail 使用多线程基于应用上下文异步发送邮件
- 简单，开箱即用

> Python 的运行环境要求 3.6 以上。


## 要求

| 依赖 | 说明 |
| -------- | -------- |
| Python | `>= 3.6` |
| Flask | `>= 1.0.2` |
| cymysql | `>= 0.9.10` |
| Flask-Login |`>= 0.4.1`|
| Flask-Mail |`>= 0.9.1`|
| Flask-SQLAlchemy  |`>= 2.3.2`|
| itsdangerous |`>= 0.24`|
| Jinja2 |`>= 2.10`|
| requests |`>= 2.18.4`|
| SQLAlchemy  |`>= 1.2.8`|
| urllib3 |`>= 1.22`|
| Werkzeug |`>= 0.14.1`|
| WTForms |`>= 2.2`|


## 注意

1. 数据库的表在运行 manage.py 时会自动生成；
2. 需要修改 app 目录下的 secure.py 文件，填入 MySQL 数据库的访问密码和网站的安全密钥；
3. Flask 扩展需要自行安装


## 安装

1. 先 fork 项目到自己的项目下，或直接下载代码到本地；
2. 补充 app 目录下的 secure.py 文件：

```
# -*- coding: UTF-8 -*-
import os

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://用户名:密码@IP地址(如127.0.0.1):端口号(如3306)/数据库(如book)'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = 'XXXXXXXX' # 随机字符串即可

MAIL_DEBUG = False
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = os.environ.get('MAIL_USERNAME') # 关键信息可记录于 Shell 的环境变量中
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') # 如 zsh 中，在 .zshrc 文件里加入 
                                                # export MAIL_USERNAME='邮箱'
                                                # export MAIL_PASSWORD='校验码' 
MAIL_SUBJECT_PREFIX = '[拾光]'
MAIL_SENDER = '拾光 <picklight@sliveryou.cn>'
```

## 相关依赖

最好在 pipenv 的虚拟环境中安装，避免全局污染

- flask

```
pipenv install flask
```

- requests

```
pip3 install requests
```

- WTforms

```
pip3 install wtforms
```

- SQLALChemy

```
pipenv install flask-sqlalchemy
```

- Jinja2

```
pip3 install Jinja2
```

- flask-login

```
pipenv install flask-login
```

- flask-mail

```
pipenv install flask-mail
```


## 运行

```
python fisher.py
```


## 在项目中使用事务

使用 contextmanager 装饰器，当进行数据库处理时，发生错误会自动回滚：

```
class SQLAlchemy(_SQLAlchemy):
    # 创建 _SQLAlchemy 的子类
    @contextmanager
    def auto_commit(self):
        # 创建上下文环境的 enter 和 exit 方法，实现自动 commit
        try:
            yield
            self.session.commit()
        except Exception as e:
            # 数据库对象事物回滚
            self.session.rollback()
            raise e
```


## 在项目中使用 filter_by

重写 filter_by 方法，默认加入条件 status=1：

```
class Query(BaseQuery):
    # 继承 BaseQuery，重写 filter_by 方法
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        # super 返回当前类的基类：第一个参数表示当前类，第二个参数表示当前实例
        return super(Query, self).filter_by(**kwargs)

# 相当于每次使用 fliter_by 时都加入了 status=1 的条件
# Gift.query.filter_by(id=gid).first_or_404() ==> Gift.query.filter_by(id=gid,status=1).first_or_404()
```


## 在项目中构建 ViewModel

推荐在渲染模板之前，创建 ViewModel 文件，将原始数据进行处理，具体可参考 app/view_models/book.py 文件。


## 在项目中发送邮件

直接调用发送邮件方法，已经默认多线程异步发送邮件：

```
def send_async_email(app, msg):
    # 因为线程隔离的影响，所以需要创建应用上下文
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass


def send_email(to, subject, template, **kwargs):
    msg = Message(current_app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=current_app.config['MAIL_SENDER'],
                  recipients=[to])
    msg.html = render_template(template, **kwargs)
    # 获取真实的 app 对象
    app = current_app._get_current_object()
    # 异步发送电子邮件
    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()
```


## 上线

可以参考：[CentOS 下用 Nginx 和 uwsgi 部署 flask 项目](https://segmentfault.com/a/1190000004294634)

目前项目运行：[http://118.25.50.77:8000/](http://118.25.50.77:8000/)