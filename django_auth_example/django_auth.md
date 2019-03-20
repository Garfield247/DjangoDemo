## 基本设置

网站提供登录、注册等用户认证功能是一个常见的需求。因此，`Django` 提供了一套功能完整的、灵活的、易于拓展的用户认证系统：`django.contrib.auth`。在本教程中，我将向你展示 `auth` 模块的基本用法，例如如何提供用户注册、登录、修改密码、找回密码等功能；如何拓展 `auth` 内置的 `User` 模型；如何自定义用户验证后台，以支持用户使用诸如邮箱手机号等用户名登录（默认只支持使用用户名登录）等等。

### 开启一个新的 Django 工程

使用 `Django` 提供的命令建立一个新的工程，我命名为 `django_auth_example`。

```
$ django-admin startproject django_auth_example
```

工程建好了，目录结构如下：

```
django_auth_example/
    manage.py
    django_auth_example/
        __init__.py
        settings.py
        urls.py
        wsgi.py
```

### 必要的配置

`Django` 在新建工程时已经为使用用户认证系统做好了全部必要的配置。检查一下 `settings.py` 文件中是否已经做好了全部必要配置。

首先检查一下必要的应用是否已经在 `INSTALLED_APPS` 配置里列出：

```
django_auth_example/settings.py

INSTALLED_APPS = [
    # 其它应用列表...
    'django.contrib.auth',
    'django.contrib.contenttypes',
]
```

为了使用用户认证系统，必须安装以下两个应用：

- django.contrib.auth
- django.contrib.contenttypes

django.contrib.contenttypes 是 auth 模块的用户权限处理部分依赖的应用。

其次需要在中间件 `MIDDLEWARE` 配置里列出以下两个中间件：

- SessionMiddleware 用户处理用户会话。
- AuthenticationMiddleware 绑定一个 User 对象到请求中（具体将在后面介绍）。

即像下面这样的配置：

```
django_auth_example/settings.py

MIDDLEWARE = [
    # 其它中间列表...
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]
```

如果以上配置没问题的话就可以正常地使用用户认证系统了。

### 新建一个应用

即便是目前只使用 Django 用户认证系统的默认特性，推荐的做法也是新建一个应用，用于存放和用户功能相关的代码，为将来可能的功能拓展做准备。因此让我们来新建一个应用，我习惯上把应用命名为 users。

```
$ python manage.py startapp users
```

新建的应用一定要记得在 `settings.py` 里注册，否则 `Django` 无法得知你新建了应用。

```python
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users'
]
```

## 拓展 User 模型

Django 用户认证系统提供了一个内置的 User 对象，用于记录用户的用户名，密码等个人信息。对于 Django 内置的 `User` 模型， 仅包含以下一些主要的属性：

- username，即用户名
- password，密码
- email，邮箱
- first_name，名
- last_name，姓

对于一些网站来说，用户可能还包含有昵称、头像、个性签名等等其它属性，因此仅仅使用 Django 内置的 User 模型是不够。好在 Django 用户系统遵循可拓展的设计原则，我们可以方便地拓展 User 模型。

### 继承 `AbstractUser` 拓展用户模型

这是推荐做法。事实上，查看 `User` 模型的源码就知道，User 也是继承自 `AbstractUser`抽象基类，而且仅仅就是继承了 `AbstractUser`，没有对 `AbstractUser` 做任何的拓展。以下就是 `User` 的源码：

```python
class User(AbstractUser):
    """
    Users within the Django authentication system are represented by this
    model.

    Username, password and email are required. Other fields are optional.
    """
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
```

所以，如果我们继承 `AbstractUser`，将获得 `User` 的全部特性，而且还可以根据自己的需求进行拓展。

我们之前新建了一个 users 应用，通常我们把和数据库模型相关的代码写在 `models.py` 文件里。打开 `users/models.py` 文件，写上我们自定义的用户模型代码：

```python
users/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)

    class Meta(AbstractUser.Meta):
        pass
```

我们给自定义的用户模型新增了一个 nickname（昵称）属性，用来记录用户的昵称信息，设置 `blank=True` 的目的是让用户在注册时无需填写昵称。根据你的需求可以自己进一步拓展，例如增加用户头像、个性签名等等，添加多少属性字段没有任何限制。

同时，我们继承了 `AbstractUser` 的内部类属性 `Meta` ，不过目前什么也没做。在这里继承 `Meta` 的原因是在你的项目中可能需要设置一些 `Meta` 类的属性值，不要忘记继承 `AbstractUser.Meta` 中已有的属性。

