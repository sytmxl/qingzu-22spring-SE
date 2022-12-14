from django.db import models
from index.models import House
'''
1.建库时少用外键
2.尽可能少更改这一文件，提早确定这个文件的需求
'''
# Create your models here.
#

class Contract(models.Model):
    ContractID = models.AutoField(primary_key=True,null=False)
    OrderID = models.IntegerField(null=False)
    File = models.FileField(upload_to='',null=True,default='') #合同图片
    FilePath = models.CharField(max_length=255,null=True,default='') #合同图片路由
    Passed = models.BooleanField(default=False) # 是否被管理员审核通过过
    Result = models.BooleanField(default=False)     # 管理员审核结果

class Order(models.Model):
    OrderID = models.AutoField(primary_key=True,null=False)
    OrderDate = models.DateTimeField(null=False)
    DueDate = models.DateTimeField(null=False)
    Price = models.IntegerField(null=False)
    Mark = models.FloatField(null=True)
    Comment = models.CharField(max_length=50,null=True)
    Pay = models.BooleanField(null=False)
    UserID = models.IntegerField(null=False)
    HouseID = models.IntegerField(null=False)

class User(models.Model):
    UserID = models.AutoField(primary_key=True,null=False)
    Email = models.CharField(max_length=255,null=False)
    Username = models.CharField(max_length=255,null=False)
    Password = models.CharField(max_length=255,null=False)
    avatar = models.FileField(upload_to='',null=True,default='') #用户头像文件字段
    avatar_url = models.CharField(max_length=255,default='',null=True) #用户头像路由
    Phone = models.CharField(max_length=11,null=True)
    Status = models.CharField(max_length=1,null=True)  # Y代表用户，G代表管理员，S代表师傅
    Login = models.BooleanField(null=False,default=False)
    City = models.CharField(max_length=255,null=True)
    Job = models.CharField(max_length=255,null=True)
    Introduction = models.TextField(null=True)
    WorkID = models.IntegerField(null=True, default=0)  # 判定师傅空闲 为0则空闲 为一workID则忙于对应work

class Work(models.Model):
    WorkID = models.AutoField(primary_key=True,null=False)
    Datetime = models.DateField(null=False)
    HouseID = models.IntegerField(null=False)
    Description = models.TextField(null=False)
    Picture = models.FileField(upload_to='',null=True,default='') #报修投诉图片
    Picture_url = models.CharField(max_length=255,null=True,default='') #报修投诉图片路由
    UserID = models.IntegerField(null=False)
    WorkerID = models.IntegerField(null=True)
    Comment = models.CharField(max_length=255,null=True)
    Mark = models.FloatField(null=True)
    Status = models.BooleanField(null=False,default=False)
    Admincomment = models.TextField(null=True)
    Workercomment = models.TextField(null=True)
    OrderID = models.IntegerField(null=True)

class UserHouse(models.Model):
    UserID = models.IntegerField(null=False)
    HouseID = models.IntegerField(null=False)
    Mark = models.FloatField(null=True)
