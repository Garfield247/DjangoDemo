# Django

## 安装

```shell
pip install django[==version]
```

## 创建项目

```shell
django-admin startproject <object_name>
```

*目录结构*

```josn
<object_name>
├── <object_name>
│   ├── __init__.py
│   ├── settings.py //配置文件
│   ├── urls.py  //URL声明
│   └── wsgi.py //兼容 WSGI 的 Web 服务器的入口点
└── manage.py //命令行脚本
```

### 初始的设置

编辑 `settings.py` 。

1. 把 `TIME_ZONE` 设为你所在的时区。

   ```python
    TIME_ZONE = 'Asia/Shanghai'
   ```

2. 将语言设置为中文

   ```python
   LANGUAGE_CODE = 'zh-Hans'
   ```

3. `INSTALLED_APPS`设置(默认已开启)

   ```python
   django.contrib.admin :管理后台
   django.contrib.auth :身份验证系统
   django.contrib.contenttypes :内容类型框架
   django.contrib.sessions :会话框架
   django.contrib.messages :消息框架
   django.contrib.staticfiles :管理静态文件的框架
   ```

4. 数据库

   **如果要使用数据库要配置数据库链接并进行数据库初始化操作**

   Django默认使用SQLite数据库

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
       }
   }
   ```

   若要使用Mysql数据库应按照如下格式配置

   ```python
   DATABASES = {    
       'default':{
           'ENGINE':'django.db.backends.mysql',
           'NAME':'数据库名',
           'USER':'数据库用户名',
           'PASSWORD':'数据库密码',
           'HOST':'数据库地址',
           'PORT':'数据库端口',
       }
   }
   ```

   执行数据库迁移命令

   ```
   python manage.py migrate
   ```

5. 查看能否正常运行

   ```shell
   python manage.py runserver
   ```

   若正常运行则会输出如下命令：

   ```shell
   Performing system checks...
   
   System check identified no issues (0 silenced).
   March 04, 2019 - 11:34:28
   Django version 1.11.4, using settings 'demo01.settings'
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CONTROL-C
   ```

   