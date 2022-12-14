# encoding:utf-8
from django.http import JsonResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.conf.global_settings import MEDIA_ROOT
import re,json

from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics,ttfonts
from .models import *
from user.models import *
import datetime
from reportlab.pdfgen import canvas
from django.core import serializers
import shutil

@csrf_exempt
def FirstPage(request): #主界面
    if request.method == 'POST':  # 判断请求方式是否为 POST（要求POST方式）
        querylist = request.POST
        function_id = querylist.get('function_id')
        user_id = querylist.get('user_id')
        user = User.objects.get(UserID=user_id)
        if function_id == '0':  # 我的订单
            orderlist = []
            order = Order.objects.filter(UserID=user_id,Pay=False)
            #如果用户没有订单?
            for x in order:
                y = House.objects.get(HouseID=x.HouseID)
                orderlist.append({
                    'OrderDate':x.OrderDate.date(),
                    'OrderID': x.OrderID,
                    'HouseID': x.HouseID,
                    'LandlordName': y.LandlordName,
                    'LandlordPhone': y.LandlordPhone,
                    'Address': y.Address
                })
            return JsonResponse({'orderlist': orderlist})
        elif function_id == '1':  # 保修投诉
            orderlist = []
            order = Order.objects.filter(UserID=user_id)
            for x in order:
                y = House.objects.get(HouseID=x.HouseID)
                print(x.DueDate)
                orderlist.append({
                    'OrderDate': x.OrderDate.date(),
                    'OrderID': x.OrderID,
                    'HouseID': x.HouseID,
                    'LandlordName': y.LandlordName,
                    'LandlordPhone': y.LandlordPhone,
                    'Address': y.Address
                })
            return JsonResponse({'orderlist': orderlist})
        elif function_id == '2':  # 我的收藏
            houselist = []
            for x in UserHouse.objects.filter(UserID=user_id):
                pics = Picture.objects.filter(HouseID=x.HouseID).values('PicPath')
                house = House.objects.get(HouseID=x.HouseID)
                houselist.append({
                    'HouseID': x.HouseID,
                    'Housename': house.Housename,
                    'Floor':house.Floor,
                    'PicPathList': list(pics),
                    'Address':house.Address,
                    'Area':house.Area,
                    'Housetype':house.Housetype,
                    'Rent':house.Rent,
                })
            return JsonResponse({'houselist': houselist})
        elif function_id == '3':  # 个人资料
            return JsonResponse({'introduction': user.Introduction})
        elif function_id == '4': # 主页
            houselist = []
            allhouse = House.objects.filter()
            for x in allhouse:
                pics = Picture.objects.filter(HouseID=x.HouseID).values('PicPath')
                house = House.objects.get(HouseID=x.HouseID)
                houselist.append({
                    'HouseID': x.HouseID,
                    'Housename': house.Housename,
                    'Floor':house.Floor,
                    'PicPathList': list(pics),
                    'Address': house.Address,
                    'Area': house.Area,
                    'Housetype': house.Housetype,
                    'Rent': house.Rent,
                })
            return JsonResponse({'houselist':houselist})
        elif function_id == '5': #查看
            house_id = querylist.get('house_id')
            house = House.objects.get(HouseID=house_id)
            picturelist = []
            for x in Picture.objects.filter(HouseID=house_id):
                picturelist.append({
                    'PicPathList': x.PicPath
                })
            return JsonResponse({'Mark':house.Mark,
                                 'HouseID':house.HouseID,
                                 'Housename':house.Housename,
                                 'Rent':house.Rent,
                                 'Housetype': house.Housetype,
                                 'Area': house.Area,
                                 'Floor': house.Floor,
                                 'Type': house.Type,
                                 'LandlordPhone': house.LandlordPhone,
                                 'Introduction': house.Introduction,
                                 'Picturelist': picturelist
                                 })
        elif function_id == '6': # 收藏
            house_id = querylist.get('house_id')
            house = House.objects.get(HouseID=house_id)
            if UserHouse.objects.filter(UserID=user_id,HouseID=house_id).exists() == True:
                return JsonResponse({'errornumber': 3, 'message': "用户已收藏！"})
            else:
                new_collection = UserHouse(UserID=user_id,HouseID=house_id,Mark=house.Mark)
                new_collection.save()
                return JsonResponse({'errornumber': 1, 'message': "成功登录并收藏！"})#未成功登录的情况暂时由前端处理
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})

