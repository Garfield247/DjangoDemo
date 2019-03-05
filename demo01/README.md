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

```json
demo01<object_name>
├── demo01<object_name>
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

   并在`__init__.py` 内添加初始化代码

   ```python
   import pymysql
   pymysql.install_as_MySQLdb()
   ```

   **数据库迁移**

   生成迁移

   ```shell
   python manage.py makemigrations
   ```

   执行迁移

   ```shell
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

   访问`http://127.0.0.1:8000/` 会看到

   ```html
   正常工作了！
   祝贺你的第一个由Django驱动的页面。
   接下来运行你的第一个程序 python manage.py startapp [app_label].
   
   您看到此消息是由于Django的配置文件设置了 DEBUG = True，您还没有配置任何路由URL。开始工作吧。
   ```

   

## 创建一个应用

```shell
python manage.py startapp <AppName>
```

使用应用前需要将应用配置到项目中，在`settings.py`中将应用加入到`INSTALLED_APPS`选项中

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapps'
]
```

项目目录

```json
demo01<object_name>
├── demo01<object_name>
│   ├── __init__.py
│   ├── settings.py //配置文件
│   ├── urls.py  //URL声明
│   └── wsgi.py //兼容 WSGI 的 Web 服务器的入口点
└── manage.py //命令行脚本
└── myapps<app_name>
    ├── admin.py //管理站点模型的声明文件，默认为空
    ├── apps.py //应用信息定义文件，在其中生成了AppConfig，该类用于定义应用名等数据
    ├── __init__.py
    ├── migrations //自动生成，生成迁移文件的
    │   └── __init__.py
    ├── models.py //添加模型层数据类文件
    ├── tests.py //测试代码文件
    └── views.py //定义URL相应函数（路由规则）

```

### 基本视图

1. 构造路由函数

   在`myapps/views.py` 中建立一个路由响应函数

   ```python
   from django.http import HttpResponse
   
   # Create your views here.
   
   def welcome(request):
       return HttpResponse("Hello Django!")
   ```

2. 在URL中进行注册

   - 方式一(不推荐)

     在`demo01/urls.py`

     ```python
     from django.conf.urls import url
     from django.contrib import admin
     from myapps import views
     
     
     urlpatterns = [
         url(r'^admin/', admin.site.urls),
         url(r'^welcome/',views.welcome),
     ]
     ```

   - 方式二(推荐)

     1. 在myapps包下新建urls.py文件(`myapps/urls.py`),参照`demo01/urls.py` 编写如下内容

     ```python
     from django.conf.urls import url
     from myapps import views
     
     urlpatterns = [
         url(r'^$',views.welcome),
     ]
     ```

     2. 在`demo01/urls.py` 中导入`myapps/urls.py`的url配置

     ```python
     from django.conf.urls import url
     from django.contrib import admin
     from django.conf.urls import include
     
     urlpatterns = [
         url(r'^admin/', admin.site.urls),
         url(r'^welcome/',include('myapps.urls')),
     
     ]
     ```

     > 现在如果编写正确，访问http://127.0.0.1:8000/welcome/可以看到"Hello Django!"的字样。

   

### 基本模板

1. 在项目跟目录创建`templates`文件夹

2. 打开`demo01/settings.py`对模板进行配置

   ```python
   TEMPLATES = [
       {
           'BACKEND': 'django.template.backends.django.DjangoTemplates',
           'DIRS': [os.path.join(BASE_DIR, 'templates')],
           'APP_DIRS': True,
           'OPTIONS': {
               'context_processors': [
                   'django.template.context_processors.debug',
                   'django.template.context_processors.request',
                   'django.contrib.auth.context_processors.auth',
                   'django.contrib.messages.context_processors.messages',
               ],
           },
       },
   ]
   ```

   **配置说明：**

   - BACKEND 的值是一个点分 Python 路径，指向实现 Django 模板后端 API 的模板引擎类。内置的后端有 django.template.backends.django.DjangoTemplates 和 django.template.backends.jinja2.Jinja2
   - DIRS 定义一个目录列表，模板引擎按顺序在里面查找模板源文件
   - APP_DIRS 设定是否在安装的应用中查找模板。按约定，APPS_DIRS 设为 True 时，DjangoTemplates 会在INSTALLED_APPS 中的各个应用里查找名为“templates”的子目录。这样，即使 DIRS 为空，模板引擎还能查找应用模板。
   - OPTIONS 是一些针对后端的设置。同一个后端可以配置具有不同选项的多个实例，然而这并不常见。此时，要为各个引擎定义唯一的 NAME。

3. 创建建议的模板文件(`templates/index1.html`)

   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <title>{{ title }}</title>
   </head>
   <body>
   {{ welcome }}
   </body>
   </html>
   ```

4. 在`myapps/views.py`创建使用模板的视图函数

   ```python
   from django.shortcuts import render
   from django.http import HttpResponse
   
   # Create your views here.
   
   def welcome(request):
       return HttpResponse("HELLO Django!")
   
   def template_test(request):
       context = {'title': '模板测试',
                  'welcome': '欢迎来到模板测试页面'}
       return render(request, 'index1.html', context)
   ```

5. 在`myapps/urls.py`进行注册

   ```python
   ...
   url(r'^template_test/$',views.template_test),
   ...
   ```

> 访问http://127.0.0.1:8000/welcome/template_test/可以查看结果



### 定义模型

1. 在myapps/models.py中创建自己的Models继承自models.Model

   ```python
   from django.db import models
   
   # Create your models here.
   class Grade(models.Model):
       gname = models.CharField(max_length=20)
       gdate = models.DateField()
       ggirlnum = models.IntegerField()
       gboynum = models.IntegerField()
       isDelete = models.BooleanField()
   
       def __str__(self):
           return self.gname
   
   
   class Student(models.Model):
       # 如果存储比较短的字符串使用charfield
       # 存储大文本数据，要使用TextField
       sname = models.CharField(max_length=30)
       # 整数类型IntegerField
       sage = models.IntegerField()
       sinfo = models.CharField(max_length=100)
       isDelete = models.BooleanField()
       # ForeignKey一对多的关联关系
       sgrade = models.ForeignKey('Grade')
   
       def __str__(self):
           return self.sname
   ```

   