**注意：**一定要继承 `AbstractUser`，而不是继承 `auth.User`。尽管 `auth.User` 继承自 `AbstractUser` 且并没有对其进行任何额外拓展，但 `AbstractUser` 是一个抽象类，而 `auth.User` 不是。如果你继承了 `auth.User` 类，这会变成多表继承，在目前的情况下这种继承方式是不被推荐的。关于 Django 的抽象模型类和多表继承，请查阅 Django 的官方文档 [模型继承](https://docs.djangoproject.com/en/1.11/topics/db/models/#model-inheritance)。

此外，`AbstractUser` 类又继承自 `AbstractBaseUser`，前者在后者的基础上拓展了一套用户权限（Permission）系统。因此如非特殊需要，尽量不要从 `AbstractBaseUser` 拓展，否则你需要做更多的额外工作。

为了让 Django 用户认证系统使用我们自定义的用户模型，必须在 settings.py 里通过 `AUTH_USER_MODEL` 指定自定义用户模型所在的位置，即需要如下设置：

```python
django_auth_example/settings.py

# 其它设置...
AUTH_USER_MODEL = 'users.User'
```

即告诉 Django，使用 users 应用下的 `User` 用户模型。

顺便再修改一下语言设置和时区设置：

```python 
django_auth_example/settings.py

# 其它设置...

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
```

设置好自定义用户模型后，生成数据库迁移文件，并且迁移数据库以生成各个应用必要的数据库表。即运行如下两条命令：

```shell
$ python manage.py makemigrations
$ python manage.py migrate
```

OK，现在 `Django` 用户系统使用的用户模型就是自定义的 `User` 模型了。

**注意：**一定要在设置好 `AUTH_USER_MODEL = 'users.User'` 后在第一次迁移数据库，即指定好自定义的用户模型后再执行数据库迁移命令。

### 使用 Profile 模式拓展用户模型

如果想为一个已使用了 `Django` 内置 `User` 模型的项目拓展用户模型，上述继承 `AbstractUser` 的拓展方式会变得有点麻烦。`Django` 没有提供一套自动化的方式将内置的 `User` 迁移到自定义的用户模型，因为 Django 已经为内置的 `User` 模型生成了相关数据库迁移文件和数据库表。如果非要这么做的话，需要手工修改迁移文件和数据库表，并且移动数据库中相关的用户数据。

所以我们采用另一种不改动数据库表的方式来拓展用户模型，具体来说，我们在创建一个模型（通常命名为 Profile）来记录用户相关的数据，然后使用一对一的方式将这个 Profile 模型和 User 关联起来，就好像每个用户都关联着一张记录个人资料的表一样。代码如下：

```python
models.py

from django.contrib.auth.models import User

class Profile(models.Model):
    nickname = models.CharField(max_length=50, blank=True)
    user = models.OneToOneField(User)
```

这种方式和 `AbstractUser` 的区别是，继承 `AbstractUser` 的用户模型只有一张数据库表。而 Profile 这种模式有两张表，一张是 User 模型对应的表，一张是 Profile 模型对应的表，两张表通过一对一的关系关联。可见，当要查询某个用户的 Profile 时，需要执行额外的跨表查询操作，所以这种方式比起直接继承 `AbstractUser` 效率更低一点。因此对于新项目来说，优先推荐使用继承 `AbstractUser` 的方式来拓展用户模型。

PS：如果你使用了Profile 模式，你可能希望在创建 User 对象的时候同时也创建与之关联的 Profile 对象。你可以使用 Django 的 Signal 实现这个需求。由于 Profile 模式不是我们要介绍的重点内容，因此具体的实现细节请参照相关的文档，这里不再赘述。

OK，自定义的 User 模型已经建立好了，接下来就是如何创建用户，即用户注册流程了。

## 注册

用户注册就是创建用户对象，将用户的个人信息保存到数据库里。回顾一下 Django 的 MVT 经典开发流程，对用户注册功能来说，首先创建用户模型（M），这一步我们已经完成了。编写注册视图函数（V），并将为视图函数绑定对应的 URL。编写注册模板（T），模板中提供一个注册表单给用户。Django 用户系统内置了登录、修改密码、找回密码等视图，但是唯独用户注册的视图函数没有提供，这一部分需要我们自己来写。

### 编写用户注册表单

`Django` 已经内置了一个用户注册表单：`django.contrib.auth.forms.UserCreationForm`，不过这个表单的一个小问题是它关联的是 `django` 内置的 `User` 模型，从它的源码中可以看出：

```python
class UserCreationForm(forms.ModelForm):
    ...
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}
```

问题就出在内部类 `Meta` 的 `model` 属性，它的值对应的是 `auth.User`，因此无法用于我们自定义的 User 模型。好在表单实际上就是一个 Python 类，因此我们可以继承它，对它做一点小小的修改就可以了。

表单的代码通常写在 `forms.py` 文件里，因此在 users 应用下新建一个 `forms.py` 文件用于存放表单代码，然后写上如下代码：

```python
users/forms.py

from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")
```

`UserCreationForm` 的 `Meta` 内部类下的 `model` 属性对应的是 auth.User 模型。而 `RegisterForm` 通过覆写父类 `model` 属性的值，将其改为 users.User。

此外 `fields` 用于指定表单的字段，这些指定的字段在模板中会被渲染成表单控件（即一些 `<input>` 等表单控件）。 `UserCreationForm` 中只指定了 `fields = ("username",)`，即用户名，此外还有两个字段密码和确认密码在 `UserCreationForm` 的属性中指定。所以默认的表单渲染后只有用户名（username）、密码、确认密码三个表单控件。我们还希望用户注册时提供邮箱地址，所以在 `fields` 中增加了 email 字段。

**注意：**虽然 `model` 属性的值都被指定为 User，但一个是 auth.User，另一个是 users.User。

#### 编写用户注册视图函数

首先来分析一下注册函数的逻辑。用户在注册表单里填写注册信息，然后通过表单将这些信息提交给服务器。视图函数从用户提交的数据提取用户的注册信息，然后验证这些数据的合法性。如果数据合法，就新建一个用户对象，将用户的数据保存到数据库，否则就将错误信息返回给用户，提示用户对提交的信息进行修改。过程就是这么简单，下面是对应的代码（视图函数的代码通常写在 `views.py` 文件里）：

```python
users/views.py

from django.shortcuts import render, redirect
from .forms import RegisterForm

def register(request):
    # 只有当请求为 POST 时，才表示用户提交了注册信息
    if request.method == 'POST':
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、邮箱（email）
        # 用这些数据实例化一个用户注册表单
        form = RegisterForm(request.POST)

        # 验证数据的合法性
        if form.is_valid():
            # 如果提交数据合法，调用表单的 save 方法将用户数据保存到数据库
            form.save()

            # 注册成功，跳转回首页
            return redirect('/')
    else:
        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        form = RegisterForm()

    # 渲染模板
    # 如果用户正在访问注册页面，则渲染的是一个空的注册表单
    # 如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    return render(request, 'users/register.html', context={'form': form})
```

注意以上视图是处理表单的经典流程，即：

```python
def form_process_view(request):
    if request.method == 'POST':
        # 请求为 POST，利用用户提交的数据构造一个绑定了数据的表单
        form = Form(request.POST)

        if form.is_valid():
            # 表单数据合法
            # 进行其它处理...
            # 跳转
            return redirect('/')
    else:
        # 请求不是 POST，构造一个空表单
        form = Form()

    # 渲染模板
    # 如果不是 POST 请求，则渲染的是一个空的表单
    # 如果用户通过表单提交数据，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    return render(request, 'template.html', context={'form': form})
```

以上逻辑代码稍加修改就可以应用于各种表单处理。

#### 设置 URL 模式

视图函数需要和对应的 URL 绑定，这样当用户访问某个 URL 时，Django 才知道调用哪个视图函数处理用户请求。首先在 **users 应用**下新建一个 urls.py 文件用于设置注册视图函数的 URL 模式。

```python
users/urls.py

from django.conf.urls import url
from . import views

app_name = 'users'
urlpatterns = [
    url(r'^register/', views.register, name='register'),
]
```

`app_name = 'users'` 为这个 urls 模块设置命名空间。关于 URL 模式的设置如果不明白的话请参考相关基础教程，这里不再赘述。

接下来需要在工程的 `urls.py` 文件里包含 users 应用的 URL 模式。打开 `django_auth_example/` 目录下的 `urls.py` 文件，将 `users.urls.py` 包含进来：

```python
django_auth_example/urls.py

from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 别忘记在顶部引入 include 函数
    url(r'^users/', include('users.urls')),
]
```

### 编写注册页面模板

我们在视图函数中渲染了 `users/register.html`，不过目前这个模板文件还不存在，我们这就来创建它。我习惯喜欢将模板文件放在项目根目录（`manage.py` 所在目录）的 `templates/` 目录下，然后在 `templates/` 目录下再新建各个和应用同名的文件夹，用于存放该应用下的模板文件。当然模板放在哪里是无关紧要的，具体视项目而定，只要通过配置模板路径使 `Django` 能够找到模板文件即可。

#### 设置模板目录结构

按照我的习惯，先在项目根目录（`manage.py` 所在目录）新建一个 `templates/` 目录，然后在 `templates/` 目录下新建一个 `users` 目录，用于存放 `users` 应用的相关模板文件。然后在 `users/` 目录下新建一个 `register.html` 模板文件（注意是 `templates/` 下的 `users/` 目录，不是 `users` 应用目录）。此时目录结构变为：

```
django_auth_example/
    manage.py
    django_auth_example/
        __init__.py
        settings.py
        urls.py
        wsgi.py
    templates/
        users/
            register.html
```

#### 配置模板路径

接着需要在 settings.py 里设置 templates/ 所在路径，在 settings.py 找到 `TEMPLATES` 选项，它的内容是这样的：

```python
django_auth_example/settings.py

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

其中 `DIRS` 就是设置模板的路径，在 [] 中写入 `os.path.join(BASE_DIR, 'templates')`，即像下面这样：

```python
django_auth_example/settings.py

TEMPLATES = [
    {
        ...
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        ...
    },
]
```

这里 `BASE_DIR` 是 settings.py 在配置开头前面定义的变量，记录的是工程根目录 django_auth_example/ 的值（注意是最外层的 django_auth_example/ 目录）。在这个目录下有模板文件所在的目录 templates/，于是利用`os.path.join` 把这两个路径连起来，构成完整的模板路径，Django 就知道去这个路径下面找我们的模板了。

#### 渲染注册表单

接下来就是在 register.html 模板中渲染表单了，具体代码如下：

```html
templates/users/register.html 

<!DOCTYPE html>
<html lang="zh-cn">
<head>
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>注册</title>
    <link rel="stylesheet" href="https://unpkg.com/mobi.css/dist/mobi.min.css">
    <style>
        .errorlist {
            color: red;
        }
    </style>
</head>
<body>
<div class="flex-center">
    <div class="container">
        <div class="flex-center">
            <div class="unit-1-2 unit-1-on-mobile">
                <h3>注册</h3>
                <form class="form" action="{% url 'users:register' %}" method="post">
                    {% csrf_token %}
                    {% for field in form %}
                        {{ field.label_tag }}
                        {{ field }}
                        {{ field.errors }}
                        {% if field.help_text %}
                            <p class="help text-small text-muted">{{ field.help_text|safe }}</p>
                        {% endif %}
                    {% endfor %}
                    <button type="submit" class="btn btn-primary btn-block">注册</button>
                </form>
                <div class="flex-center top-gap text-small">
                    <a href="login.html">已有账号登录</a>
                </div>
            </div>
        </div>
    </div>
</div>
</body>
</html>
```

为了使注册页面更加美观，我引入了 mobi.css 提供样式支持。其它的代码请忽略，重点只关注表单部分：

```html
<form class="form" action="{% url 'users:register' %}" method="post">
  {% csrf_token %}
  {% for field in form %}
    {{ field.label_tag }}
    {{ field }}
    {{ field.errors }}
    {% if field.help_text %}
        <p class="help text-small text-muted">{{ field.help_text|safe }}</p>
    {% endif %}
  {% endfor %}
  <button type="submit" class="btn btn-primary btn-block">注册</button>
</form>
```

在 Django 中使用表单，必须注意以下几点：

- 设置表单的 `action` 属性。这个例子中，表单的数据将提交给 `URL /users/register/`，然后 `Django` 调用对应的视图函数 `register` 进行处理。这里我们使用了 `{% url %}` 模板标签，防止 URL 硬编码。
- 设置表单的 method 属性，通常提交 表单数据都是通过 post 方法提交。
- 在表单中加入 {% csrf_token %} 模板标签。这个模板标签的用途就是用于防止跨站请求伪造攻击，提高网站的安全性。至于什么是跨站请求伪造，感兴趣的可以搜索相关资料查阅。这里只需记住只要使用了表单，一定要在表单中加 {% csrf_token %} 模板标签，否则 Django 将不允许你提交表单数据。

接下来就是表单的控件部分。对表单 form（这是一个模板变量，是 `RegisterForm` 的一个实例，我们在 `register` 视图函数中将它传递给模板的。）进行循环就可以得到表单的各个控件：

- {{ field.label_tag }} 是相应控件的 label 标签
- {{ field }} 是相应的表单控件
- {{ field.errors }} 是表单的错误（如果有的话）
- {{ field.help_text|safe }} 是控件相关的帮助信息

例如 `RegisterForm` 表单有用户名字段，渲染的表单控件为：

```html
<label for="id_username">用户名:</label><!-- 对应 {{ field.label_tag }} -->
<input type="text" name="username" id="id_username" autofocus required maxlength="150" /><!-- 对应 {{ field }} -->
<p class="help text-small text-muted">必填。150个字符或者更少。包含字母，数字和仅有的@/./+/-/_符号。</p><!-- 对应 {{ field.help_text }} -->
```

你可以按 F12 看看表单的源代码，对比一下表单控件是哪一部分渲染而成的。这种表单渲染方式是一种比较通用的做法，你可以把它当做一个模板，稍作修改就可以应用与其它需要渲染表单的模板中。

OK，运行开发服务器，访问 http://127.0.0.1:8000/users/register/，可以看到渲染的用户注册表单了。

你可以尝试注册一个用户，或者尝试故意输错一些信息，看看表单渲染的错误信息是什么样的.

### 在 `Admin` 后台查看用户是否注册成功

`如果表单数据没有错误`，提交表单后就会跳转到首页，由于我们没有写任何处理首页的视图函数，所以得到一个 404 错误。不过没有关系，我么你现在只关心用户是否注册成功。那么怎么查看用户是否已经注册成功呢？可以去 `Django Admin` 后台看看是否有用户新注册的数据。为了在 `Admin` 后台查看用户数据，首先需要注册用户模型。打开 `users/admin.py` 文件，在里面注册 users.User 模型：

```python
users/admin.py

from django.contrib import admin
from .models import User

admin.site.register(User)
```

为了进入后台，还要创建一个超级管理员用户，使用 `python manage.py createsuperuser` 创建一个管理员账户即可。

浏览器输入 http://127.0.0.1:8000/admin/，登录管理员账户，可以查看到注册的用户信息了

其中有一个是使用 `createsuperuser` 命令创建的管理员账户，另外是注册的新用户。

至此，注册功能已经完成了。用户注册后就要登录，接下来就是如何提供用户登录功能了。

## 登录

用户已经能够在我们的网站注册了，注册就是为了登录，接下来我们为用户提供登录功能。和注册不同的是，Django 已经为我们写好了登录功能的全部代码，我们不必像之前处理注册流程那样费劲了。只需几分钟的简单配置，就可为用户提供登录功能。接下来就来看看如何使用内置的登录功能。

### 引入内置的 URL 模型

`Django` 内置的登录、修改密码、找回密码等视图函数对应的 URL 模式位于 `django.contrib.auth.urls.py` 中，首先在工程的 `urls.py` 文件里包含这些 URL 模式。打开 `django_auth_example/` 目录下的 `urls.py` 文件，将 `django.contrib.auth.urls.py` 包含进来：

```python
django_auth_example/urls.py

from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^users/', include('users.urls')),
    # 将 auth 应用中的 urls 模块包含进来
    url(r'^users/', include('django.contrib.auth.urls')),
]
```

这将包含以下的 URL 模式：

```
^users/login/$ [name='login']
^users/logout/$ [name='logout']
^users/password_change/$ [name='password_change']
^users/password_change/done/$ [name='password_change_done']
^users/password_reset/$ [name='password_reset']
^users/password_reset/done/$ [name='password_reset_done']
^users/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$ [name='password_reset_confirm']
^users/reset/done/$ [name='password_reset_complete']
```

设置模板路径

默认的登录视图函数渲染的是 `registration/login.html` 模板，因此需要在 `templates/` 目录下新建一个 `registration` 文件夹，再在 `registration/` 目录下新建 `login.html` 模板文件。此时目录结构为：

```
django_auth_example/
    manage.py
    django_auth_example/
        __init__.py
        settings.py
        urls.py
        wsgi.py
    templates/
        users/
            register.html
        registration/
            login.html