@csrf_exempt
def search(request): #我要租房
    if request.method == 'POST':  # 判断请求方式是否为 POST（要求POST方式）
        querylist = request.POST
        function_id = querylist.get('function_id')
        user_id = querylist.get('user_id')
        user = User.objects.get(UserID=user_id)
        if function_id == '0':  # 我的订单
            orderlist = []
            order = Order.objects.filter(UserID=user_id,Pay=False)
            #如果用户没有订单?
            for x in order:
                y = House.objects.get(HouseID=x.HouseID)
                orderlist.append({
                    'OrderDate':x.OrderDate.date(),
                    'OrderID': x.OrderID,
                    'HouseID': x.HouseID,
                    'LandlordName': y.LandlordName,
                    'LandlordPhone': y.LandlordPhone,
                    'Address': y.Address
                })
            return JsonResponse({'orderlist': orderlist})
        elif function_id == '1':  # 保修投诉
            orderlist = []
            order = Order.objects.filter(UserID=user_id)
            for x in order:
                y = House.objects.get(HouseID=x.HouseID)
                print(x.DueDate)
                orderlist.append({
                    'OrderDate': x.OrderDate.date(),
                    'OrderID': x.OrderID,
                    'HouseID': x.HouseID,
                    'LandlordName': y.LandlordName,
                    'LandlordPhone': y.LandlordPhone,
                    'Address': y.Address
                })
            return JsonResponse({'orderlist': orderlist})
        elif function_id == '2':  # 我的收藏
            houselist = []
            for x in UserHouse.objects.filter(UserID=user_id):
                pics = Picture.objects.filter(HouseID=x.HouseID).values('PicPath')
                house = House.objects.get(HouseID=x.HouseID)
                houselist.append({
                    'HouseID': x.HouseID,
                    'Housename': house.Housename,
                    'Floor':house.Floor,
                    'PicPathList': list(pics),
                    'Address':house.Address,
                    'Area':house.Area,
                    'Housetype':house.Housetype,
                    'Rent':house.Rent,
                })
            return JsonResponse({'houselist': houselist})
        elif function_id == '3':  # 个人资料
            return JsonResponse({'introduction': user.Introduction})
        elif function_id == '4': # 主页
            houselist = []
            allhouse = House.objects.filter()
            for x in allhouse:
                pics = Picture.objects.filter(HouseID=x.HouseID).values('PicPath')
                house = House.objects.get(HouseID=x.HouseID)
                houselist.append({
                    'HouseID': x.HouseID,
                    'Housename': house.Housename,
                    'Floor':house.Floor,
                    'PicPathList': list(pics),
                    'Address': house.Address,
                    'Area': house.Area,
                    'Housetype': house.Housetype,
                    'Rent': house.Rent,
                })
            return JsonResponse({'houselist':houselist})
        elif function_id == '5': #查看
            house_id = querylist.get('house_id')
            house = House.objects.get(HouseID=house_id)
            return JsonResponse({'Mark':house.Mark,
                                 'HouseID':house.HouseID,
                                 'Housename':house.Housename,
                                 'Rent':house.Rent,
                                 'Housetype': house.Housetype,
                                 'Area': house.Area,
                                 'Floor': house.Floor,
                                 'Type': house.Type,
                                 'LandlordPhone': house.LandlordPhone,
                                 'Introduction': house.Introduction})
        elif function_id == '6': # 收藏
            house_id = querylist.get('house_id')
            house = House.objects.get(HouseID=house_id)
            if UserHouse.objects.filter(UserID=user_id,HouseID=house_id).exists() == True:
                return JsonResponse({'errornumber': 3, 'message': "用户已收藏！"})
            else:
                new_collection = UserHouse(UserID=user_id,HouseID=house_id,Mark=house.Mark)
                new_collection.save()
                return JsonResponse({'errornumber': 1, 'message': "成功登录并收藏！"})#未成功登录的情况暂时由前端处理
        elif function_id == '7': #房源搜索
            house_name = querylist.get('house_name')
            houses = House.objects.filter(Housename__contains=house_name)
            # return JsonResponse(list(response), safe=False, json_dumps_params={'ensure_ascii': False})
            houselist = []
            for house in houses:
                pics = Picture.objects.filter(HouseID=house.HouseID).values('PicPath')
                houselist.append({
                    'HouseID': house.HouseID,
                    'PicPathList': list(pics),
                    'Address': house.Address,
                    'Area': house.Area,
                    'Housetype': house.Housetype,
                    'Rent': house.Rent,
                    'Floor': house.Floor,
                    'Housename': house.Housename
                })
            return JsonResponse({'houselist': houselist})
        elif function_id == '8': #房源筛选
            city = querylist.get('city')
            type = querylist.get('type')
            rent = querylist.get('rent')
            houses = House.objects.filter()
            if (city != 'undefined/undefined/undefined')and(city!='无/undefined/undefined'):
                lay = city.split('/')
                if lay[1] == '市辖区':
                    city = lay[0][:-1] + lay[2][:-1]
                else:
                    city = lay[1][:-1] + lay[2][:-1]
                houses = houses.filter(Address=city)
            if (type != '')and(type !='无'):
                houses = houses.filter(Housetype=type)

            if rent == '1':
                houses = houses.filter(Rent__lte=1000)
            if rent == '2':
                houses = houses.filter(Rent__gte=1000).filter(Rent__lte=3000)
            if rent == '3':
                houses = houses.filter(Rent__gte=3000).filter(Rent__lte=5000)
            if rent == '4':
                houses = houses.filter(Rent__gte=5000).filter(Rent__lte=10000)
            if rent == '5':
                houses = houses.filter(Rent__gte=10000)

            houselist = []
            for house in houses:
                pics = Picture.objects.filter(HouseID=house.HouseID).values('PicPath')
                houselist.append({
                    'HouseID': house.HouseID,
                    'PicPathList': list(pics),
                    'Address': house.Address,
                    'Area': house.Area,
                    'Housetype': house.Housetype,
                    'Rent': house.Rent,
                    'Floor': house.Floor,
                    'Housename': house.Housename
                })
            return JsonResponse({'houselist': houselist})
        elif function_id == '9': #提交申请
            house_id = querylist.get('house_id')
            house = House.objects.get(HouseID=house_id,Status=False)
            start_day = datetime.datetime.strptime(querylist.get('start_day'), '%Y-%m-%d').date()
            finish_day = datetime.datetime.strptime(querylist.get('finish_day'), '%Y-%m-%d').date()
            day = (finish_day-start_day).days
            type = querylist.get('type')
            price = house.Rent*day
            if type == '1': #短租
                return JsonResponse({'DayRent':house.Rent,'day':day,'Price':price})
            elif type == '2':
                return JsonResponse({'LandlordName':house.LandlordName,'Username':user.Username,'Address':house.Address,'Area':house.Area,'day':day,'starttime':str(start_day)})
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})

