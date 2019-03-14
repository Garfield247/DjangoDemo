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

定制 Admin 后台
在 admin post 列表页面，我们只看到了文章的标题，但是我们希望它显示更加详细
的信息，这需要我们来定制 Admin 了，在 admin.py 添加如下代码：
【blog/admin.py】

```python
from django.contrib import admin
from .models import Post, Category, Tag
class PostAdmin(admin.ModelAdmin):
list_display = ['title', 'created_time', 'modified_time', 'category', 'author']

#把新增的 PostAdmin 也注册进来

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
```

## 详情页视图

1.在`【blogproject/blog/urls.py】`中绑定URL

```python
from django.conf.urls import url

from blog import views

app_name = 'blog'
urlpatterns = [
    url(r"^$",views.index,name="index"),
    url(r"^post/(?P<pk>[0-9]+)/$",views.detail,name='detail')
]
```

<!--通过 app_name='blog' 告诉 Django 这个 urls.py 模块是属于 blog 应用的这种技术叫做视图函数命名空间（相当于 flask 的蓝本名+视图函数名） -->

<!--被括起来的部分 (?P<pk>[0-9]+)匹配 文章ID，
那么这个 ID  会在调用视图函数 detail 时被传递进去给到参数 pk，实际上视图函数
的调用就是这个样子： detail(request, pk=ID)。-->

2.为了方便地生成上述的 URL，我们在 Post 类里定义一个 get_absolute_url 方法（直接在
模型中自己就生成了自己的 URL！！！） 

```python
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

    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})
```

3.编写detail视图函数

```python
def detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    return render(request,'blog/detail.html',context=post)
```

4.改写模板

- 将公共部分提取出来形成`base.html`

  ```html
  {% load staticfiles %}
  <!DOCTYPE html>
  <html>
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
  
  <body>
  <div class="container">
      <header id="site-header">
          <div class="row">
              <div class="col-md-4 col-sm-5 col-xs-8">
                  <div class="logo">
                      <h1><a href="index.html"><b>Black</b> &amp; White</a></h1>
                  </div>
              </div><!-- col-md-4 -->
              <div class="col-md-8 col-sm-7 col-xs-4">
                  <nav class="main-nav" role="navigation">
                      <div class="navbar-header">
                          <button type="button" id="trigger-overlay" class="navbar-toggle">
                              <span class="ion-navicon"></span>
                          </button>
                      </div>
  
                      <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                          <ul class="nav navbar-nav navbar-right">
                              <li class="cl-effect-11"><a href="index.html" data-hover="首页">首页</a></li>
                              <li class="cl-effect-11"><a href="full-width.html" data-hover="博客">博客</a></li>
                              <li class="cl-effect-11"><a href="about.html" data-hover="关于">关于</a></li>
                              <li class="cl-effect-11"><a href="contact.html" data-hover="联系">联系</a></li>
                          </ul>
                      </div><!-- /.navbar-collapse -->
                  </nav>
                  <div id="header-search-box">
                      <a id="search-menu" href="#"><span id="search-icon" class="ion-ios-search-strong"></span></a>
                      <div id="search-form" class="search-form">
                          <form role="search" method="get" id="searchform" action="#">
                              <input type="search" placeholder="搜索" required>
                              <button type="submit"><span class="ion-ios-search-strong"></span></button>
                          </form>
                      </div>
                  </div>
              </div><!-- col-md-8 -->
          </div>
      </header>
  </div>
  <div class="copyrights">Collect from <a href="http://www.cssmoban.com/">网页模板</a></div>
  <div class="copyrights">Modified by <a href="http://zmrenwu.com/">追梦人物的博客</a></div>
  
  <div class="content-body">
      <div class="container">
          <div class="row">
              <main class="col-md-8">
                  {% block main %}
                  {% endblock main %}
              </main>
              <aside class="col-md-4">
                  {% block toc %}
                  {% endblock toc %}
                  <div class="widget widget-recent-posts">
                      <h3 class="widget-title">最新文章</h3>
                      <ul>
                          <li>
                              <a href="#">Django 博客开发入门教程：前言</a>
                          </li>
                          <li>
                              <a href="#">Django 博客使用 Markdown 自动生成文章目录</a>
                          </li>
                          <li>
                              <a href="#">部署 Django 博客</a>
                          </li>
                      </ul>
                  </div>
                  <div class="widget widget-archives">
                      <h3 class="widget-title">归档</h3>
                      <ul>
                          <li>
                              <a href="#">2017 年 5 月</a>
                          </li>
                          <li>
                              <a href="#">2017 年 4 月</a>
                          </li>
                          <li>
                              <a href="#">2017 年 3 月</a>
                          </li>
                      </ul>
                  </div>
  
                  <div class="widget widget-category">
                      <h3 class="widget-title">分类</h3>
                      <ul>
                          <li>
                              <a href="#">Django 博客教程 <span class="post-count">(13)</span></a>
                          </li>
                          <li>
                              <a href="#">Python 教程 <span class="post-count">(11)</span></a>
                          </li>
                          <li>
                              <a href="#">Django 用户认证 <span class="post-count">(8)</span></a>
                          </li>
                      </ul>
                  </div>
  
                  <div class="widget widget-tag-cloud">
                      <h3 class="widget-title">标签云</h3>
                      <ul>
                          <li>
                              <a href="#">Django</a>
                          </li>
                          <li>
                              <a href="#">Python</a>
                          </li>
                          <li>
                              <a href="#">Java</a>
                          </li>
                          <li>
                              <a href="#">笔记</a>
                          </li>
                          <li>
                              <a href="#">文档</a>
                          </li>
                          <li>
                              <a href="#">AngularJS</a>
                          </li>
                          <li>
                              <a href="#">CSS</a>
                          </li>
                          <li>
                              <a href="#">JavaScript</a>
                          </li>
                          <li>
                              <a href="#">Snippet</a>
                          </li>
                          <li>
                              <a href="#">jQuery</a>
                          </li>
                      </ul>
                  </div>
                  <div class="rss">
                      <a href=""><span class="ion-social-rss-outline"></span> RSS 订阅</a>
                  </div>
              </aside>
          </div>
      </div>
  </div>
  <footer id="site-footer">
      <div class="container">
          <div class="row">
              <div class="col-md-12">
                  <p class="copyright">&copy 2017 - 采集自<a href="http://www.cssmoban.com/"
                                                          target="_blank" title="模板之家">模板之家</a>
                  </p>
              </div>
          </div>
      </div>
  </footer>
  
  <!-- Mobile Menu -->
  <div class="overlay overlay-hugeinc">
      <button type="button" class="overlay-close"><span class="ion-ios-close-empty"></span></button>
      <nav>
          <ul>
              <li><a href="index.html">首页</a></li>
              <li><a href="full-width.html">博客</a></li>
              <li><a href="about.html">关于</a></li>
              <li><a href="contact.html">联系</a></li>
          </ul>
      </nav>
  </div>
  
  <script src="js/script.js"></script>
  
  </body>
  </html>
  
  ```

  

