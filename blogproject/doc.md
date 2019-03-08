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

  

## 首页视图

Hello 视图函数

1.绑定URL与视图函数

在`blog` 应用下创建一个`urls.py`文件，写入如下代码

```python
from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r"^$",views.index,name="index"),
]
```

<!--绑定关系的写法是把网址和对应的处理函数作为参数传给 url 函数（ 第一个参数是网
址，第二个参数是处理函数），另外我们还传递了另外一个参数 name，这个参数的值
将作为处理函数 index 的别名，一般设置为视图函数名-->

将应用的url配置到项目url

编辑`【blogproject/blogproject/urls.py】`将blog下的url进行导入

```python
from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r"blog/",include("blog.urls")),
]
```

2.编写视图函数

编辑`【blogproject/blog/views.py】`文件，定义index函数

```python
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("欢迎来到首页！")
```

运行项目，访问http://127.0.0.1:8000/blog/查看结果

3.`Django`模板系统

在项目根目录创建`templates`文件夹，再在该目录（`【blogproject/templates】`）下创建`blog`文件夹

```
mkdir ./templates
mkdir ./templates
```

创建`【blogproject/templates\blog\index.html】` 文件，并写入下面的代码：

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{{ title }}</title>
</head>
<body>
<h1>{{ welcome }}</h1>
</body>
</html>
```

在`【blogproject/blogproject/settings.py】`中配置模板路径

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

修改`【blogproject/blog/views.py】`下的`index`视图函数

```python
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    # return HttpResponse("欢迎来到首页！")
    return render(request,'blog/index.html',context={'title':"我的博客首页",'welcome':"欢迎访问我的博客首页"})
```

运行项目，访问http://127.0.0.1:8000/blog/查看结果



## 真正的首页视图

1.修改`【blogproject/blog/views.py】`下的`index`视图函数

```python
from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
# Create your views here.

def index(request):
    # return HttpResponse("欢迎来到首页！")
    # return render(request,'blog/index.html',context={'title':"我的博客首页",'welcome':"欢迎访问我的博客首页"})
    post_list = Post.objects.all().order_by("-created_time")
    return render(request,'blog/index.html',context={'post_list':post_list})
```

2.处理静态文件

先在 `blog` 应用下建立一个 `static` 文件夹，再在 `static\` 目录下建立一个 `blog` 文件夹。

把下博客模板中的`html`文件拷贝到templates文件夹下

 `css` 和 `js` 文件夹连同里面的全部文件一同拷贝到`static\` 目录下建立一个 `blog` 文件夹

修改`【templates/blog/index.html】`文件引入静态文件

```html
<head>
    <title>Black &amp; White</title>

    <!-- meta -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- css -->
    <!--<link rel="stylesheet" href="css/bootstrap.min.css">-->
    <link rel="stylesheet" href="{% static 'blog/css/bootstrap.min.css' %}">
    <link rel="stylesheet" href="http://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css">
    <!--<link rel="stylesheet" href="css/pace.css">-->
    <link rel="stylesheet" href="{% static 'blog/css/pace.css' %}">
    <!--<link rel="stylesheet" href="css/custom.css">-->
    <link rel="stylesheet" href="{% static 'blog/css/custom.css' %}">

    <!-- js -->
    <!--<script src="js/jquery-2.1.3.min.js"></script>-->
    <script src="{% static 'blog/js/jquery-2.1.3.min.js' %}"></script>
    <!--<script src="js/bootstrap.min.js"></script>-->
    <script src="{% static 'blog/js/bootstrap.min.js' %}"></script>
    <!--<script src="js/pace.min.js"></script>-->
    <script src="{% static 'blog/js/pace.min.js' %}"></script>
    <!--<script src="js/modernizr.custom.js"></script>-->
    <script src="{% static 'blog/js/modernizr.custom.js' %}"></script>
</head>

```
文章列表
```html
<main class="col-md-8">
    {% for post in post_list %}
    <article class="post post-{{ post.pk }}">
        <header class="entry-header">
            <h1 class="entry-title">
                <a href="single.html">{{ post.title }}</a>
            </h1>
            <div class="entry-meta">
                <span class="post-category"><a href="#">{{ post.category.name }}</a></span>
                <span class="post-date"><a href="#"><time class="entry-date"
                                                          datetime="{{ post.created_time }}">{{ post.created_time }}</time></a></span>
                <span class="post-author"><a href="#">{{ post.author }}</a></span>
                <span class="comments-link"><a href="#">4 评论</a></span>
                <span class="views-count"><a href="#">588 阅读</a></span>
            </div>
        </header>
        <div class="entry-content clearfix">
            <p>{{ post.excerpt }}</p>
            <div class="read-more cl-effect-14">
                <a href="#" class="more-link">继续阅读 <span class="meta-nav">→</span></a>
            </div>
        </div>
    </article>
    {% empty %}
    <div class="no-post">暂时还没有发布的文章！ </div>
    {% endfor %}

    <!-- 简单分页效果
<div class="pagination-simple">
<a href="#">上一页</a>
<span class="current">第 6 页 / 共 11 页</span>
<a href="#">下一页</a>
</div>
-->
    <div class="pagination">
        <ul>
            <li><a href="">1</a></li>
            <li><a href="">...</a></li>
            <li><a href="">4</a></li>
            <li><a href="">5</a></li>
            <li class="current"><a href="">6</a></li>
            <li><a href="">7</a></li>
            <li><a href="">8</a></li>
            <li><a href="">...</a></li>
            <li><a href="">11</a></li>
        </ul>
    </div>
</main>
```

## Admin 后台发布文章

1.在 Admin 后台注册模型
	要在后台注册我们自己创建的几个模型（类似于 Flask-admin 的 ModelView） ，这
样 Django Admin 才能知道它们的存在，注册非常简单，只需要在 blog\admin.py
中加入下面的代码：
【blog/admin.py】

```python
from django.contrib import admin
from .models import Post, Category, Tag
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
```

激活虚拟环境，运行开发服务器，访问 http://127.0.0.1:8000/admin/ ，就进入了到
了 Django Admin 后台登录页面，输入刚才创建的管理员账户密码就可以登录到后台
了