@csrf_exempt
def order(request):
    if request.method == 'POST':  # 判断请求方式是否为 POST（要求POST方式）
        querylist = request.POST
        function_id = querylist.get('function_id')
        user_id = querylist.get('user_id')
        user = User.objects.get(UserID=user_id)
        if function_id == '0':  # 我的订单
            orderlist = []
            order = Order.objects.filter(UserID=user_id,Pay=False)
            for x in order:
                y = House.objects.get(HouseID=x.HouseID)
                orderlist.append({
                    'OrderDate':x.OrderDate.date(),
                    'OrderID': x.OrderID,
                    'HouseID': x.HouseID,
                    'LandlordName': y.LandlordName,
                    'LandlordPhone': y.LandlordPhone,
                    'Address': y.Address
                })
            return JsonResponse({'orderlist': orderlist})
        elif function_id == '1':  # 保修投诉
            orderlist = []
            order = Order.objects.filter(UserID=user_id)
            for x in order:
                y = House.objects.get(HouseID=x.HouseID)
                print(x.DueDate)
                orderlist.append({
                    'OrderDate': x.OrderDate.date(),
                    'OrderID': x.OrderID,
                    'HouseID': x.HouseID,
                    'LandlordName': y.LandlordName,
                    'LandlordPhone': y.LandlordPhone,
                    'Address': y.Address
                })
            return JsonResponse({'orderlist': orderlist})
        elif function_id == '2':  # 我的收藏
            houselist = []
            for x in UserHouse.objects.filter(UserID=user_id):
                pics = Picture.objects.filter(HouseID=x.HouseID).values('PicPath')
                house = House.objects.get(HouseID=x.HouseID)
                houselist.append({
                    'HouseID': x.HouseID,
                    'Housename': house.Housename,
                    'Floor':house.Floor,
                    'PicPathList': list(pics),
                    'Address':house.Address,
                    'Area':house.Area,
                    'Housetype':house.Housetype,
                    'Rent':house.Rent,
                })
            return JsonResponse({'houselist': houselist})
        elif function_id == '3':  # 个人资料
            return JsonResponse({'introduction': user.Introduction})
        elif function_id == '4': # 主页
            houselist = []
            allhouse = House.objects.filter()
            for x in allhouse:
                pics = Picture.objects.filter(HouseID=x.HouseID).values('PicPath')
                house = House.objects.get(HouseID=x.HouseID)
                houselist.append({
                    'HouseID': x.HouseID,
                    'Housename': house.Housename,
                    'Floor':house.Floor,
                    'PicPathList': list(pics),
                    'Address': house.Address,
                    'Area': house.Area,
                    'Housetype': house.Housetype,
                    'Rent': house.Rent,
                })
            return JsonResponse({'houselist': houselist})
        elif function_id == '5': #正在处理
            order = Order.objects.filter(UserID=user_id)
            orderlist = []
            for x in order:
                if Contract.objects.filter(OrderID=x.OrderID).exists():
                    contract = Contract.objects.get(OrderID=x.OrderID)
                    if contract.Passed == False:
                        y = House.objects.get(HouseID=x.HouseID)
                        orderlist.append({
                            'OrderDate': x.OrderDate.date(),
                            'OrderID': x.OrderID,
                            'HouseID': x.HouseID,
                            'LandlordName': y.LandlordName,
                            'LandlordPhone': y.LandlordPhone,
                            'Address': y.Address
                        })
            return JsonResponse({'orderlist': orderlist})
        elif function_id == '6': #历史记录
            order = Order.objects.filter(UserID=user_id)
            orderlist = []
            for x in order:
                if not Contract.objects.filter(OrderID=x.OrderID).exists():
                    print(x.OrderID)
                    y = House.objects.get(HouseID=x.HouseID)
                    orderlist.append({
                        'OrderDate': x.OrderDate.date(),
                        'OrderID': x.OrderID,
                        'HouseID': x.HouseID,
                        'LandlordName': y.LandlordName,
                        'LandlordPhone': y.LandlordPhone,
                        'Address': y.Address
                })
                else:
                    contract = Contract.objects.get(OrderID=x.OrderID)
                    if contract.Passed == True:
                        y = House.objects.get(HouseID=x.HouseID)
                        orderlist.append({
                            'OrderDate': x.OrderDate.date(),
                            'OrderID': x.OrderID,
                            'HouseID': x.HouseID,
                            'LandlordName': y.LandlordName,
                            'LandlordPhone': y.LandlordPhone,
                            'Address': y.Address
                        })
            return JsonResponse({'orderlist': orderlist})
        elif function_id == '7': #订单详情
            order_id = querylist.get('order_id')
            order = Order.objects.get(OrderID=order_id,Pay=True)
            house_id = order.HouseID
            house = House.objects.get(HouseID=house_id)
            return JsonResponse({'Mark':house.Mark,
                                 'HouseID':house.HouseID,
                                 'Housename':house.Housename,
                                 'Rent':house.Rent,
                                 'Housetype': house.Housetype,
                                 'Area': house.Area,
                                 'Floor': house.Floor,
                                 'Type': house.Type,
                                 'LandlordPhone': house.LandlordPhone,
                                 'OrderDate': order.OrderDate.date(),
                                 'DueDate': order.DueDate.date(),
                                 'Introduction': house.Introduction})
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})

