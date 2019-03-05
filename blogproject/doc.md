## 创建项目

1.使用SHELL命令创建`Django`项目工程

```shell
django-admin startproject blogproject
```

2.进行基础配置

编辑`【blogproject/blogproject/settings.py】`将语言改为中文，时区设为中国

```python
# 把英文改为中文
LANGUAGE_CODE = 'zh-hans'
# 把国际时区改为中国时区
TIME_ZONE = 'Asia/Shanghai'
```

3.初次运行

*在项目根目录下执行*

```
python manage.py runserver
```

访问http://127.0.0.1:8000/观察是否能正常运行

## 创建应用

1.使用SHELL命令创建`Django`应用

```
python manage.py startapp blog
```

2.注册应用

编辑`【blogproject/blogproject/settings.py】` 对`blog`应用进行注册

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog'
]
```

## 创建数据库模型

1.设计数据库表结构

- 文章
  - 标题
  - 正文
  - 发布时间
  - 修改时间
  - 摘要
  - 分类（一对多）
  - 标签（多对多）
  - 作者

- 分类
  - 分类名
- 标签
  - 标签名



2.编写模型代码

编辑`【blogproject/blog/models.py】` 

```python
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

class Tag(models.Model):
    name = models.CharField(max_length=100)

class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    excerpt = models.CharField(max_length=200,blank=True)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag,blank=True)
    author = models.ForeignKey(User)
```

