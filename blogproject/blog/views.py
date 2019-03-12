from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from markdown import markdown
from comments.forms import CommentForm
from .models import Post, Category


# Create your views here.

def index(request):
    '''
    首页视图函数
    :param request:
    :return:
    '''
    # return HttpResponse("欢迎来到首页！")
    # return render(request,'blog/index.html',context={'title':"我的博客首页",'welcome':"欢迎访问我的博客首页"})
    post_list = Post.objects.all()
    return render(request,'blog/index.html',context={'post_list':post_list})

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

def archives(request,year,month):
    '''
    归档视图函数
    :param requests:
    :param year:
    :param month:
    :return:
    '''
    post_list = Post.objects.filter(created_time__year=year,created_time__month=month)
    return render(request,'blog/index.html',context={'post_list':post_list})

def category(request,pk):
    '''
    分类视图函数
    :param request:
    :param pk:
    :return:
    '''
    cate = get_object_or_404(Category,pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request,'blog/index.html',context={'post_list':post_list})