@csrf_exempt
def info_order(request):
    if request.method == 'POST':
        querylist = request.POST
        function_id = querylist.get('function_id')
        user_id = querylist.get('user_id')
        user = User.objects.get(UserID=user_id)
        if function_id == '0':  # 我的订单
            orderlist = []
            order = Order.objects.filter(UserID=user_id, Pay=False)
            # 如果用户没有订单?
            for x in order:
                y = House.objects.get(HouseID=x.HouseID)
                orderlist.append({
                    'OrderDate': x.OrderDate.date(),
                    'OrderID': x.OrderID,
                    'HouseID': x.HouseID,
                    'LandlordName': y.LandlordName,
                    'LandlordPhone': y.LandlordPhone,
                    'Address': y.Address
                })
            return JsonResponse({'orderlist': orderlist})
        elif function_id == '1':  # 保修投诉
            orderlist = []
            order = Order.objects.filter(UserID=user_id)
            for x in order:
                y = House.objects.get(HouseID=x.HouseID)
                print(x.DueDate)
                orderlist.append({
                    'OrderDate': x.OrderDate.date(),
                    'OrderID': x.OrderID,
                    'HouseID': x.HouseID,
                    'LandlordName': y.LandlordName,
                    'LandlordPhone': y.LandlordPhone,
                    'Address': y.Address
                })
            return JsonResponse({'orderlist': orderlist})
        elif function_id == '2':  # 我的收藏
            houselist = []
            for x in UserHouse.objects.filter(UserID=user_id):
                pics = Picture.objects.filter(HouseID=x.HouseID).values('PicPath')
                house = House.objects.get(HouseID=x.HouseID)
                houselist.append({
                    'HouseID': x.HouseID,
                    'Housename': house.Housename,
                    'Floor': house.Floor,
                    'PicPathList': list(pics),
                    'Address': house.Address,
                    'Area': house.Area,
                    'Housetype': house.Housetype,
                    'Rent': house.Rent,
                })
            return JsonResponse({'houselist': houselist})
        elif function_id == '3':  # 个人资料
            return JsonResponse({'introduction': user.Introduction})
        elif function_id == '4':  # 主页
            houselist = []
            allhouse = House.objects.filter()
            for x in allhouse:
                pics = Picture.objects.filter(HouseID=x.HouseID).values('PicPath')
                house = House.objects.get(HouseID=x.HouseID)
                houselist.append({
                    'HouseID': x.HouseID,
                    'Housename': house.Housename,
                    'Floor': house.Floor,
                    'PicPathList': list(pics),
                    'Address': house.Address,
                    'Area': house.Area,
                    'Housetype': house.Housetype,
                    'Rent': house.Rent,
                })
            return JsonResponse({'houselist': houselist})
    else:
        return  JsonResponse({'errornumber': 2, 'message': "请求方式错误"})

