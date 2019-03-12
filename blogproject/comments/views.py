from django.shortcuts import render, get_object_or_404, redirect
from .forms import CommentForm

# Create your views here.
from blog.models import Post


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