```

### 编写登录模板

登录模板的代码和注册模板的代码十分类似：

```html
registration/login.html

<!DOCTYPE html>
<html lang="zh-cn">
<head>
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>登录</title>
    <link rel="stylesheet" href="https://unpkg.com/mobi.css/dist/mobi.min.css">
    <style>
        .errorlist {
            color: red;
        }
    </style>
</head>
<body>
<div class="flex-center">
    <div class="container">
        <div class="flex-center">
            <div class="unit-1-2 unit-1-on-mobile">
                <h3>登录</h3>
                <form class="form" action="{% url 'login' %}" method="post">
                    {% csrf_token %}
                    {{ form.non_field_errors }}
                    {% for field in form %}
                        {{ field.label_tag }}
                        {{ field }}
                        {{ field.errors }}
                        {% if field.help_text %}
                            <p class="help text-small text-muted">{{ field.help_text|safe }}</p>
                        {% endif %}
                    {% endfor %}
                    <button type="submit" class="btn btn-primary btn-block">登录</button>
                </form>
                <div class="flex-left top-gap text-small">
                    <div class="unit-2-3"><span>没有账号？<a href="{% url 'users:register' %}">立即注册</a></span></div>
                    <div class="unit-1-3 flex-right"><span><a href="reset_password.html">忘记密码？</a></span></div>
                </div>
            </div>
        </div>
    </div>
