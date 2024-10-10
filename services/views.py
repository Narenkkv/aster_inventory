from django.shortcuts import render,redirect
from services.models import *
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
import pandas as pd
import json

# Create your views here.


def index(request):
    try:
        if request.method == "POST" and 'login' in request.POST:
            username = request.POST['username'].lower()
            password = request.POST['pass'].lower()
            userNameCheck = Usermaster.objects.filter(name=username).all()
            if not userNameCheck:
                messages.error(request,'Invalid User Name !...')
                return redirect('index')
            else:
                passwordCheck = Usermaster.objects.filter(password=password).all()
                if not passwordCheck:
                    messages.error(request,'Incorrect Password !...')
                    return redirect('index')
                else:
                    return redirect('productentry')
        return render(request, 'login/index.html')
    except Exception as e:
        print(e)
        return render(request, 'login/index.html')

def productentry(request):
    try:
        if request.method == "POST" and 'recordsave' in request.POST:
            productcode = request.POST['item_name']
            productname = ProductMaster.objects.filter(item_code = '')
        return render(request, 'productEntry.html')
    except Exception as e:
        print(e)
        return render(request, 'login/index.html')


def productlist(request,search):
   try:
        result = []
        if search == '-':
            data = ProductMaster.objects.all().order_by('item_number')[:10]
            for i in data:
                res = {
                    'item_code':i.item_code,
                    'item_name':i.product_name
                }
                result.append(res)
        else:
            data = ProductMaster.objects.filter(search_name__icontains = search).all()
            for i in data:
                res = {
                    'item_code':i.item_code,
                    'item_name':i.product_name
                }
                result.append(res)
        return JsonResponse(result,safe = False)
   except Exception as e:
        print(e)
        return HttpResponse(json.dumps({'errorMsg': str(e)}), 500)