- `index.html`

  ```html
  {% extends 'base.html' %}
  {% block main %}
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
              <a href="{{ post.get_absolute_url }}" class="more-link">继续阅读 <span class="meta-nav">→</span></a>
          </div>
      </div>
  </article>
  {% empty %}
  <div class="no-post">暂时还没有发布的文章！</div>
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
  {% endblock main %}
  
  ```

- `detail.html`

  ```python
  {% extends 'base.html' %}
  {% block main %}
  <article class="post post-{{ post.pk }}">
      <header class="entry-header">
          <h1 class="entry-title">{{ post.title }}</h1>
          <div class="entry-meta">
  <span class="post-category"><a
          href="#">{{ post.category.name }}</a></span>
              <span class="post-date"><a href="#"><time
                      class="entry-date"
                      datetime="{{ post.created_time }}">{{ post.created_time }}</time></a
              ></span>
              <span class="post-author"><a
                      href="#">{{ post.author }}</a></span>
              <span class="comments-link"><a href="#">4 评论
  </a></span>
              <span class="views-count"><a href="#">588 阅读
  </a></span>
          </div>
      </header>
      <div class="entry-content clearfix">
          {{ post.body }}
      </div>
  </article>
  <section class="comment-area" id="comment-area">
      <hr>
      <h3>发表评论</h3>
      <form action="#" method="post" class="comment-form">
          <div class="row">
              <div class="col-md-4">
                  <label for="id_name">名字： </label>
                  <input type="text" id="id_name" name="name"
                         required>
              </div>
              <div class="col-md-4">
                  <label for="id_email">邮箱： </label>
                  <input type="email" id="id_email" name="email"
                         required>
              </div>
              <div class="col-md-4">
                  <label for="id_url">网址： </label>
                  <input type="text" id="id_url" name="url">
              </div>
              <div class="col-md-12">
                  <label for="id_comment">评论： </label>
                  <textarea name="comment" id="id_comment"
                            required></textarea>
                  <button type="submit" class="comment-btn">发表
                  </button>
              </div>
          </div> <!-- row -->
      </form>
      <div class="comment-list-panel">
          <h3>评论列表，共 <span>4</span> 条评论</h3>
          <ul class="comment-list list-unstyled">
              <li class="comment-item">
                  <span class="nickname">追梦人物</span>
                  <time class="submit-date" datetime="2012-11-
  09T23:15:57+00:00">2017 年 3 月 12 日 14:56
                  </time>
                  <div class="text">
                      文章观点又有道理又符合人性，这才是真正为了表达观
                      点而写，不是为了迎合某某知名人士粉丝而写。我觉得如果琼瑶是前妻，生了三孩子
                      后被一不知名的女人挖了墙角，我不信谁会说那个女人是追求真爱，说同情琼瑶骂小
                      三的女人都是弱者。
                  </div>
              </li>
              <li class="comment-item">
                  <span class="nickname">zmrenwu</span>
                  <time class="submit-date" datetime="2012-11-
  09T23:15:57+00:00">2017 年 3 月 11 日 23:56
                  </time>
                  <div class="text">
                      本能有可能会冲破格局，但格局有时候也会拘住本能。
                  </div>
              </li>
              <li class="comment-item">
                  <span class="nickname">蝙蝠侠</span>
                  <time class="submit-date" datetime="2012-11-
  09T23:15:57+00:00">2017 年 3 月 9 日 8:56
                  </time>
                  <div class="text">
                      其实真理一般是属于沉默的大多数的。那些偏激的观点
                      只能吸引那些同样偏激的人。前几年琼瑶告于妈抄袭，大家都表示大快人心，说明吃
                      瓜观众都只是就事论事，并不是对琼瑶有偏见。
                  </div>
              </li>
              <li class="comment-item">
                  <span class="nickname">长江七号</span>
                  <time class="submit-date" datetime="2012-11-
  09T23:15:57+00:00">2017 年 2 月 12 日 12:56
                  </time>
                  <div class="text">
                      观点我很喜欢！就是哎嘛本来一清二楚的，来个小三小
                      四乱七八糟一团乱麻夹缠不清，简直麻烦要死
                  </div>
              </li>
          </ul>
      </div>
  </section>
  {% endblock main %}
  {% block toc %}
  <div class="widget widget-content">
      <h3 class="widget-title">文章目录</h3>
      <ul>
          <li>
              <a href="#">教程特点</a>
          </li>
          <li>
              <a href="#">谁适合这个教程</a>
          </li>
          <li>
              <a href="#">在线预览</a>
          </li>
          <li>
              <a href="#">资源列表</a>
          </li>
          <li>
              <a href="#">获取帮助</a>
          </li>
      </ul>
  </div>
  {% endblock toc %}
  ```

  **Done！**

  ## 添加markdown支持

  1.安装Markdown

  ```shell
  pip install markdown
  ```

  2.在detail中渲染markdown

  ```python
  def detail(request,pk):
      post = get_object_or_404(Post,pk=pk)
      post.body = markdown(post.body,
                           extensions = [
                               'markdown.extensions.extra',
                               'markdown.extensions.codehilite',
                               'markdown.extensions.toc',
                           ]
                           )
      return render(request,'blog/detail.html',context={'post':post})
  ```

  3.在模板中使用safe防止markdown转义

  ```html
  {{ post.body }}   >>>    {{ post.body|safe }}
  ```

  <!--safe 是 Django 模板系统中的过滤器（ Filter），可以简单地把它看成是一种函数，其作用是作用于模板变量，将模板变量的值变为经过滤器处理过后的值。例如这里{{ post.body|safe }}，本来 {{ post.body }} 经模板系统渲染后应该显示 body 本身的值，但是在后面加上 safe 过滤器后，渲染的值不再是 body 本身的值，而是由 safe函数处理后返回的值。过滤器的用法是在模板变量后加一个 | 管道符号，再加上过滤器的名称。可以连续使用多个过滤器，例如 {{var|filter1|filter2 }}。-->

  4.代码高亮

  - 安装Pygments

    ```shell
    pip install Pygments
    ```

  - 在`base.html`<!--引入样式文件-->

    ```
    <link rel="stylesheet" href="{% static 'blog/css/highlights/github.css' %}">
    ```

  **Done!**

  ## 使用自定义标签模板

  1.编写模板标签代码

  在我们的 `blog` 应用下创建一个 `templatetags` 文件夹。然后在这个文件夹下创建
  一个 `__init__.py` 文件，使这个文件夹成为一个 Python 包，之后在 `templatetags\` 目
  录下创建一个 `blog_tags.py` 文件

  ```python
  from django import template
  from ..models import Post,Category
  
  register = template.Library()
  
  # 最新文章模板标签
  @register.simple_tag
  def get_recent_posts(num=5):
      return Post.objects.all().order_by('-created_time')[:num]
  
  # 归档模板标签
  @register.simple_tag
  def archives():
      return Post.objects.dates('created_time','month',order='DESC')
  
  # 分类模板标签
  @register.simple_tag
  def get_categories():
      return Category.objects.all()
  
  ```

  <!--首先导入 template 这个模块，然后实例化了一个 template.Library 类，并将
  函数 get_recent_posts 装饰为 register.simple_tag。这样就可以在模板中使用语法 {%
  get_recent_posts %} 调用这个函数了（ 自定义模板标签的步骤） 。-->

  <!--dates 方法会返回一个列表，列表中的元素为每一篇文章（ Post）的创建时间，
  且是 Python 的 date 对象，精确到月份，降序排列。 接受的三个参数值表明了这些含
  义，一个是 created_time ，即 Post 的创建时间， month 是精度， order='DESC' 表明降序
  排列（即离当前越近的时间越排在前面）。-->

  2.使用自定义的模板标签

  打开 `base.html`，为了使用模板标签，我们首先需要在模板中导入存放这些模板标签的模块，这里是`blog_tags.py` 模块。当时我们为了使用 static 模板标签时曾经导入过 `{% load staticfiles %}`，这次在 `{% load staticfiles %}` 下再导入 `blog_tags`

  ```python
  {% load staticfiles %}
  {% load blog_tags %}
  <!DOCTYPE html>
  <html>
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
  
      <link rel="stylesheet" href="{% static 'blog/css/highlights/github.css' %}">
  
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
  
  <body>
  <div class="container">
      <header id="site-header">
          <div class="row">
              <div class="col-md-4 col-sm-5 col-xs-8">
                  <div class="logo">
                      <h1><a href="index.html"><b>Black</b> &amp; White</a></h1>
                  </div>
              </div><!-- col-md-4 -->
              <div class="col-md-8 col-sm-7 col-xs-4">
                  <nav class="main-nav" role="navigation">
                      <div class="navbar-header">
                          <button type="button" id="trigger-overlay" class="navbar-toggle">
                              <span class="ion-navicon"></span>
                          </button>
                      </div>
  
                      <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                          <ul class="nav navbar-nav navbar-right">
                              <li class="cl-effect-11"><a href="index.html" data-hover="首页">首页</a></li>
                              <li class="cl-effect-11"><a href="full-width.html" data-hover="博客">博客</a></li>
                              <li class="cl-effect-11"><a href="about.html" data-hover="关于">关于</a></li>
                              <li class="cl-effect-11"><a href="contact.html" data-hover="联系">联系</a></li>
                          </ul>
                      </div><!-- /.navbar-collapse -->
                  </nav>
                  <div id="header-search-box">
                      <a id="search-menu" href="#"><span id="search-icon" class="ion-ios-search-strong"></span></a>
                      <div id="search-form" class="search-form">
                          <form role="search" method="get" id="searchform" action="#">
                              <input type="search" placeholder="搜索" required>
                              <button type="submit"><span class="ion-ios-search-strong"></span></button>
                          </form>
                      </div>
                  </div>
              </div><!-- col-md-8 -->
          </div>
      </header>
  </div>
  <div class="copyrights">Collect from <a href="http://www.cssmoban.com/">网页模板</a></div>
  <div class="copyrights">Modified by <a href="http://zmrenwu.com/">追梦人物的博客</a></div>
  
  <div class="content-body">
      <div class="container">
          <div class="row">
              <main class="col-md-8">
                  {% block main %}
                  {% endblock main %}
              </main>
              <aside class="col-md-4">
                  {% block toc %}
                  {% endblock toc %}
                  <div class="widget widget-recent-posts">
                      <h3 class="widget-title">最新文章</h3>
                      {% get_recent_posts as recent_post_list %}
                      <ul>
                          {% for post in recent_post_list %}
                          <li>
                              <a href="{{ post.get_absolute_url }}">{{ post.title }}</a>
                          </li>
                          {% empty %}
                          暂无文章
                          {% endfor %}
                      </ul>
                  </div>
                  <div class="widget widget-archives">
                      <h3 class="widget-title">归档</h3>
                      {% archives as date_list %}
                      <ul>
                          {% for date in date_list %}
                          <li>
                              <a href="#">{{ date.year }} 年 {{ date.month }} 月</a>
                          </li>
                          {% empty %}
                          暂无归档！
                          {% endfor %}
                      </ul>
                  </div>
  
                  <div class="widget widget-category">
                      <h3 class="widget-title">分类</h3>
                      {% get_categories as category_list %}
                      <ul>
                          {% for category in category_list %}
                          <li>
                              <a href="#">{{ category.name }} <span class="post-count">(13)</span></a>
                          </li>
                          {% empty %}
                          暂无分类！
                          {% endfor %}
                      </ul>
                  </div>
  
                  <div class="widget widget-tag-cloud">
                      <h3 class="widget-title">标签云</h3>
                      <ul>
                          <li>
                              <a href="#">Django</a>
                          </li>
                          <li>
                              <a href="#">Python</a>
                          </li>
                          <li>
                              <a href="#">Java</a>
                          </li>
                          <li>
                              <a href="#">笔记</a>
                          </li>
                          <li>
                              <a href="#">文档</a>
                          </li>
                          <li>
                              <a href="#">AngularJS</a>
                          </li>
                          <li>
                              <a href="#">CSS</a>
                          </li>
                          <li>
                              <a href="#">JavaScript</a>
                          </li>
                          <li>
                              <a href="#">Snippet</a>
                          </li>
                          <li>
                              <a href="#">jQuery</a>
                          </li>
                      </ul>
                  </div>
                  <div class="rss">
                      <a href=""><span class="ion-social-rss-outline"></span> RSS 订阅</a>
                  </div>
              </aside>
          </div>
      </div>
  </div>
  <footer id="site-footer">
      <div class="container">
          <div class="row">
              <div class="col-md-12">
                  <p class="copyright">&copy 2017 - 采集自<a href="http://www.cssmoban.com/"
                                                          target="_blank" title="模板之家">模板之家</a>
                  </p>
              </div>
          </div>
      </div>
  </footer>
  
  <!-- Mobile Menu -->
  <div class="overlay overlay-hugeinc">
      <button type="button" class="overlay-close"><span class="ion-ios-close-empty"></span></button>
      <nav>
          <ul>
              <li><a href="index.html">首页</a></li>
              <li><a href="full-width.html">博客</a></li>
              <li><a href="about.html">关于</a></li>
              <li><a href="contact.html">联系</a></li>
          </ul>
      </nav>
  </div>
  
  <script src="js/script.js"></script>
  
  </body>
  </html>
  
  ```

  在`settings.py`中对`blog_tags`进行注册（1.10及以后版本可不注册）

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
          'libraries': {
              'blog_tags': 'blog.templatetags.blog_tags',
  
          }
          },
      },
  ]
  ```

  **Done！**

