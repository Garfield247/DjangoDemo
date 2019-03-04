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