</div>
</body>
</html>
```

为了登录页面的美观我引入了 mobi.css 提供样式支持，其它代码请忽略，我们只关注表单部分的代码。

```html
<form class="form" action="{% url 'login' %}" method="post">
  {% csrf_token %}
  {{ form.non_field_errors }}
  {% for field in form %}
    {{ field.label_tag }}
    {{ field }}
    {{ field.errors }}
    {% if field.help_text %}
        <p class="help text-small text-muted">{{ field.help_text|safe }}</p>
    {% endif %}
  {% endfor %}
  <button type="submit" class="btn btn-primary btn-block">登录</button>
</form>
```

循环表单字段、渲染控件、渲染帮助信息等在注册表单部分已经讲过，登录表单中只引入了一个新的东西：`{{ form.non_field_errors }}`，这显示的同样是表单错误，但是显示的表单错误是和具体的某个表单字段无关的。相对 `{{ field.errors }}`，这个则显示的是具体某个字段的错误。比如对于字段 `username`，如果用户输入的 `username` 不符合要求，比如太长了或者太短了，表单会在 `username` 下方渲染这个错误。但有些表单错误不和任何具体的字段相关，比如用户输入的用户名和密码无法通过验证，这可能是用户输入的用户名不存在，也可能是用户输入的密码错误，因此这个错误信息将通过

 `{{ form.non_field_errors }}` 渲染。

**注意：**你可能觉得用户名不存在错误和 `username` 字段有关，密码错误和 password 字段有关。但是在现代的用户认证系统中，我们不为用户提供这么详细的信息，只是笼统地告知用户名不存在或者密码错误。这能提高一些用户账户的安全性。

此外登录表单的 action 属性的值是 `{% url 'login' %}`，即 `auth` 应用下的 `login` 视图函数对应的 URL，用户提交的表单数据将提交给这个 URL，`Django` 调用 `login` 视图函数来处理。

不要忘了加 `{% csrf_token %}` 模板标签。

现在打开开发服务器，在浏览器输入 http://127.0.0.1:8000/users/login/，你将看到一个用户登陆表单。

故意使用一个不存在的账户登录，或者故意输错密码，你将看到表单渲染的非字段相关的错误。

如果用户登录成功，你会发现跳转到了 http://127.0.0.1:8000/accounts/profile/ 页面。由于我们没有写任何视图函数处理这个 URL，所以看到一个 404 错误。不过没有关系，我们目前只关注用户是否已经登录。

### 如何在模板中判断用户是否已经登录

在模板中判断用户是否已经登录非常简单，使用 `{% if user.is_authenticated %}` 条件判断即可。借此机会，我们来处理一下网站首页。

在 user/views.py 写一个首页视图函数：

```python
user/views.py 