## 分类与归档

**1.归档**

归档视图函数

```python
def archives(request, year, month):
	post_list = Post.objects.filter(created_time__year=year,created_time__month=month).order_by('-created_time')
	return render(request, 'blog/index.html', context={'post_list': post_list})
```

<!--Python 中类实例调用属性的方法通常是 created_time.year，但是由于这里作为函数的参数列表，所以 Django 要求我们把点替换成了两个下划线，即 created_time__year。-->

绑定URL

```python
from django.conf.urls import url

from . import views

app_name = 'blog'
urlpatterns = [
    url(r"^$",views.index,name="index"),
    url(r"^post/(?P<pk>[0-9]+)/$",views.detail,name="detail"),
    url(r"^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$",views.archives,name="archives"),
]
```

修改模板`base.html`

```html
<div class="widget widget-archives">
    <h3 class="widget-title">归档</h3>
    {% archives as date_list %}
    <ul>
        {% for date in date_list %}
        <li>
            <a href="{% url 'blog:archives' date.year date.month %}">{{ date.year }} 年 {{ date.month }} 月</a>
        </li>
        {% empty %}
        暂无归档！
        {% endfor %}
    </ul>
</div>
```

<!--{% url %} 这个模板标签的作用是解析视图函数 blog:archives 对应的 URL 模式，并把 URL 模式中的年和月替换成 date.year， date.month 的值。（ 相当于 Flask 里模板中的{{url_for()}}标签） -->

