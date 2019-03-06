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

> User 是从 `django.contrib.auth.models` 导入的。
>
> `django.contrib.auth` 是 `Django` 内置的应用，专门用于处理网站用户的注册、登录等流
>
> 程， User 是 `Django` 为我们已经写好的用户模型

## 迁移数据库

在项目根目录下分别执行下面两条命令

```shell
python manage.py makemigrations
python manage.py migrate
```

> 执行第一句之后，`Django`会在`【blogproject/blog/migrations】`目录下生成`0001_initial.py`文件
>
> 执行第二句之后才将操作真正的应用于数据库
>
> 想了解`Django`究竟做了什么可以使用如下命令
>
> ```shell
> python manage.py sqlmigrate blog 0001
> ```

## 用Django的方式操作数据库

- 存数据

  在项目根目录执行如下命令打开一个Django的交互式命令行

  ```python
  python manage.py shell
  ```

  创建一个分类和标签

  ```python
  In [1]: from blog.models import Category,Tag,Post
      
  In [2]: c = Category(name="category_test")
      
  In [3]: c.save()
      
  In [4]: t = Tag(name="tag test")
      
  In [5]: t.save()                                                                   
  ```

  创建文章之前需要先创建一个User

  运行如下命令根据提示创建用户

  ```
  python manage.py cratesuperuser
  ```

  最后出现`Superuser created successfully.` 说明用户创建成功了。

  再次运行 `python manage.py shell` 进入 Python 命令交互栏，开始创建文章：

  ```python 
  In [1]: from blog.models import Category,Tag,Post
      
  In [2]: from django.utils import timezone
      
  In [3]: from django.contrib.auth.models import User                                   
      
  In [4]: user = User.objects.get(username = "garfield")
  
  In [5]: c = Category.objects.get(name="category_test")
  
  In [6]: p = Post(title="title test",body="body test",created_time=timezone.now(),modified_time=timezone.now(),category=c,author=user)
      
  In [7]: p.save() 
  ```

- 取数据

  数据都已经存入数据库现在将数据取出来

  ```python
  In [1]: from blog.models import Category,Tag,Post                                                                                    
  In [2]: Category.objects.all()                                                                                                          
  Out[2]: <QuerySet [<Category: Category object>]>
  
  In [3]: Tag.objects.all()                                                                                                               
  Out[3]: <QuerySet [<Tag: Tag object>]>
  
  In [4]: Post.objects.all()                                                                                                              
  Out[4]: <QuerySet [<Post: Post object>]>
  
  ```

  <!--objects 是我们的模型管理器（相当于 flask 里的 query） ，它为我们提供一系列
  从数据库中取数据方法，这里我们使用了 all 方法，表示我们要把对应的数据全
  部取出来。-->

  上面取数据虽然都返回了数据但无发直观看出究竟是不是我们存入的，为了数据的显示更人性化我们将喂模型添加一个`__str__`方法

  ```python
  from django.contrib.auth.models import User
  from django.db import models
  
  # Create your models here.
  class Category(models.Model):
      name = models.CharField(max_length=100)
  
      def __str__(self):
          return self.name
  
  class Tag(models.Model):
      name = models.CharField(max_length=100)
  
      def __str__(self):
          return self.name
  
  class Post(models.Model):
      title = models.CharField(max_length=100)
      body = models.TextField()
      created_time = models.DateTimeField()
      modified_time = models.DateTimeField()
      excerpt = models.CharField(max_length=200,blank=True)
      category = models.ForeignKey(Category)
      tags = models.ManyToManyField(Tag,blank=True)
      author = models.ForeignKey(User)
  
      def __str__(self):
          return self.title
  ```

  重新进入`Django SHELL`进行查询

  ```python
  In [1]: from blog.models import Category,Tag,Post                                                                                       
  In [2]: Category.objects.all()                                                                                                          
  Out[2]: <QuerySet [<Category: category_test>]>
  
  In [3]: Tag.objects.all()                                                                                                               
  Out[3]: <QuerySet [<Tag: tag test>]>
  
  In [4]: Post.objects.all()                                                                                                              
  Out[4]: <QuerySet [<Post: title test>]>
  ```

- 改数据

  **该数据和增加数据一样都是save()**

  ```python
  In [5]: c = Category.objects.get(name="category_test")                                                                                  
  In [6]: c.name  = "category test new"                                                                                                   
  In [7]: c.save()                                                                                                                        
  In [8]: Category.objects.all()                                                                                                          
  Out[8]: <QuerySet [<Category: category test new>]>
  
  ```

- 删数据

  ```python
  In [9]: t = Tag.objects.get(name="tag test")                                                                                            
  In [10]: t.delete()                                                                                                                     
  Out[10]: (1, {'blog.Post_tags': 0, 'blog.Tag': 1})
  
  In [11]: Tag.objects.all()                                                                                                              
  Out[11]: <QuerySet []>
  
  ```

  