def index(request):
    return render(request, 'index.html')
```

为这个视图函数配置 URL 模式，在 `django_auth_example/urls.py` 进行配置：

```python
from django.conf.urls import url, include
from django.contrib import admin

from users import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 别忘记在顶部引入 include 函数
    url(r'^users/', include('users.urls')),
    url(r'^users/', include('django.contrib.auth.urls')),
    # 别忘记在顶部引入 views 模块
    url(r'^$', views.index, name='index')
]
```

**注意：**直接在项目的 `urls.py` 中配置 URL 是不推荐的，应该在应用的 `urls.py` 下进行配置，然后在项目的 `urls.py` 中通过 `include` 函数包含。不过这里作为示例情况特殊，所以姑且这样做。

由于视图渲染了 `index.html` 文件，因此在 `templates/` 目录下建一个 `index.html` 模板文件（注意我们没有把它放在 `users/` 下，也没放在 `registration/` 下）。然后写上下面的代码：

```html
templates/index.html

<!DOCTYPE html>
<html lang="zh-cn">
<head>
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>首页</title>
    <link rel="stylesheet" href="https://unpkg.com/mobi.css/dist/mobi.min.css">
</head>
<body>
<div class="flex-center">
    <div class="container">
        <div>
            <h1 class="logo"><a href="{% url 'index' %}">Django Auth Example</a></h1>
            {% if user.is_authenticated %}
                <p>你已登录，欢迎你：<a href="#">{{ user.username }}</a></p>
            {% else %}
                <p>你还没有登录，请
                    <button class="btn btn-default"><a href="{% url 'login' %}">登录</a></button>
                    或者
                    <button class="btn btn-default"><a href="{% url 'users:register' %}">注册</a></button>
                </p>
            {% endif %}
        </div>
    </div>