@csrf_exempt
def service(request):
    if request.method == 'POST':
        querylist = request.POST
        function_id = querylist.get('function_id')
        user_id = querylist.get('user_id')
        user = User.objects.get(UserID=user_id)
        if function_id == '0':  # 我的订单
            orderlist = []
            order = Order.objects.filter(UserID=user_id, Pay=False)
            for x in order:
                y = House.objects.get(HouseID=x.HouseID)
                orderlist.append({
                    'OrderDate': x.OrderDate.date(),
                    'OrderID': x.OrderID,
                    'HouseID': x.HouseID,
                    'LandlordName': y.LandlordName,
                    'LandlordPhone': y.LandlordPhone,
                    'Address': y.Address
                })
            return JsonResponse({'orderlist': orderlist})
        elif function_id == '1':  # 保修投诉
            orderlist = []
            order = Order.objects.filter(UserID=user_id)
            for x in order:
                y = House.objects.get(HouseID=x.HouseID)
                print(x.DueDate)
                orderlist.append({
                    'OrderDate': x.OrderDate.date(),
                    'OrderID': x.OrderID,
                    'HouseID': x.HouseID,
                    'LandlordName': y.LandlordName,
                    'LandlordPhone': y.LandlordPhone,
                    'Address': y.Address
                })
            return JsonResponse({'orderlist': orderlist})
        elif function_id == '2':  # 我的收藏
            houselist = []
            for x in UserHouse.objects.filter(UserID=user_id):
                pics = Picture.objects.filter(HouseID=x.HouseID).values('PicPath')
                house = House.objects.get(HouseID=x.HouseID)
                houselist.append({
                    'HouseID': x.HouseID,
                    'Housename': house.Housename,
                    'Floor': house.Floor,
                    'PicPathList': list(pics),
                    'Address': house.Address,
                    'Area': house.Area,
                    'Housetype': house.Housetype,
                    'Rent': house.Rent,
                })
            return JsonResponse({'houselist': houselist})
        elif function_id == '3':  # 个人资料
            return JsonResponse({'introduction': user.Introduction})
        elif function_id == '4':  # 主页
            houselist = []
            allhouse = House.objects.filter()
            for x in allhouse:
                pics = Picture.objects.filter(HouseID=x.HouseID).values('PicPath')
                house = House.objects.get(HouseID=x.HouseID)
                houselist.append({
                    'HouseID': x.HouseID,
                    'Housename': house.Housename,
                    'Floor': house.Floor,
                    'PicPathList': list(pics),
                    'Address': house.Address,
                    'Area': house.Area,
                    'Housetype': house.Housetype,
                    'Rent': house.Rent,
                })
            return JsonResponse({'houselist': houselist})
        elif function_id == '5': # 历史订单
            order = Order.objects.filter(UserID=user_id, Pay=True)
            orderlist = []
            for x in order:
                contract = Contract.objects.get(OrderID=x.OrderID)
                if contract.Passed == True:
                    y = House.objects.get(HouseID=x.HouseID)
                    orderlist.append({
                        'OrderDate': x.OrderDate.date(),
                        'OrderID': x.OrderID,
                        'HouseID': x.HouseID,
                        'LandlordName': y.LandlordName,
                        'LandlordPhone': y.LandlordPhone,
                        'Address': y.Address
                    })
            return JsonResponse({'orderlist': orderlist})
        elif function_id == '6': #正在处理保修
            work = Work.objects.filter(UserID=user_id,Status=False)
            worklist = []
            for x in work:
                y=House.objects.get(HouseID=x.HouseID)
                worklist.append({
                    'Datetime':x.Datetime,
                    'OrderID':x.OrderID,
                    'Address':y.Address,
                    'WorkID':x.WorkID
                })
            return JsonResponse({'worklist': worklist})
        elif function_id == '7': #历史完成报修
            work = Work.objects.filter(UserID=user_id,Status=True)
            worklist = []
            for x in work:
                y=House.objects.get(HouseID=x.HouseID)
                worklist.append({
                    'Datetime':x.Datetime,
                    'OrderID':x.OrderID,
                    'Address':y.Address,
                    'WorkID': x.WorkID
                })
            return JsonResponse({'worklist': worklist})
        elif function_id == '8': # 查看历史订单详情
            order_id = querylist.get('order_id')
            order = Order.objects.get(OrderID=order_id)
            house_id = order.HouseID
            house = House.objects.get(HouseID=house_id)
            return JsonResponse({'Mark':house.Mark,
                                 'HouseID':house.HouseID,
                                 'Housename':house.Housename,
                                 'Rent':house.Rent,
                                 'Housetype': house.Housetype,
                                 'Area': house.Area,
                                 'Floor': house.Floor,
                                 'Type': house.Type,
                                 'LandlordPhone': house.LandlordPhone,
                                 'OrderDate': order.OrderDate.date(),
                                 'DueDate': order.DueDate.date(),
                                 'Introduction': house.Introduction})
        elif function_id == '9': #我要报修投诉
            order_id = querylist.get('order_id')
            order = Order.objects.get(OrderID=order_id)
            house_id = order.HouseID
            house = House.objects.get(HouseID=house_id)
            return JsonResponse({'Mark':house.Mark,
                                 'HouseID':house.HouseID,
                                 'Housename':house.Housename,
                                 'Rent':house.Rent,
                                 'Housetype': house.Housetype,
                                 'Area': house.Area,
                                 'Floor': house.Floor,
                                 'Type': house.Type,
                                 'LandlordPhone': house.LandlordPhone,
                                 'OrderDate': order.OrderDate.date(),
                                 'DueDate': order.DueDate.date(),
                                 'Introduction': house.Introduction})
        elif function_id == '10':#查看投诉详情
            work_id=querylist.get('work_id')
            work = Work.objects.get(WorkID=work_id)
            house_id = work.HouseID
            house = House.objects.get(HouseID=house_id)
            order = Order.objects.get(OrderID=work.OrderID)
            return JsonResponse({'HouseID':house.HouseID,
                                 'Housename':house.Housename,
                                 'Rent':house.Rent,
                                 'Housetype': house.Housetype,
                                 'Area': house.Area,
                                 'Floor': house.Floor,
                                 'Type': house.Type,
                                 'LandlordPhone': house.LandlordPhone,
                                 'OrderDate': order.OrderDate.date(),
                                 'DueDate': order.DueDate.date(),
                                 'Introduction': house.Introduction,
                                 'ComplainPic':work.Picture_url,
                                 'ComplainText':work.Description})
        elif function_id == '11':#联系师傅/客服
            work_id = querylist.get('work_id')
            list = Message.objects.filter(WorkID=work_id)
            messagelist = []
            for x in list:
                messagelist.append({
                    'errnum':x.Errornumber,
                    'id':x.UserID,
                    'text':x.Text,
                    'name':x.Username
                })
            return JsonResponse({'massagelist':messagelist})
        elif function_id == '12':#进入我要报修/投诉界面
            order_id = querylist.get('order_id')
            order = Order.objects.get(OrderID=order_id)
            house_id = order.HouseID
            house = House.objects.get(HouseID=house_id)
            return JsonResponse({'Mark':house.Mark,
                                 'HouseID':house.HouseID,
                                 'Housename':house.Housename,
                                 'Rent':house.Rent,
                                 'Housetype': house.Housetype,
                                 'Area': house.Area,
                                 'Floor': house.Floor,
                                 'Type': house.Type,
                                 'LandlordPhone': house.LandlordPhone,
                                 'OrderDate': order.OrderDate.date(),
                                 'DueDate': order.DueDate.date(),
                                 'Introduction': house.Introduction})
        elif function_id == '13': #提交
            now = datetime.datetime.now().date()
            order_id = querylist.get('order_id')
            order = Order.objects.get(OrderID=order_id)
            house_id = order.HouseID
            description = querylist.get('description')
            picture = request.FILES.get('picture')
            suffix = '.' + picture.name.split('.')[-1]
            picture.name = str(order_id)+'报修投诉'+suffix
            new_work = Work(Datetime=now, HouseID=house_id, Description=description, UserID=user_id,OrderID=order_id,Picture=picture,Status = False)
            new_work.save()
            new_work.Picture_url = "http://127.0.0.1:8000/media/" + new_work.Picture.name
            print(new_work.Picture.name)
            new_work.save()
            return JsonResponse({'errornumber': 1, 'message': "提交投诉/报修成功！",'picture_url':new_work.Picture_url})
        elif function_id == '14': #提交留言
            work_id = querylist.get('work_id')
            Errornumber = querylist.get('errornumber')
            UserID = querylist.get('id')
            Text = querylist.get('text')
            Username = querylist.get('name')
            new_message = Message(Errornumber=Errornumber,UserID = UserID,Text = Text,Username = Username,WorkID=work_id)
            new_message.save()
            return JsonResponse({'errornumber': 1, 'message': "留言成功！"})
        elif function_id == '15': #评分
            work_id = querylist.get('work_id')
            mark = querylist.get('mark')
            work = Work.objects.get(WorkID=work_id)
            work.Mark = mark
            work.Status = True
            work.save()
            return JsonResponse({'errornumber': 1, 'message': "评分成功！"})

    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})