**2.分类**

分类视图函数

```python
def category(request,pk):
    cate = get_object_or_404(Category,pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})
```

绑定URL

```python
from django.conf.urls import url

from . import views

app_name = 'blog'
urlpatterns = [
    url(r"^$",views.index,name="index"),
    url(r"^post/(?P<pk>[0-9]+)/$",views.detail,name="detail"),
    url(r"^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$",views.archives,name="archives"),
    url(r"^category/(?P<pk>[0-9]+)/$",views.category,name="category"),
]
```

修改模板`base.html`

```html
<div class="widget widget-category">
    <h3 class="widget-title">分类</h3>
    {% get_categories as category_list %}
    <ul>
        {% for category in category_list %}
        <li>
            <a href="{% url 'blog:category' category.pk %}">{{ category.name }} <span class="post-count">(13)</span></a>
        </li>
        {% empty %}
        暂无分类！
        {% endfor %}
    </ul>
</div>
```

**Done!**

## 评论

创建一个新的应用

```python
python manage.py startapp comments
```

在`settings.py`中注册`comments` 应用

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'comments',
]
```

创建数据库模型

```python
from django.db import models

# Create your models here.
class Comment(models.Model):

    name = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    url = models.URLField(blank=True)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey('blog.Post')

    def __str__(self):
        return self.text[:20]