</div>
</body>
</html>
```

为了页面的美观，我引入了 `mobi.css` 提供样式支持。其它代码请忽略，重点只关注用户登录验证部分：

```html
{% if user.is_authenticated %}
    <p>你已登录，欢迎你：<a href="#">{{ user.username }}</a></p>
{% else %}
    <p>你还没有登录，请
    <button class="btn btn-default"><a href="{% url 'login' %}">登录</a></button>
    或者
    <button class="btn btn-default"><a href="{% url 'users:register' %}">注册</a></button>
</p>
{% endif %}
```

`user.is_authenticated` 当用户已经登录时返回 True，否则返回 False。所以已登录的用户将看到欢迎页面，否则将看到登录注册按钮。

你也许奇怪我们在 `index` 视图中并没有传递 `user` 模板变量给 `index.html`，为什么可以在模板中引用 user 呢？这是因为 `Django` 的 `auth` 应用为我们设置了模板常量，所以在任何模板中都可以引用 `{{ user }}`。此外，我们之前提过的 `django.contrib.auth.middleware.AuthenticationMiddleware` 为所有的请求 request 绑定了一个 user 属性。所以在模板中引用 `{{ user }}` 和 `{{ request.user }}` 是等价。

OK 了！不过目前为止，如果你已经登录过了，想要看看未登录的效果会变得比较困难，因为我们还无法注销登录。下面就来给网站添加注销登录的功能吧！

## 注销和页面跳转

当用户想切换登录账号，或者想退出登录状态时，这时候就需要注销已登录的账号。现在我们来为网站添加注销登录的功能，这个功能 Django 也已经为我们提供，我们只需做一点简单配置。

### 注销登录

注销登录的视图为 logout，我们简单修改一下 index.html 的代码，添加一个注销登录的按钮：

```html
templates/index.html