@csrf_exempt
def info_complain(request):
    if request.method == 'POST':
        querylist = request.POST
        function_id = querylist.get('function_id')
        user_id = querylist.get('user_id')
        user = User.objects.get(UserID=user_id)
        if function_id == '0':  # 我的订单
            orderlist = []
            order = Order.objects.filter(UserID=user_id, Pay=False)
            # 如果用户没有订单?
            for x in order:
                y = House.objects.get(HouseID=x.HouseID)
                orderlist.append({
                    'OrderDate': x.OrderDate.date(),
                    'OrderID': x.OrderID,
                    'HouseID': x.HouseID,
                    'LandlordName': y.LandlordName,
                    'LandlordPhone': y.LandlordPhone,
                    'Address': y.Address
                })
            return JsonResponse({'orderlist': orderlist})
        elif function_id == '1':  # 保修投诉
            orderlist = []
            order = Order.objects.filter(UserID=user_id)
            for x in order:
                y = House.objects.get(HouseID=x.HouseID)
                print(x.DueDate)
                orderlist.append({
                    'OrderDate': x.OrderDate.date(),
                    'OrderID': x.OrderID,
                    'HouseID': x.HouseID,
                    'LandlordName': y.LandlordName,
                    'LandlordPhone': y.LandlordPhone,
                    'Address': y.Address
                })
            return JsonResponse({'orderlist': orderlist})
        elif function_id == '2':  # 我的收藏
            houselist = []
            for x in UserHouse.objects.filter(UserID=user_id):
                pics = Picture.objects.filter(HouseID=x.HouseID).values('PicPath')
                house = House.objects.get(HouseID=x.HouseID)
                houselist.append({
                    'HouseID': x.HouseID,
                    'Housename': house.Housename,
                    'Floor': house.Floor,
                    'PicPathList': list(pics),
                    'Address': house.Address,
                    'Area': house.Area,
                    'Housetype': house.Housetype,
                    'Rent': house.Rent,
                })
            return JsonResponse({'houselist': houselist})
        elif function_id == '3':  # 个人资料
            return JsonResponse({'introduction': user.Introduction})
        elif function_id == '4':  # 主页
            houselist = []
            allhouse = House.objects.filter()
            for x in allhouse:
                pics = Picture.objects.filter(HouseID=x.HouseID).values('PicPath')
                house = House.objects.get(HouseID=x.HouseID)
                houselist.append({
                    'HouseID': x.HouseID,
                    'Housename': house.Housename,
                    'Floor': house.Floor,
                    'PicPathList': list(pics),
                    'Address': house.Address,
                    'Area': house.Area,
                    'Housetype': house.Housetype,
                    'Rent': house.Rent,
                })
            return JsonResponse({'houselist': houselist})
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})

@csrf_exempt
def connect(request):
    if request.method == 'POST':
        querylist = request.POST
        function_id = querylist.get('function_id')
        user_id = querylist.get('user_id')
        user = User.objects.get(UserID=user_id)
        if function_id == '0':  # 我的订单
            orderlist = []
            order = Order.objects.filter(UserID=user_id, Pay=False)
            # 如果用户没有订单?
            for x in order:
                y = House.objects.get(HouseID=x.HouseID)
                orderlist.append({
                    'OrderDate': x.OrderDate.date(),
                    'OrderID': x.OrderID,
                    'HouseID': x.HouseID,
                    'LandlordName': y.LandlordName,
                    'LandlordPhone': y.LandlordPhone,
                    'Address': y.Address
                })
            return JsonResponse({'orderlist': orderlist})
        elif function_id == '1':  # 保修投诉
            orderlist = []
            order = Order.objects.filter(UserID=user_id)
            for x in order:
                y = House.objects.get(HouseID=x.HouseID)
                print(x.DueDate)
                orderlist.append({
                    'OrderDate': x.OrderDate.date(),
                    'OrderID': x.OrderID,
                    'HouseID': x.HouseID,
                    'LandlordName': y.LandlordName,
                    'LandlordPhone': y.LandlordPhone,
                    'Address': y.Address
                })
            return JsonResponse({'orderlist': orderlist})
        elif function_id == '2':  # 我的收藏
            houselist = []
            for x in UserHouse.objects.filter(UserID=user_id):
                pics = Picture.objects.filter(HouseID=x.HouseID).values('PicPath')
                house = House.objects.get(HouseID=x.HouseID)
                houselist.append({
                    'HouseID': x.HouseID,
                    'Housename': house.Housename,
                    'Floor': house.Floor,
                    'PicPathList': list(pics),
                    'Address': house.Address,
                    'Area': house.Area,
                    'Housetype': house.Housetype,
                    'Rent': house.Rent,
                })
            return JsonResponse({'houselist': houselist})
        elif function_id == '3':  # 个人资料
            return JsonResponse({'introduction': user.Introduction})
        elif function_id == '4':  # 主页
            houselist = []
            allhouse = House.objects.filter()
            for x in allhouse:
                pics = Picture.objects.filter(HouseID=x.HouseID).values('PicPath')
                house = House.objects.get(HouseID=x.HouseID)
                houselist.append({
                    'HouseID': x.HouseID,
                    'Housename': house.Housename,
                    'Floor': house.Floor,
                    'PicPathList': list(pics),
                    'Address': house.Address,
                    'Area': house.Area,
                    'Housetype': house.Housetype,
                    'Rent': house.Rent,
                })
            return JsonResponse({'houselist': houselist})
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})