```

评论表单

在`comments`应用下创建`forms.py`

```python
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','email','url','text']
```

<!--要使用 Django 的表单功能，我们首先导入 forms 模块。 Django 的表单类必须继承自 forms.Form 类或者 forms.ModelForm 类。 如果表单对应有一个数据库模型（例如这里的评论表单对应着评论模型），那么使用 ModelForm 类会简单很多，这是 Django为我们提供的方便。之后我们在表单的内部类 Meta 里指定一些和表单相关的东西。model = Comment 表明这个表单对应的数据库模型是 Comment 类。 fields = ['name','email', 'url', 'text'] 指定了表单需要显示的字段，这里我们指定了 name、 email、 url、text 需要显示。-->

评论视图函数

```python
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CommentForm

# Create your views here.
from blogproject.blog.models import Post


def post_comment(request,post_pk):
    post = get_object_or_404(Post,pk=post_pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect(post)
        else:
            comment_list = post.comment_set_all()
            context = {
                'post':post,
                'form':form,
                'comment_list':comment_list
         }
        return redirect(request,'blog/detail.html',context=context )
```



绑定`url`

`【blogproject/comments/urls.py】`

```python
from django.conf.urls import url
from . import views

app_name = 'comments'
urlpatterns = [
    url(r'^comments/post/(?P<pk>[0-9]+)/$',views.post_comment,name='post_comment')
]
```

`【blogproject/blogproject/urls.py】`

```python
from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r"^blog/",include("blog.urls")),
    url(r'^comments/',include('comments.urls'))
]