{% if user.is_authenticated %}
  <p>你已登录，欢迎你：<a href="#">{{ user.username }}</a></p>
  <button class="btn btn-default"><a href="{% url 'logout' %}">注销登录</a></button>
{% else %}
  <p>你还没有登录，请
    <button class="btn btn-default"><a href="{% url 'login' %}">登录</a></button>
    或者
    <button class="btn btn-default"><a href="{% url 'users:register' %}">注册</a></button>
  </p>
{% endif %}
```

如果你已经登陆，就会看到一个注销登录的按钮，点击该按钮就会跳转到注销登录已成功地页面。再一次访问首页，你将看到登录、注册按钮，说明你已经成功注销登录状态了。

### 页面跳转

我们之前在登录、注册和注销的过程中发现，登录成功后会跳转到一个 404 页面，注册成功后返回的是首页，而注销登录后跳转到了 `Admin` 后台的注销成功页面。对于一个网站来说，比较好的用户体验是登录、注册和注销后跳转回用户之前访问的页面。。接下来我们看看如何让登录、注册和注销后跳转回用户之前访问的页面。

#### 登录和注销后返回当前页面

在登录和注销的视图函数中，Django 已经为我们处理了跳转回用户之前访问页面的流程。其实现的原理是，在登录和注销的流程中，始终传递一个 next 参数记录用户之前访问页面的 URL。因此，我们需要做的就是在用户访问登录或者注销的页面时，在 URL 中传递一个 next 参数给视图函数，具体做法如下：

```html
templates/index.html

<button class="btn btn-default">
  <a href="{% url 'logout' %}?next={{ request.path }}">注销登录</a>
</button>

<button class="btn btn-default">
  <a href="{% url 'login' %}?next={{ request.path }}">登录</a>
