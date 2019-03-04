from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def welcome(request):
    return HttpResponse("HELLO Django!")

def template_test(request):
    context = {'title': '模板测试',
               'welcome': '欢迎来到模板测试页面'}
    return render(request, 'index1.html', context)