```

修改详情页视图函数

```python
def detail(request,pk):
    '''
    文章详情页视图函数
    :param request:
    :param pk:
    :return:
    '''
    post = get_object_or_404(Post,pk=pk)
    post.body = markdown(post.body,
                         extensions = [
                             'markdown.extensions.extra',
                             'markdown.extensions.codehilite',
                             'markdown.extensions.toc',
                         ]
                         )
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {'post':post,
               'form':form,
               'comment_list':comment_list,
               }
    return render(request,'blog/detail.html',context=context)		
```

修改模板

- 渲染表单

  ```html
      <h3>发表评论</h3>
      <form action="{% url 'comments:post_comment' post.pk %}" method="post" class="comment-form">
          {% csrf_token %}
          <div class="row">
              <div class="col-md-4">
                  <label for="{{ form.name.id_for_label }}">名字： </label>
                  {{ form.name }}
                  {{ form.name.errors }}
              </div>
              <div class="col-md-4">
                  <label for="{{ form.email.id_for_label }}">邮箱： </label>
                  {{ form.email }}
                  {{ form.email.errors }}
              </div>
              <div class="col-md-4">
                  <label for="{{ form.url.id_for_label }}">Url： </label>
                  {{ form.url }}
                  {{ form.url.errors }}
              </div>
              <div class="col-md-12">
                  <label for="{{ form.text.id_for_label }}">评论： </label>
                  {{ form.text }}
                  {{ form.text.errors }}
              </div>
              <button type="submit" class="comment-btn">发表</button>
          </div> <!-- row -->
      </form>
  ```

- 展示评论

  ```python
    <div class="comment-list-panel">
          <h3>评论列表，共 <span>{{ comment_list|length }}</span> 条评论</h3>
          <ul class="comment-list list-unstyled">
              {% for comment in comment_list  %}
              <li class="comment-item">
                  <span class="nickname">{{ comment.name }}</span>
                  <time class="submit-date" datetime="{{ comment.created_time }}">{{ comment.created_time }}</time>
                  <div class="text">
                      {{ comment.text }}
                  </div>
              </li>
              {% empty %}
              暂无评论
              {% endfor %}
          </ul>
      </div>
  ```

  **Done !**（运行前执行数据库迁移）

## 改进

- 文章列表默认逆序

  1.Post 类的内部定义一个 Meta 类，并指定排序属性

  ```python
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
  
      def get_absolute_url(self):
          return reverse('blog:detail',kwargs={'pk':self.pk})
      
      class Meta:
          ordering = ['-created_time']
  ```

  2.删掉视图函数中对文章列表中返回结果进行排序的代码

- 完善链接跳转

  `base.html`

  ```html
  <h1><a href="{% url 'blog:index' %}"><b>Black</b> &amp; White</a></h1>
  <!--首页logo链接-->
  ```

  `index.html`

  ```html
   <span class="comments-link"><a href="{{ post.get_absolute_url }}#comment-area">{{ post.comment_set.count }} 评论</a></span>
  <!--文章列表页评论数量和评论跳转-->
  ```

  

## 文章阅读量

1.修改模型`【blog/models.py】` 并增加模型方法。

```python
class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    excerpt = models.CharField(max_length=200,blank=True)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag,blank=True)
    author = models.ForeignKey(User)
    
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})

    class Meta:
        ordering = ['-created_time']
        
    def increase_views(self):
        self.views +=1
        self.save(update_fields=['views'])