</button>
```

可以看到，我们在登录和注销的 URL 后加了 next 参数，其值为 `{{ request.path }}`。request.path 是用户当前访问页面的 URL。在 URL 中传递参数的方法就是在要传递的参数前加一个 ？然后写上传递的参数名和参数值，用等号链接。关于在 URL 中传递参数具体请 HTTP 的相关协议。

为了在整个登录流程中记录 next 的值，还需要在登录表单中增加一个表单控件，用于传递 next 值。

```html
registration/login.html

<form class="form" action="{% url 'login' %}" method="post">
  ...                 
  <button type="submit" class="btn btn-primary btn-block">登录</button>
  <input type="hidden" name="next" value="{{ next }}"/>
</form>
```

即在表单中增加了一个隐藏的 input 控件，其值为 {{ next }}，即之前通过 URL 参数传递给登录视图函数的，然后登录视图函数又将该值传递给了 login.html 模板。这样在整个登录流程中，始终有一个记录着用户在登录前页面 URL 的变量 next 在视图和模板间来回传递，知道用户登录成功后再跳转回 next 记录的页面 URL。

现在你可以点击登录和注销的按钮来走一遍登录和注销流程，发现页面跳转已经符合我们的需求了。不过还由一点点小瑕疵，就是如果用户不是通过点击登录和注销按钮，而是直接在页面输入 URL 来访问相关页面话，那这个 next 就没有值，从而无法向之前那样跳转回用户之前访问的页面。比如用户想登录，他直接在浏览器的地址栏输入 /users/login/，由于在 URL 中没有传递 next，所以就无法记录用户登录前的页面 URL，那在登录成功后就无法将他带回登录前的页面了。当然这种情况是极为罕见的，很少有用户会记住你网站的 URL 地址，但如果真有这样的用户，我们就把他跳转回首页吧，因为没有任何办法记录他之前访问的页面。要想把用户跳转回首页，可以在 settings 中做如下设置：

```python
LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'
```

这样，整个登录和注销流程就形成了一个闭环。如果用户通过点击登录或者注销按钮登录和注销的话，在登录或者注销成功后就会被带回登录或者注销前的页面，否则将他带回网站首页。

#### 注册后返回当前页面

类似的，我们也希望用户注册后返回注册前页面。不过由于注册视图函数是我们自己写的，之前的处理方式是用户注册成功后将其带回网站首页，因此需要修改一下注册视图函数：

```python
users/views.py

def register(request):
    # 从 get 或者 post 请求中获取 next 参数值
    # get 请求中，next 通过 url 传递，即 /?next=value
    # post 请求中，next 通过表单传递，即 <input type="hidden" name="next" value="{{ next }}"/>
    redirect_to = request.POST.get('next', request.GET.get('next', ''))

    # 只有当请求为 POST 时，才表示用户提交了注册信息
    if request.method == 'POST':
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、确认密码、邮箱（email）
        # 用这些数据实例化一个用户注册表单
        form = RegisterForm(request.POST)

        # 验证数据的合法性
        if form.is_valid():
            # 如果提交数据合法，调用表单的 save 方法将用户数据保存到数据库
            form.save()

            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
    else:
        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        form = RegisterForm()

    # 渲染模板
    # 如果用户正在访问注册页面，则渲染的是一个空的注册表单
    # 如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    # 将记录用户注册前页面的 redirect_to 传给模板，以维持 next 参数在整个注册流程中的传递
    return render(request, 'users/register.html', context={'form': form, 'next': redirect_to})
```

逻辑非常简答，就是首先尝试从用户的 GET 或者 POST 请求中获取 next 参数值，即在注册成功后需要跳转的 URL，如果有值，注册成功后跳转到该 URL，否则跳转回首页。同是不要忘记将该值传给模板，以维持 next 参数在整个注册流程中的传递。

接下来修改模板，和登录模板的设置是一样的：

```html
registration/login.html

<button class="btn btn-default">
  <a href="{% url 'users:register' %}?next={{ request.path }}">注册</a>
</button>
templates/users/register.html

<form class="form" action="{% url 'users:register' %}" method="post">
  ...       
  <button type="submit" class="btn btn-primary btn-block">注册</button>
  <input type="hidden" name="next" value="{{ next }}"/>
</form>
```

**注意：**在注册视图函数中，对 next 的任意值我们都进行了跳转，这可能导致一些安全问题。正确的做法应该是在跳转前，对需要跳转的 URL 做安全性检查。不过这里只作为一个示例，在实际项目中请仔细考虑可能的安全后果，以及添加必要的安全性检查代码。

OK，如此修改以后，用户的登录、注册和注销流程的用户体验可以形成一个比较良好闭环了。接下来就来实现修改密码的功能。