from django.shortcuts import render,redirect
from services.models import *
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.utils.encoding import smart_str
from django.db.models import Q, F, Func, Value,Case,When,IntegerField
from  django.db.models.functions import Upper
from django.db import transaction
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
                    if username.isdownload == 2:
                        return redirect('store_expiry_data_entry')
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
                with transaction.atomic():
                    product_name = request.POST['item_name']
                    packsize = request.POST['packsize']
                    batch = request.POST['batch'].upper()
                    qty = request.POST['qty']
                    mrp = request.POST['mrp']
                    expMonth = request.POST['expMonth']
                    expYear = request.POST['expYear']
                    getKey = product_name+packsize
                    getName = ItemMaster.objects.filter(unique_key = getKey).get()
                    ProductDetail.objects.create(
                        store_id = request.session['storeid'],
                        item_code = getName.aster_code,
                        item_name = getName.product_name,
                        batch = batch,
                        qty = qty,
                        mrp = mrp,
                        user_name = request.session['username'],
                        date_of_created = datetime.now(),
                        rack_no = request.session['rackNo'],
                        exp_date = expMonth+'-'+expYear,
                        pack_size = packsize
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
            data = ItemMaster.objects.all().order_by('aster_code')[:50]
            for i in data:
                res = {
                    'item_code':i.aster_code,
                    'item_name':i.product_name
                }
                result.append(res)
        else:
            data = ItemMaster.objects.filter(product_name__icontains = search).all().order_by('aster_code')[:50]
            for i in data:
                res = {
                    'item_code':i.aster_code,
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
            data = StoreMaster.objects.filter(active = 1).all().order_by('d_365_store_id')[:50]
            for i in data:
                res={
                    'store_code':i.d_365_store_id,
                    'store_name':i.d_365_store_id+'_'+i.short_name
                }
                result.append(res)
        else:   
            data = StoreMaster.objects.filter(Q(short_name__icontains=search) | Q(d_365_store_id__icontains=search),active = 1).all().order_by('d_365_store_id')[:50]
            for i in data:
                res = {
                    'store_code':i.d_365_store_id,
                    'store_name':i.d_365_store_id+'_'+i.short_name
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
    
def scanbarcode(request):
    if request.method == "POST":
        try:
            barCode = request.POST.get('barcode')
            print(barCode)
            product = ProductBarcodeMaster.objects.filter(barcode=barCode).first()
            print(product)
            if product:
                print({'ids': product.itemnumber, 'name': product.productdescription})
                return JsonResponse({
                    'success': True,
                    'product': {'ids': product.itemnumber, 'name': product.productdescription}
                })
            else:
                return JsonResponse({'success': False, 'error': 'Product not found.'})
        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

def store_expiry_report_download_data(request):
    try:
        if request.method == "POST" and 'storedownloadrecord' in request.POST:
            fromDate = request.POST['fromdate']
            toDate = request.POST['todate']
            connection_string = ('DRIVER={ODBC Driver 17 for SQL Server};'
                        f"SERVER={os.environ["HOST"]};"
                        f"DATABASE={os.environ["DB_NAME"]};"
                        f"UID={os.environ["DB_USER"]};"
                        f"PWD={os.environ["DB_PASSWORD"]};")
            conn = pyodbc.connect(connection_string)
            query = """
                SELECT a.store_id as Store_Code ,a.item_code as Item_code,a.item_name as Item_Name,a.batch as Batch,a.qty as Return_Qty,a.mrp as Mrp,b.vendor_name,c.store_state as Store_State 
                FROM  store_expiry_product_detail a  left join  supplier_return_item b
                    ON a.store_id = b.store_id AND a.item_code = b.item_code AND a.batch = b.batch_no AND a.id = b.productdetail_id
                    LEFT JOIN store_master c ON a.store_id = c.D_365_Store_Id
                            WHERE CAST(a.date_of_created AS DATE) BETWEEN ? AND ? and b.store_id = ?
                """
            print(query)
            filename = f'Expiry_Data_{fromDate}_{toDate}'
            data = pd.read_sql_query(query, conn, params=(fromDate, toDate,request.session['storeid']))
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                data.to_excel(writer, sheet_name='Audit_Data', index=False)
            output.seek(0)
            response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename={smart_str(filename + ".xlsx")}'
            conn.close()
            return response
        return render(request, 'store_expiry_download.html')
    except Exception as e:
        print(e)
        return render(request, 'login/index.html')
    
def store_expiry_data_entry(request):
    try:
        if request.method == "POST": 
            if 'expiryrecordsave' in request.POST:
                with transaction.atomic():
                    productcode = request.POST['item_name']
                    productname = ProductMaster.objects.filter(item_number = productcode).get()
                    batch = request.POST['batch'].upper()
                    qty = request.POST['qty']
                    mrp = request.POST['mrp']
                    expMonth = request.POST['expMonth']
                    expYear = request.POST['expYear']
                    newentry = StoreExpiryProductDetail.objects.create(
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
                    getproductdetailsid = newentry.id
                    state = StoreMaster.objects.get(d_365_store_id = request.session['storeid'])
                    itemList = EnteroItemLists.objects.annotate(batch_no_upper = Upper('batch_no')).filter(mdm = productname.item_reference, batch_no_upper = batch, state = state.store_state)
                    if itemList.exists():
                        selected_vendor = None
                        details =  itemList.order_by(state.store_state.lower())
                        state_column_prefix = f"{state.store_state.lower()}"
                        print(state_column_prefix)
                        for item in details:
                            if float(item.qty_sold) >= float(qty):
                                selected_vendor = item.entity_name
                                break 
                            else:
                                selected_vendor = 'Others'
                        SupplierReturnItem.objects.create(
                            store_id = request.session['storeid'],
                            item_code = productcode,
                            item_name = productname.product_name,
                            batch_no = batch,
                            date_of_expiry = item.batch_expiry_date,
                            vendor_name = selected_vendor,
                            accepted_qty = item.qty_sold,
                            created_by = request.session['username'],
                            date_of_creation = datetime.now(),
                            return_qty = qty,
                            remaining_qty = (float(item.qty_sold) - float(qty)),
                            productdetail_id = getproductdetailsid
                        )
                        if selected_vendor != 'Others':
                            itemList = EnteroItemLists.objects.annotate(batch_no_upper = Upper('batch_no')).filter(mdm = productname.item_reference, 
                                                        batch_no_upper = batch, state = state.store_state, entity_name = selected_vendor).update(qty_sold = (float(item.qty_sold) - float(qty)))
                    else:
                        date_string = expMonth+'-'+expYear
                        date_object = datetime.strptime(date_string, "%m-%Y")
                        formatted_date = date_object.strftime("%Y-%m-%d")
                        SupplierReturnItem.objects.create(
                            store_id = request.session['storeid'],
                            item_code = productcode,
                            item_name = productname.product_name,
                            batch_no = batch,
                            date_of_expiry = formatted_date,
                            vendor_name = 'Others',
                            accepted_qty = qty,
                            created_by = request.session['username'],
                            date_of_creation = datetime.now(),
                            return_qty = qty,
                            remaining_qty = 0,
                            productdetail_id = getproductdetailsid
                        )
                return redirect('store_expiry_data_entry')
        return render(request, 'store_expiry_product_entry.html')
    except Exception as e:
        print(e)
        return render(request, 'login/index.html')
    
def getpacksize(request,productname):
    try:
        getdetails = ItemMaster.objects.filter(product_name = productname).all().order_by('sales_unit')
        packList = [i.sales_unit for i in getdetails]
        return JsonResponse({'success': True,'product': {'packSize': packList}})
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'error': str(e)})

def storeproductlist(request,search):
   try:
        result = []
        if search == '-':
            data = ProductMaster.objects.all().order_by('product_name')[:50]
            for i in data:
                res = {
                    'item_code':i.item_number,
                    'item_name':i.product_name
                }
                result.append(res)
        else:
            data = ProductMaster.objects.filter(product_name__icontains = search).all().order_by('product_name')[:50]
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