@csrf_exempt
def collection(request):
    if request.method == 'POST':
        querylist = request.POST
        function_id = querylist.get('function_id')
        user_id = querylist.get('user_id')
        user = User.objects.get(UserID=user_id)
        if function_id == '0':  # 我的订单
            orderlist = []
            order = Order.objects.filter(UserID=user_id, Pay=False)
            # 如果用户没有订单?
            for x in order:
                y = House.objects.get(HouseID=x.HouseID)
                orderlist.append({
                    'OrderDate': x.OrderDate.date(),
                    'OrderID': x.OrderID,
                    'HouseID': x.HouseID,
                    'LandlordName': y.LandlordName,
                    'LandlordPhone': y.LandlordPhone,
                    'Address': y.Address
                })
            return JsonResponse({'orderlist': orderlist})
        elif function_id == '1':  # 保修投诉
            orderlist = []
            order = Order.objects.filter(UserID=user_id)
            for x in order:
                y = House.objects.get(HouseID=x.HouseID)
                print(x.DueDate)
                orderlist.append({
                    'OrderDate': x.OrderDate.date(),
                    'OrderID': x.OrderID,
                    'HouseID': x.HouseID,
                    'LandlordName': y.LandlordName,
                    'LandlordPhone': y.LandlordPhone,
                    'Address': y.Address
                })
            return JsonResponse({'orderlist': orderlist})
        elif function_id == '2':  # 我的收藏
            houselist = []
            for x in UserHouse.objects.filter(UserID=user_id):
                pics = Picture.objects.filter(HouseID=x.HouseID).values('PicPath')
                house = House.objects.get(HouseID=x.HouseID)
                houselist.append({
                    'HouseID': x.HouseID,
                    'Housename': house.Housename,
                    'Floor': house.Floor,
                    'PicPathList': list(pics),
                    'Address': house.Address,
                    'Area': house.Area,
                    'Housetype': house.Housetype,
                    'Rent': house.Rent,
                })
            return JsonResponse({'houselist': houselist})
        elif function_id == '3':  # 个人资料
            return JsonResponse({'introduction': user.Introduction})
        elif function_id == '4':  # 主页
            houselist = []
            allhouse = House.objects.filter()
            for x in allhouse:
                pics = Picture.objects.filter(HouseID=x.HouseID).values('PicPath')
                house = House.objects.get(HouseID=x.HouseID)
                houselist.append({
                    'HouseID': x.HouseID,
                    'Housename': house.Housename,
                    'Floor': house.Floor,
                    'PicPathList': list(pics),
                    'Address': house.Address,
                    'Area': house.Area,
                    'Housetype': house.Housetype,
                    'Rent': house.Rent,
                })
            return JsonResponse({'houselist': houselist})
        elif function_id == '5': #查看
            house_id = querylist.get('house_id')
            house = House.objects.get(HouseID=house_id)
            return JsonResponse({'Mark':house.Mark,
                                 'HouseID':house.HouseID,
                                 'Housename':house.Housename,
                                 'Rent':house.Rent,
                                 'Housetype': house.Housetype,
                                 'Area': house.Area,
                                 'Floor': house.Floor,
                                 'Type': house.Type,
                                 'LandlordPhone': house.LandlordPhone,
                                 'Introduction': house.Introduction})
        elif function_id == '6':  #删除
            house_id = querylist.get('house_id')
            userhouse = UserHouse.objects.get(HouseID=house_id,UserID=user_id)
            userhouse.delete()
            houselist = []
            for x in UserHouse.objects.filter(UserID=user_id):
                house = House.objects.get(HouseID=x.HouseID)
                pics = Picture.objects.filter(HouseID=house.HouseID).values('PicPath')
                houselist.append({
                    'HouseID': house.HouseID,
                    'PicPathList': list(pics),
                    'Address': house.Address,
                    'Area': house.Area,
                    'Housetype': house.Housetype,
                    'Rent': house.Rent,
                    'Floor': house.Floor,
                    'Housename': house.Housename
                })
            return JsonResponse({'houselist': houselist})
        elif function_id == '7': # 搜索
            house_name = querylist.get('house_name')
            houses = House.objects.filter(Housename__contains=house_name)
            houselist = []
            for house in houses:
                try:
                    UserHouse.objects.get(HouseID=house.HouseID, UserID=user_id)
                    pics = Picture.objects.filter(HouseID=house.HouseID).values('PicPath')
                    houselist.append({
                        'HouseID': house.HouseID,
                        'PicPathList': list(pics),
                        'Address': house.Address,
                        'Area': house.Area,
                        'Housetype': house.Housetype,
                        'Rent': house.Rent,
                        'Floor': house.Floor,
                        'Housename': house.Housename
                    })
                except:
                    continue
            return JsonResponse({'houselist': houselist})
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})