```

2.数据库迁移

```shell
python manage.py makemigrations
python manage.py migrate
```

3.修改视图函数

```python
def detail(request,pk):
    '''
    文章详情页视图函数
    :param request:
    :param pk:
    :return:
    '''
    post = get_object_or_404(Post,pk=pk)
    
    post.increase_views()
    
    post.body = markdown(post.body,
                         extensions = [
                             'markdown.extensions.extra',
                             'markdown.extensions.codehilite',
                             'markdown.extensions.toc',
                         ]
                         )
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {'post':post,
               'form':form,
               'comment_list':comment_list,
               }
    return render(request,'blog/detail.html',context=context)
```

4修改模板

`index.html` & `detail.py`

```html
<span class="views-count"><a href="#">{{ post.views }} 阅读</a></span>
```

**Done!**

## 自动生成文章摘要

1.复写`save`方法

```python
class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    excerpt = models.CharField(max_length=200,blank=True)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag,blank=True)
    author = models.ForeignKey(User)

    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})

    class Meta:
        ordering = ['-created_time']

    def increase_views(self):
        self.views +=1
        self.save(update_fields=['views'])

    def save(self,*args,**kwargs):

        if not self.excerpt:
            md = Markdown(
                extensions=[
                    'markdown.extensions.extra',
                    'markdown.extensions.codehilite',
                ]
            )
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super(Post, self).save(*args, **kwargs)
```

2.使用 `truncatechars` 模板过滤器(与上面二选一)

```html
<div class="entry-content clearfix">
	<p>{{ post.body|truncatechars:54 }}</p>
	<div class="read-more cl-effect-14">
		<a href="{{ post.get_absolute_url }}" class="more-link">继续阅读 <span class="metanav">→</span></a>
	</div>
