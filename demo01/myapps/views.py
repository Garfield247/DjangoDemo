from django.shortcuts import render
from django.http import HttpResponse

from myapps.models import Student
# Create your views here.

def welcome(request):
    return HttpResponse("HELLO Django!")

def template_test(request):
    context = {'title': '模板测试',
               'welcome': '欢迎来到模板测试页面'}
    return render(request, 'index1.html', context)


def model_test(request):
    studenst = Student.objects.all()
    context = {"title":"模型测试","student":studenst}
    return  render(request,'index2.html',context)