@csrf_exempt
def information(request):
    if request.method == 'POST':
        querylist = request.POST
        function_id = querylist.get('function_id')
        user_id = querylist.get('user_id')
        user = User.objects.get(UserID=user_id)
        if function_id == '0':  # 我的订单
            orderlist = []
            order = Order.objects.filter(UserID=user_id, Pay=False)
            # 如果用户没有订单?
            for x in order:
                y = House.objects.get(HouseID=x.HouseID)
                orderlist.append({
                    'OrderDate': x.OrderDate.date(),
                    'OrderID': x.OrderID,
                    'HouseID': x.HouseID,
                    'LandlordName': y.LandlordName,
                    'LandlordPhone': y.LandlordPhone,
                    'Address': y.Address
                })
            return JsonResponse({'orderlist': orderlist})
        elif function_id == '1':  # 保修投诉
            orderlist = []
            order = Order.objects.filter(UserID=user_id)
            for x in order:
                y = House.objects.get(HouseID=x.HouseID)
                print(x.DueDate)
                orderlist.append({
                    'OrderDate': x.OrderDate.date(),
                    'OrderID': x.OrderID,
                    'HouseID': x.HouseID,
                    'LandlordName': y.LandlordName,
                    'LandlordPhone': y.LandlordPhone,
                    'Address': y.Address
                })
            return JsonResponse({'orderlist': orderlist})
        elif function_id == '2':  # 我的收藏
            houselist = []
            for x in UserHouse.objects.filter(UserID=user_id):
                pics = Picture.objects.filter(HouseID=x.HouseID).values('PicPath')
                house = House.objects.get(HouseID=x.HouseID)
                houselist.append({
                    'HouseID': x.HouseID,
                    'Housename': house.Housename,
                    'Floor': house.Floor,
                    'PicPathList': list(pics),
                    'Address': house.Address,
                    'Area': house.Area,
                    'Housetype': house.Housetype,
                    'Rent': house.Rent,
                })
            return JsonResponse({'houselist': houselist})
        elif function_id == '3':  # 个人资料
            return JsonResponse({'introduction': user.Introduction})
        elif function_id == '4':  # 主页
            houselist = []
            allhouse = House.objects.filter()
            for x in allhouse:
                pics = Picture.objects.filter(HouseID=x.HouseID).values('PicPath')
                house = House.objects.get(HouseID=x.HouseID)
                houselist.append({
                    'HouseID': x.HouseID,
                    'Housename': house.Housename,
                    'Floor': house.Floor,
                    'PicPathList': list(pics),
                    'Address': house.Address,
                    'Area': house.Area,
                    'Housetype': house.Housetype,
                    'Rent': house.Rent,
                })
            return JsonResponse({'houselist': houselist})
        elif function_id == '5': #短租
            house_id = querylist.get('house_id')
            flag = querylist.get('flag')
            house = House.objects.get(HouseID=house_id)
            house.Status = True
            house.save()
            start_day = datetime.datetime.strptime(querylist.get('start_day'), '%Y-%m-%d').date()
            finish_day = datetime.datetime.strptime(querylist.get('finish_day'), '%Y-%m-%d').date()
            day = (finish_day-start_day).days
            price = house.Rent/30*day
            if flag == '1':
                return JsonResponse({'dayrent': house.Rent/30, 'day':day , 'price': price})
            elif flag == '2':
                new_order = Order(OrderDate = start_day , DueDate = finish_day , Price=price , Pay=True , UserID=user_id , HouseID=house_id)
                new_order.save()
                return JsonResponse({'errornumber': 0, 'message': "短租成功！",'order_id':new_order.OrderID})
        elif function_id == '6': #长租
            house_id = querylist.get('house_id')
            flag = querylist.get('flag')
            house = House.objects.get(HouseID=house_id)
            house.Status = True
            house.save()
            start_day = datetime.datetime.strptime(querylist.get('start_day'), '%Y-%m-%d').date()
            month = int(querylist.get('month'))
            price = house.Rent*month
            finish_day = start_day + datetime.timedelta(days=month*30)
            if flag == '1':
                return JsonResponse({'Username': user.Username, 'Landlordname':house.LandlordName , 'Address': house.Address , 'Area':house.Area , 'Month':month , 'start_day':start_day , 'finish_day':finish_day})
            elif flag == '2':
                new_order = Order(OrderDate = start_day,DueDate = finish_day,Price=price,Pay=False,UserID=user_id,HouseID=house_id)
                new_order.save()
                order_id = new_order.OrderID
                file = request.FILES.get('file')
                suffix = '.' + file.name.split('.')[-1]
                file.name = str(order_id) + '合同' + suffix
                filepath = "http://127.0.0.1:8000/media/" + file.name
                new_contract = Contract(OrderID=order_id,File = file,FilePath= filepath)
                new_contract.save()
                return JsonResponse({'errornumber': 1, 'message': "长租成功！"})
        elif function_id == '7': #自动生成合同
            username = querylist.get('username')
            landlordname = querylist.get('landlordname')
            address = querylist.get('address')
            area = querylist.get('area')
            starttime = querylist.get('starttime')
            endtime = querylist.get('endtime')
            house_id = querylist.get('house_id')
            name = "租客"+user_id+"房屋"+house_id+"房屋租赁合同.pdf"
            pdf = canvas.Canvas(name)
            pdfmetrics.registerFont(TTFont('song',MEDIA_ROOT+'simsun.ttc'))
            pdf.setFont('song', 10)
            pdf.drawString(300, 700, "房屋租赁合同")
            pdf.drawString(100, 650, "甲方：" + landlordname)
            pdf.drawString(100, 630, "乙方：" + username)
            pdf.drawString(100, 610, "根据《中华人民共和国经济合同法》，为明确出租方与承租方的权利义务关系，经双方协商一致，签订本合同。")
            pdf.drawString(100, 590, "一、甲方将位于" + address + ",面积为" + area + "平方米的房子租给乙方使用。")
            pdf.drawString(100, 570, "二、租赁开始时间为" + starttime + ",结束时间为" + endtime)
            pdf.drawString(100, 530, "甲方签字：")
            pdf.drawString(300, 530, "乙方签字：")
            pdf.showPage()
            pdf.save()
            shutil.copy(name, './media/')
            pdf_url = "http://127.0.0.1:8000/media/"+name
            return JsonResponse({'errornumber': 1, 'message': "成功！",'pdf_url':pdf_url})
    else:
        return JsonResponse({'errornumber': 2, 'message': "请求方式错误"})