</div>
```

## 基于类的通用视图

- **`ListView`**    

  <!--• model：将 model 指定为 Post，告诉 Django 我要获取的模型是 Post。
  • template_name：指定这个视图渲染的模板。
  • context_object_name：指定获取的模型列表数据保存的变量名。这个变量会被传递给模板。-->

1. 将index函数改为类视图

   ```python
   class IndexView(ListView):
       model = Post
       template_name = 'blog/index.html'
       context_object_name = 'post_list'
   ```

2. 修改`category`函数

   ```python
   class CategoryView(ListView):
       model = Post
       template_name = 'blog/index.html'
       context_object_name = 'post_list'
   
       def get_queryset(self):
           cate = get_object_or_404(Category,pk=self.kwargs.get('pk'))
           return super().get_queryset().filter(category=cate)
   ```

3. 将 `archives` 视图函数改写成类视图

   ```python
   class ArchivesView(ListView):
       model = Post
       template_name = 'blog/index.html'
       context_object_name = 'post_list'
   
       def get_queryset(self):
           return super().get_queryset().filter(
               created_time__year = self.kwargs.get('year'),
               created_time__month = self.kwargs.get('month'),
               )
   ```

4. 修改`url`

   ```python
   from django.conf.urls import url
   
   from . import views
   
   app_name = 'blog'
   urlpatterns = [
       # url(r"^$",views.index,name="index"),
       url(r"^$", views.IndexView.as_view(), name="index"),
       url(r"^post/(?P<pk>[0-9]+)/$",views.detail,name="detail"),
       # url(r"^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$",views.archives,name="archives"),
       url(r"^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$", views.ArchivesView.as_view(), name="archives"),
       # url(r"^category/(?P<pk>[0-9]+)/$",views.category,name="category"),
       url(r"^category/(?P<pk>[0-9]+)/$", views.CategoryView.as_view(), name="category"),
   
   ]
   ```

- **`DetailView`** 

1.  detail 视图函数转换为等价的类视图 `PostDetailView`

   ```python
   class PostDetailView(DetailView):
       model = Post
       template_name = 'blog/detail.html'
       context_object_name = 'post'
   
       def get(self,request,*args,**kwargs):
           response = super().get(request,*args,**kwargs)
           self.object.increase_views()
           return  response
   
       def get_object(self, queryset=None):
           post = super().get_object(queryset=None)
           post.body = markdown(post.body,
                                extensions = [
                                    'markdown.extensions.extra',
                                    'markdown.extensions.codehilite',
                                    'markdown.extensions.toc'
                                ])
           return post
   
       def get_context_data(self, **kwargs):
           context = super().get_context_data(**kwargs)
           form = CommentForm()
           comment_list = self.object.comment_set.all()
           context.update({
               'form':form,
               'comment_list':comment_list,
           })
           return context
   ```

   <!--首先我们为 PostDetailView 类指定了一些属性的值，这些属性的含义和 ListView 中
   是一样的，这里不再重复讲解。
   紧接着我们覆写了 get 方法。这对应着 detail 视图函数中将 post 的阅读量 +1 的
   那部分代码。事实上，你可以简单地把 get 方法的调用看成是 detail 视图函数的调
   用。
   接着我们又复写了 get_object 方法。这对应着 detail 视图函数中根据文章的 id（也
   就是 pk）获取文章，然后对文章的 post.body 进行 Markdown 渲染的代码部
   分。
   最后我们复写了 get_context_data 方法。这部分对应着 detail 视图函数中生成评论表
   单、获取 post 下的评论列表的代码部分。这个方法返回的值是一个字典， 这个字
   典就是模板变量字典，最终会被传递给模板。
   你也许会被这么多方法搞乱，为了便于理解，你可以简单地把 get 方法看成
   是 detail 视图函数，至于其它的像 get_object、 get_context_data 都是辅助方法，这
   些方法最终在 get 方法中被调用，这里你没有看到被调用的原因是它们隐含在
   了 super(PostDetailView, self).get(request, *args, **kwargs) 即父类 get 方法的调用中。
   最终传递给浏览器的 HTTP 响应就是 get 方法返回的 HttpResponse 对象。
   这些方法的相同点：都执行了父类方法，然后对父类方法的返回值进行一些操
   作，最后返回这个修改后的返回值。-->

2. 修改url

   ```python
   from django.conf.urls import url
   
   from . import views
   
   app_name = 'blog'
   urlpatterns = [
       # url(r"^$",views.index,name="index"),
       url(r"^$", views.IndexView.as_view(), name="index"),
       # url(r"^post/(?P<pk>[0-9]+)/$",views.detail,name="detail"),
       url(r"^post/(?P<pk>[0-9]+)/$", views.PostDetailView.as_view(), name="detail"),
       # url(r"^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$",views.archives,name="archives"),
       url(r"^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$", views.ArchivesView.as_view(), name="archives"),
       # url(r"^category/(?P<pk>[0-9]+)/$",views.category,name="category"),
       url(r"^category/(?P<pk>[0-9]+)/$", views.CategoryView.as_view(), name="category"),
   ]
   ```

   