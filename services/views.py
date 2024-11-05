from django.shortcuts import render,redirect
from services.models import *
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.utils.encoding import smart_str
from django.db.models import Q
import pandas as pd
import pyodbc
import os
import sqlite3
import json
import io
# Create your views here.


def index(request):
    try:
        if request.method == "POST" and 'login' in request.POST:
            username = request.POST['username'].lower()
            password = request.POST['pass'].lower()
            storeid = request.POST.get('store_name')
            rackNo = request.POST['rackno']
            print(storeid)
            if storeid:
                request.session['storeid'] = storeid
            request.session['rackNo'] = rackNo
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
                    request.session['username'] = username
                    username =  Usermaster.objects.filter(name=username).get()
                    if username.isdownload == 1:
                        return redirect('download_data')
                    else:
                        return redirect('productentry')
        return render(request, 'login/index.html')
    except Exception as e:
        print(e)
        return render(request, 'login/index.html')

def productentry(request):
    try:
        if request.method == "POST": 
            if 'recordsave' in request.POST:
                productcode = request.POST['item_name']
                productname = ProductMaster.objects.filter(item_number = productcode).get()
                batch = request.POST['batch'].upper()
                qty = request.POST['qty']
                mrp = request.POST['mrp']
                expMonth = request.POST['expMonth']
                expYear = request.POST['expYear']
                ProductDetail.objects.create(
                    store_id = request.session['storeid'],
                    item_code = productcode,
                    item_name = productname.product_name,
                    batch = batch,
                    qty = qty,
                    mrp = mrp,
                    user_name = request.session['username'],
                    date_of_created = datetime.now(),
                    rack_no = request.session['rackNo'],
                    exp_date = expMonth+'-'+expYear
                )
                return redirect('productentry')
        return render(request, 'productEntry.html')
    except Exception as e:
        print(e)
        return render(request, 'login/index.html')


def productlist(request,search):
   try:
        result = []
        if search == '-':
            data = ProductMaster.objects.all().order_by('item_number')[:50]
            for i in data:
                res = {
                    'item_code':i.item_number,
                    'item_name':i.product_name
                }
                result.append(res)
        else:
            data = ProductMaster.objects.filter(search_name__icontains = search).all().order_by('item_number')[:50]
            for i in data:
                res = {
                    'item_code':i.item_number,
                    'item_name':i.product_name
                }
                result.append(res)
        return JsonResponse(result,safe = False)
   except Exception as e:
        print(e)
        return HttpResponse(json.dumps({'errorMsg': str(e)}), 500)
   

def download_data(request):
    try:
        if request.method == "POST" and 'downloadrecord' in request.POST:
            fromDate = request.POST['fromdate']
            toDate = request.POST['todate']
            connection_string = ('DRIVER={ODBC Driver 17 for SQL Server};'
                            f"SERVER={os.environ["HOST"]};"
                            f"DATABASE={os.environ["DB_NAME"]};"
                            f"UID={os.environ["DB_USER"]};"
                            f"PWD={os.environ["DB_PASSWORD"]};")
            conn = pyodbc.connect(connection_string)
            query = """
                SELECT * FROM product_detail
                WHERE CAST(date_of_created AS DATE) BETWEEN ? AND ?
                """
            filename = f'Audit_Data_{fromDate}'
            data = pd.read_sql_query(query, conn, params=(fromDate, toDate))
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                data.to_excel(writer, sheet_name='Audit_Data', index=False)
            output.seek(0)
            response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename={smart_str("Audit_Data_" + fromDate + ".xlsx")}'
            conn.close()
            return response
        return render(request, 'download_data.html')
    except Exception as e:
        print(e)
        return render(request, 'login/index.html')
    
def storelist(request,search):
    try:
        result = []
        if search == "-":
            data = StoreMaster.objects.all().order_by('store_code')[:50]
            for i in data:
                res={
                    'store_code':i.store_code,
                    'store_name':i.store_code+'_'+i.short_name
                }
                result.append(res)
        else:   
            data = StoreMaster.objects.filter(Q(short_name__icontains=search) | Q(store_code__icontains=search)).all().order_by('store_code')[:50]
            for i in data:
                res = {
                    'store_code':i.store_code,
                    'store_name':i.store_code+'_'+i.short_name
                }
                result.append(res)
        return JsonResponse(result,safe = False)
    except Exception as e:  
        print(e)
        return HttpResponse(json.dumps({'errorMsg': str(e)}), 500)  
    
def logout(request):
    try:
        if 'username' in request.session:
            del request.session['username']
            del request.session['rackNo']
        if 'storeid' in request.session:
            del request.session['storeid']
        return redirect('index')
    except Exception as e:
        print(e)
        return redirect('index')